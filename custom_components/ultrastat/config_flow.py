"""Config flow for the UltraStat integration."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant.components.sensor import DOMAIN as SENSOR_DOMAIN
from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.components.utility_meter import DOMAIN as UTILITY_METER_DOMAIN
from homeassistant.components.switch import DOMAIN as SWITCH_DOMAIN
from homeassistant.components.climate import DOMAIN as CLIMATE_DOMAIN
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import (
    CONF_NAME,
    CONF_TEMPERATURE_UNIT,
    UnitOfTemperature,
    UnitOfPower,
)
from homeassistant.helpers import selector
from homeassistant.data_entry_flow import section

from .const import (
    CONF_ADJACENCY,
    CONF_AREA,
    CONF_BOILER_BTUH,
    CONF_BOILER_INTLET_TEMP_ENTITY,
    CONF_BOILER_METER,
    CONF_BOILER_OUTLET_TEMP_ENTITY,
    CONF_BOILER_UNIT_COST,
    CONF_BOILER,
    CONF_CLIMATE_ENTITY,
    CONF_CONTROL_MODE,
    CONF_COOLING_CALL_ENTITY,
    CONF_COOLING,
    CONF_DEHUMIDIFICATION,
    CONF_DEHUMIDIFY_CALL_ENTITY,
    CONF_HEATING_CALL_ENTITY,
    CONF_HEATING,
    CONF_HUMIDIFICATION,
    CONF_HUMIDIFY_CALL_ENTITY,
    CONF_HUMIDITY_ENTITY,
    CONF_NUM_ROOMS,
    CONF_OUTDOOR_SENSORS,
    CONF_SOLAR_FLUX_ENTITY,
    CONF_TEMP_ENTITIES,
    CONF_WIND_DIRECTION_ENTITY,
    CONF_WIND_SPEED_ENTITY,
    DOMAIN,
    ControlMode,
)

MAIN_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_NAME): selector.TextSelector(),
        vol.Required(CONF_NUM_ROOMS): selector.NumberSelector({"min": 1, "step": 1}),
        vol.Required(
            CONF_CONTROL_MODE,
            default=ControlMode.COMFORT,
        ): selector.SelectSelector(
            selector.SelectSelectorConfig(
                options=list(ControlMode),
                mode=selector.SelectSelectorMode.DROPDOWN,
            ),
        ),
        vol.Required(
            CONF_TEMPERATURE_UNIT,
            default=UnitOfTemperature.FAHRENHEIT,
        ): selector.SelectSelector(
            selector.SelectSelectorConfig(
                options=[UnitOfTemperature.FAHRENHEIT, UnitOfTemperature.CELSIUS],
                mode=selector.SelectSelectorMode.DROPDOWN,
            ),
        ),
        vol.Required(CONF_BOILER, default=False): bool,
        # vol.Required(CONF_ADJACENCY, default=False): bool, #TODO add this feature later
        vol.Optional(CONF_OUTDOOR_SENSORS): section(
            vol.Schema(
                {
                    vol.Optional(CONF_TEMP_ENTITIES): selector.EntitySelector(
                        selector.EntitySelectorConfig(
                            domain=SENSOR_DOMAIN,
                            device_class=SensorDeviceClass.TEMPERATURE,
                        )
                    ),
                    vol.Optional(CONF_HUMIDITY_ENTITY): selector.EntitySelector(
                        selector.EntitySelectorConfig(
                            domain=SENSOR_DOMAIN,
                            device_class=SensorDeviceClass.HUMIDITY,
                        )
                    ),
                    vol.Optional(CONF_WIND_SPEED_ENTITY): selector.EntitySelector(
                        selector.EntitySelectorConfig(
                            domain=SENSOR_DOMAIN,
                            device_class=SensorDeviceClass.WIND_SPEED,
                        )
                    ),
                    vol.Optional(CONF_WIND_DIRECTION_ENTITY): selector.EntitySelector(
                        selector.EntitySelectorConfig(
                            domain=SENSOR_DOMAIN,
                            device_class=SensorDeviceClass.WIND_DIRECTION,
                        )
                    ),
                    vol.Optional(CONF_SOLAR_FLUX_ENTITY): selector.EntitySelector(
                        selector.EntitySelectorConfig(
                            domain=SENSOR_DOMAIN,
                            device_class=SensorDeviceClass.IRRADIANCE,
                        )
                    ),
                }
            ),
            {"collapsed": True},
        ),
    }
)

BOILER_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HEATING_CALL_ENTITY): selector.EntitySelector(
            selector.EntitySelectorConfig(
                domain=SWITCH_DOMAIN,
                multiple=True,
            )
        ),
        vol.Required("temp_sensors"): section(
            vol.Schema(
                {
                    vol.Optional(
                        CONF_BOILER_INTLET_TEMP_ENTITY
                    ): selector.EntitySelector(
                        selector.EntitySelectorConfig(
                            domain=SENSOR_DOMAIN,
                            device_class=SensorDeviceClass.TEMPERATURE,
                        )
                    ),
                    vol.Optional(
                        CONF_BOILER_OUTLET_TEMP_ENTITY
                    ): selector.EntitySelector(
                        selector.EntitySelectorConfig(
                            domain=SENSOR_DOMAIN,
                            device_class=SensorDeviceClass.TEMPERATURE,
                        )
                    ),
                }
            ),
            {"collapsed": True},
        ),
        vol.Required("energy_settings"): section(
            vol.Schema(
                {
                    vol.Optional(CONF_BOILER_BTUH): selector.NumberSelector(
                        {
                            "min": 0,
                            "max": 500000,
                            "unit_of_measurement": UnitOfPower.BTU_PER_HOUR,
                        }
                    ),
                    vol.Optional(CONF_BOILER_METER): selector.EntitySelector(
                        selector.EntitySelectorConfig(
                            domain=UTILITY_METER_DOMAIN,
                        )
                    ),
                    vol.Optional(CONF_BOILER_UNIT_COST): selector.NumberSelector(
                        {
                            "min": 0.0,
                            "max": 100.0,
                            "step": 0.01,
                            "unit_of_measurement": "$/Kbtu",
                        }
                    ),
                }
            ),
            {"collapsed": True},
        ),
    }
)

ROOM_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_AREA): selector.AreaSelector(),
        vol.Required(CONF_TEMP_ENTITIES): selector.EntitySelector(
            selector.EntitySelectorConfig(
                domain=SENSOR_DOMAIN,
                device_class=SensorDeviceClass.TEMPERATURE,
                multiple=True,
            )
        ),
        vol.Optional(CONF_HUMIDITY_ENTITY): selector.EntitySelector(
            selector.EntitySelectorConfig(
                domain=SENSOR_DOMAIN,
                device_class=SensorDeviceClass.HUMIDITY,
            )
        ),
        vol.Optional(CONF_HEATING): section(
            vol.Schema(
                {
                    vol.Optional(CONF_HEATING_CALL_ENTITY): selector.EntitySelector(
                        selector.EntitySelectorConfig(domain=SWITCH_DOMAIN)
                    ),
                    vol.Optional(CONF_CLIMATE_ENTITY): selector.EntitySelector(
                        selector.EntitySelectorConfig(domain=CLIMATE_DOMAIN)
                    ),
                }
            ),
            {"collapsed": True},
        ),
        vol.Optional(CONF_COOLING): section(
            vol.Schema(
                {
                    vol.Optional(CONF_COOLING_CALL_ENTITY): selector.EntitySelector(
                        selector.EntitySelectorConfig(domain=SWITCH_DOMAIN)
                    ),
                    vol.Optional(CONF_CLIMATE_ENTITY): selector.EntitySelector(
                        selector.EntitySelectorConfig(domain=CLIMATE_DOMAIN)
                    ),
                }
            ),
            {"collapsed": True},
        ),
        vol.Optional(CONF_HUMIDIFICATION): section(
            vol.Schema(
                {
                    vol.Optional(CONF_HUMIDIFY_CALL_ENTITY): selector.EntitySelector(
                        selector.EntitySelectorConfig(domain=SWITCH_DOMAIN)
                    ),
                    vol.Optional(CONF_CLIMATE_ENTITY): selector.EntitySelector(
                        selector.EntitySelectorConfig(domain=CLIMATE_DOMAIN)
                    ),
                }
            ),
            {"collapsed": True},
        ),
        vol.Optional(CONF_DEHUMIDIFICATION): section(
            vol.Schema(
                {
                    vol.Optional(CONF_DEHUMIDIFY_CALL_ENTITY): selector.EntitySelector(
                        selector.EntitySelectorConfig(domain=SWITCH_DOMAIN)
                    ),
                    vol.Optional(CONF_CLIMATE_ENTITY): selector.EntitySelector(
                        selector.EntitySelectorConfig(domain=CLIMATE_DOMAIN)
                    ),
                }
            ),
            {"collapsed": True},
        ),
    }
)


def gen_adjacency_schema(num_rooms: int):
    """Generates an adjacency matrix schema based on the number of rooms."""
    return vol.Schema({})


class ConfigFlowHandler(ConfigFlow, domain=DOMAIN):
    """Handle a config or options flow for UltraStat."""

    VERSION = 1
    MINOR_VERSION = 1

    # def async_config_entry_title(self, options: Mapping[str, Any]) -> str:
    #     """Return config entry title."""
    #     return cast(str, options["name"]) if "name" in options else ""

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Invoked when a user initiates a flow via the user interface."""
        if user_input is not None:
            self.data = user_input
            self.data["room_conf"] = []
            self.data[CONF_ADJACENCY] = False  # TODO Remove once adjacency is supported
            if self.data[CONF_BOILER]:
                return await self.async_step_boiler()
            # Return the form of the next step.
            return await self.async_step_room()

        return self.async_show_form(step_id="user", data_schema=MAIN_SCHEMA)

    async def async_step_boiler(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Configure boiler options."""
        if user_input is not None:
            # Input is valid, set data.
            self.data["boiler_conf"] = user_input
            # Return the form of the next step.
            return await self.async_step_room()

        return self.async_show_form(step_id="boiler", data_schema=BOILER_SCHEMA)

    async def async_step_adjacency(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Configure room adjacency matrix."""
        if user_input is not None:
            # Input is valid, set data.
            self.data["adjacency"] = user_input
            # Return the form of the next step.
            return self.async_create_entry(title=self.data[CONF_NAME], data=self.data)
        return self.async_show_form(
            step_id="adjacency",
            data_schema=gen_adjacency_schema(self.data[CONF_NUM_ROOMS]),
        )

    async def async_step_room(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Captures configuration of thermal controls in each room."""
        if user_input is not None:
            # Input is valid, set data.
            self.data["room_conf"].append(user_input)
            if len(self.data["room_conf"]) == self.data[CONF_NUM_ROOMS]:
                if self.data[CONF_ADJACENCY]:
                    return await self.async_step_adjacency()

                return self.async_create_entry(
                    title=self.data[CONF_NAME], data=self.data
                )
            # Return the form of the next step.
            return await self.async_step_room()

        return self.async_show_form(step_id="room", data_schema=ROOM_SCHEMA)
