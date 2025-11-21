"""Sensor platform for UniStat integration."""

import logging
from typing import Dict


from .const import (
    CONF_AREA,
    CONF_TEMP_ENTITY,
    CONF_HUMIDITY_ENTITY,
    CONF_HEATING_CALL_ENTITY,
    CONF_COOLING_CALL_ENTITY,
    CONF_HUMIDIFY_CALL_ENTITY,
    CONF_DEHUMIDIFY_CALL_ENTITY,
    CONF_CLIMATE_ENTITY,
    CONF_DEHUMIDIFICATION,
    CONF_HUMIDIFICATION,
)
from homeassistant.components.climate import (
    ClimateEntity,
    HVACMode,
    ClimateEntityFeature,
    ATTR_PRESET_MODE,
    ATTR_TEMPERATURE,
    ATTR_HUMIDITY,
    PRESET_NONE,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_NAME,
    UnitOfTemperature,
    CONF_TEMPERATURE_UNIT,
    STATE_UNAVAILABLE,
    STATE_UNKNOWN,
    EVENT_HOMEASSISTANT_START,
)
from homeassistant.core import (
    CoreState,
    Event,
    EventStateChangedData,
    HomeAssistant,
    State,
    callback,
)
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.event import (
    async_track_state_change_event,
)
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

_LOGGER = logging.getLogger(__name__)


# async def async_setup_platform(
#     hass: HomeAssistant,
#     config: ConfigType,
#     async_add_entities: AddEntitiesCallback,
#     discovery_info: DiscoveryInfoType | None = None,
# ) -> None:
#     """Set up the generic thermostat platform."""

#     await async_setup_reload_service(hass, DOMAIN, PLATFORMS)
#     await _async_setup_config(
#         hass, config, config.get(CONF_UNIQUE_ID), async_add_entities
#     )


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Initialize UniStat config entry."""

    def format_entity_id(name: str):
        return name.lower().replace(" ", "_").replace("-", "_")

    registry = er.async_get(hass)
    # Validate + resolve entity registry id to entity_id
    climate_entities = []
    for room in config_entry.data["room_conf"]:
        base_name = config_entry.data[CONF_NAME]
        _LOGGER.warning(
            "Configuring thermostat UI for %s",
            room[CONF_AREA],
        )
        name = f"{base_name} {room[CONF_AREA]}"
        entity_id = er.async_validate_entity_id(
            registry, format_entity_id(f"climate.{name}")
        )
        unique_id = f"{config_entry.entry_id}_{room[CONF_AREA]}"
        climate_entities.append(
            UniStatClimateEntity(
                hass,
                unique_id=unique_id,
                name=name,
                wrapped_entity_id=entity_id,
                temp_unit=config_entry.data[CONF_TEMPERATURE_UNIT],
                temperature_entity_id=room[CONF_TEMP_ENTITY],
                humidity_entity_id=room.get(CONF_HUMIDITY_ENTITY, None),
                heat_call_entity_id=room.get(CONF_HEATING_CALL_ENTITY, None),
                cool_call_entity_id=room.get(CONF_COOLING_CALL_ENTITY, None),
                humidify_call_entity_id=room[CONF_HUMIDIFICATION].get(
                    CONF_HUMIDIFY_CALL_ENTITY, None
                )
                if CONF_HUMIDIFICATION in room
                else None,
                dehumidify_call_entity_id=room[CONF_DEHUMIDIFICATION].get(
                    CONF_DEHUMIDIFY_CALL_ENTITY, None
                )
                if CONF_DEHUMIDIFICATION in room
                else None,
                climate_entity_id=room.get(CONF_CLIMATE_ENTITY, None),
                presets=None,  # TODO add preset support
            )
        )
    async_add_entities(climate_entities)


class UniStatClimateEntity(ClimateEntity, RestoreEntity):
    """UniStat CLimate."""

    _attr_should_poll = False
    _attr_has_entity_name = True
    _attr_hvac_modes = (
        HVACMode.OFF,
        HVACMode.AUTO,
    )

    def __init__(
        self,
        hass: HomeAssistant,
        unique_id: str,
        name: str,
        wrapped_entity_id: str,
        temp_unit: UnitOfTemperature,
        temperature_entity_id: str,
        humidity_entity_id: str | None = None,
        heat_call_entity_id: str | None = None,
        cool_call_entity_id: str | None = None,
        humidify_call_entity_id: str | None = None,
        dehumidify_call_entity_id: str | None = None,
        climate_entity_id: str | None = None,
        presets: Dict[str, Dict] | None = None,
    ) -> None:
        """Initialize unistat Sensor."""
        super().__init__()

        # Set builtin attributes
        self._wrapped_entity_id = wrapped_entity_id
        self._attr_name = name
        self._attr_unique_id = unique_id
        self._attr_temperature_unit = temp_unit
        self._attr_hvac_mode = HVACMode.OFF
        self._attr_supported_features = (
            ClimateEntityFeature.TARGET_TEMPERATURE
            | ClimateEntityFeature.TURN_ON
            | ClimateEntityFeature.TURN_OFF
        )

        if temp_unit == UnitOfTemperature.FAHRENHEIT:
            self._attr_max_temp = 85
            self._attr_min_temp = 60
        else:
            self._attr_max_temp = 30
            self._attr_min_temp = 15
        self._attr_target_temperature_step = 1

        self._has_humidity = humidity_entity_id and (
            dehumidify_call_entity_id or humidify_call_entity_id
        )
        if self._has_humidity:
            self._attr_min_humidity = 20
            self._attr_max_humidity = 70
            self._attr_supported_features |= ClimateEntityFeature.TARGET_HUMIDITY

        if presets:
            self._attr_supported_features |= ClimateEntityFeature.PRESET_MODE
            self._attr_preset_modes = [PRESET_NONE, *presets.keys()]
        else:
            presets = {}
            self._attr_preset_modes = [PRESET_NONE]
        self._presets = presets
        self._presets_inv = {v: k for k, v in presets.items()}

        # UniStatClimateEntity specific members
        # Entities
        self._temperature_entity_id = temperature_entity_id
        self._heat_call_entity_id = heat_call_entity_id
        self._cool_call_entity_id = cool_call_entity_id
        self._humidify_call_entity_id = humidify_call_entity_id
        self._dehumidify_call_entity_id = dehumidify_call_entity_id
        self._climate_entity_id = climate_entity_id
        self._humidity_entity_id = humidity_entity_id

    async def async_added_to_hass(self) -> None:
        """Run when entity about to be added."""
        await super().async_added_to_hass()

        # Add listener
        self.async_on_remove(
            async_track_state_change_event(
                self.hass,
                [self._temperature_entity_id],
                self._async_temperature_changed,
            )
        )
        if self._humidify_call_entity_id:
            self.async_on_remove(
                async_track_state_change_event(
                    self.hass, [self._humidity_entity_id], self._async_humidity_changed
                )
            )

        DEFAULT_HUMIDITY = 40

        def _default_temperature():
            return (
                72
                if self._attr_temperature_unit == UnitOfTemperature.FAHRENHEIT
                else 23
            )

        @callback
        def _async_startup(_: Event | None = None) -> None:
            """Init on startup."""
            sensor_state = self.hass.states.get(self._temperature_entity_id)
            if sensor_state and sensor_state.state not in (
                STATE_UNAVAILABLE,
                STATE_UNKNOWN,
            ):
                self._async_update_temp(sensor_state)
                self.async_write_ha_state()

            if self._humidify_call_entity_id:
                sensor_state = self.hass.states.get(self._humidity_entity_id)
                if sensor_state and sensor_state.state not in (
                    STATE_UNAVAILABLE,
                    STATE_UNKNOWN,
                ):
                    self._async_update_temp(sensor_state)
                    self.async_write_ha_state()

            # TODO set initial heating/cooling/humidity control states

        if self.hass.state is CoreState.running:
            _async_startup()
        else:
            self.hass.bus.async_listen_once(EVENT_HOMEASSISTANT_START, _async_startup)

        # Check If we have an old state
        if (old_state := await self.async_get_last_state()) is not None:
            # If we have no initial temperature, restore
            if self._attr_target_temperature is None:
                # If we have a previously saved temperature
                if old_state.attributes.get(ATTR_TEMPERATURE) is None:
                    self._attr_target_temperature = _default_temperature()
                    _LOGGER.warning(
                        "Undefined target temperature, falling back to %s",
                        self._attr_target_temperature,
                    )
                else:
                    self._target_temp = float(old_state.attributes[ATTR_TEMPERATURE])
            if self._has_humidity and self._attr_target_humidity is None:
                if old_state.attributes.get(ATTR_HUMIDITY) is None:
                    self._attr_target_humidity = DEFAULT_HUMIDITY
                    _LOGGER.warning(
                        "Undefined target humidity, falling back to %s",
                        self._attr_target_humidity,
                    )
                else:
                    self._attr_target_humidity = float(
                        old_state.attributes[ATTR_HUMIDITY]
                    )
            if (
                self.preset_modes
                and old_state.attributes.get(ATTR_PRESET_MODE) in self.preset_modes
            ):
                self._attr_preset_mode = old_state.attributes.get(ATTR_PRESET_MODE)
            if not self._attr_hvac_mode and old_state.state:
                self._attr_hvac_mode = HVACMode(old_state.state)

        else:
            # No previous state, try and restore defaults
            if self._attr_target_temperature is None:
                self._attr_target_temperature = _default_temperature()
                _LOGGER.warning(
                    "No previously saved temperature, setting to %s",
                    self._attr_target_temperature,
                )
            if self._has_humidity and self._attr_target_humidity is None:
                self._attr_target_humidity = DEFAULT_HUMIDITY
                _LOGGER.warning(
                    "No previously saved humidity, setting to %s",
                    self._attr_target_humidity,
                )

        # Set default state to off
        if not self._attr_hvac_mode:
            self._attr_hvac_mode = HVACMode.OFF

    async def _async_humidity_changed(
        self, event: Event[EventStateChangedData]
    ) -> None:
        """Handle humidity changes."""
        new_state = event.data["new_state"]
        if new_state is None or new_state.state in (STATE_UNAVAILABLE, STATE_UNKNOWN):
            return

        self._async_update_humidity(new_state)
        self.async_write_ha_state()

    async def _async_temperature_changed(
        self, event: Event[EventStateChangedData]
    ) -> None:
        """Handle temperature changes."""
        new_state = event.data["new_state"]
        if new_state is None or new_state.state in (STATE_UNAVAILABLE, STATE_UNKNOWN):
            return

        self._async_update_temp(new_state)
        self.async_write_ha_state()

    @callback
    def _async_update_temp(self, state: State) -> None:
        """Update thermostat with latest state from sensor."""
        try:
            temperature = float(state.state)
            if temperature < -100 or temperature > 150:
                raise ValueError(f"Sensor has illegal state {state.state}")  # noqa: TRY301
            self._attr_current_temperature = temperature
        except ValueError as ex:
            _LOGGER.error("Unable to update from sensor: %s", ex)

    @callback
    def _async_update_humidity(self, state: State) -> None:
        """Update thermostat with latest state from sensor."""
        try:
            humidity = float(state.state)
            if humidity < 0 or humidity > 100:
                raise ValueError(f"Sensor has illegal state {state.state}")  # noqa: TRY301
            self._attr_current_humidity = humidity
        except ValueError as ex:
            _LOGGER.error("Unable to update from sensor: %s", ex)

    async def async_set_hvac_mode(self, hvac_mode):
        """Set hvac mode."""
        if hvac_mode not in (self.hvac_modes or []):
            _LOGGER.error("Unrecognized hvac mode: %s", hvac_mode)
            return
        self._attr_hvac_mode = hvac_mode
        # Ensure we update the current operation after changing the mode
        self.async_write_ha_state()

    async def async_turn_on(self):
        """Turn the entity on."""
        await self.async_set_hvac_mode(HVACMode.AUTO)

    async def async_turn_off(self):
        """Turn the entity off."""
        await self.async_set_hvac_mode(HVACMode.OFF)

    async def async_set_humidity(self, humidity):
        """Set new target humidity."""
        raise NotImplementedError

    async def async_set_temperature(self, **kwargs):
        """Set new target temperature."""
        raise NotImplementedError

    async def async_set_preset_mode(self, preset_mode):
        """Set new preset mode."""
        if preset_mode not in (self.preset_modes or []):
            raise ValueError(
                f"Got unsupported preset_mode {preset_mode}. Must be one of"
                f" {self.preset_modes}"
            )
        if preset_mode == self._attr_preset_mode:
            return
        self._attr_preset_mode = preset_mode
        raise NotImplementedError

        self.async_write_ha_state()
