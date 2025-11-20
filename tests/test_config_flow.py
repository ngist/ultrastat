"""Test the UltraStat config flow."""

from unittest.mock import AsyncMock

from custom_components.ultrastat.const import (
    CONF_AREA,
    CONF_BOILER_BTUH,
    CONF_BOILER_INTLET_TEMP_ENTITY,
    CONF_BOILER_METER,
    CONF_BOILER_OUTLET_TEMP_ENTITY,
    CONF_BOILER_UNIT_COST,
    CONF_BOILER,
    CONF_CONTROL_MODE,
    CONF_COOLING,
    CONF_DEHUMIDIFICATION,
    CONF_HEATING_CALL_ENTITY,
    CONF_HEATING,
    CONF_HUMIDIFICATION,
    CONF_HUMIDITY_ENTITY,
    CONF_NUM_ROOMS,
    CONF_OUTDOOR_SENSORS,
    CONF_SOLAR_FLUX_ENTITY,
    CONF_TEMP_ENTITIES,
    CONF_WIND_DIRECTION_ENTITY,
    CONF_WIND_SPEED_ENTITY,
    CONF_CLIMATE_ENTITY,
    CONF_COOLING_CALL_ENTITY,
    CONF_HUMIDIFY_CALL_ENTITY,
    CONF_DEHUMIDIFY_CALL_ENTITY,
    DOMAIN,
    ControlMode,
)
import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from homeassistant import config_entries
from homeassistant.const import CONF_NAME, CONF_TEMPERATURE_UNIT, UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType

pytestmark = pytest.mark.usefixtures("mock_setup_entry")

MAIN_SETTINGS_MINIMAL = {
    CONF_NAME: "My ultrastat",
    CONF_NUM_ROOMS: 1,
    CONF_BOILER: False,
    # CONF_ADJACENCY: False, #TODO re-enable one adjacency is added back
    CONF_CONTROL_MODE: ControlMode.COMFORT,
    CONF_TEMPERATURE_UNIT: UnitOfTemperature.FAHRENHEIT,
}

MAIN_SETTINGS_MAXIMAL = {
    CONF_NAME: "My ultrastat",
    CONF_NUM_ROOMS: 3,
    CONF_BOILER: True,
    # CONF_ADJACENCY: False, #TODO re-enable one adjacency is added back
    CONF_CONTROL_MODE: ControlMode.COMFORT,
    CONF_TEMPERATURE_UNIT: UnitOfTemperature.FAHRENHEIT,
    CONF_OUTDOOR_SENSORS: {
        CONF_TEMP_ENTITIES: "sensor.outside_temp",
        CONF_HUMIDITY_ENTITY: "sensor.outside_humidity",
        CONF_WIND_SPEED_ENTITY: "sensor.wind_speed",
        CONF_WIND_DIRECTION_ENTITY: "sensor.wind_direction",
        CONF_SOLAR_FLUX_ENTITY: "sensor.solar_irradiance",
    },
}

BOILER_SETTINGS_MINIMAL = {
    CONF_HEATING_CALL_ENTITY: ["switch.zone1"],
}

BOILER_SETTINGS_MAXIMAL = {
    CONF_HEATING_CALL_ENTITY: ["switch.zone1"],
    "temp_sensors": {
        CONF_BOILER_INTLET_TEMP_ENTITY: "sensor.inlet_temp",
        CONF_BOILER_OUTLET_TEMP_ENTITY: "sensor.outlet_temp",
    },
    "energy_settings": {
        CONF_BOILER_BTUH: 140000,
        CONF_BOILER_METER: "utility_meter.boiler",
        CONF_BOILER_UNIT_COST: 0.5,
    },
}

ROOM_1_SETTINGS = {
    CONF_AREA: "area.living_room",
    CONF_TEMP_ENTITIES: ["sensor.room1_temp"],
}
ROOM_2_SETTINGS = {
    CONF_AREA: "area.kitchen",
    CONF_TEMP_ENTITIES: ["sensor.room2_temp"],
}
ROOM_3_SETTINGS = {
    CONF_AREA: "area.bedroom",
    CONF_TEMP_ENTITIES: ["sensor.room3_temp"],
    CONF_HEATING: {
        CONF_HEATING_CALL_ENTITY: "switch.boiler_zone1",
        CONF_CLIMATE_ENTITY: "climate.heatpump1",
    },
    CONF_COOLING: {
        CONF_COOLING_CALL_ENTITY: "switch.boiler_zone1",
        CONF_CLIMATE_ENTITY: "climate.heatpump1",
    },
    CONF_HUMIDIFICATION: {
        CONF_HUMIDIFY_CALL_ENTITY: "switch.humidifier",
        CONF_CLIMATE_ENTITY: "climate.heatpump1",
    },
    CONF_DEHUMIDIFICATION: {
        CONF_DEHUMIDIFY_CALL_ENTITY: "switch.dehumidifier",
        CONF_CLIMATE_ENTITY: "climate.heatpump1",
    },
}

PLATFORMS = ["climate"]


@pytest.mark.parametrize("platform", PLATFORMS)
async def test_minimal_config_flow(
    hass: HomeAssistant, mock_setup_entry: AsyncMock, platform
) -> None:
    """Test the minimal config flow with no optional inputs."""

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    assert not result["errors"]

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        MAIN_SETTINGS_MINIMAL,
    )
    await hass.async_block_till_done()

    assert result["type"] is FlowResultType.FORM
    assert not result["errors"]
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        ROOM_1_SETTINGS,
    )
    await hass.async_block_till_done()

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == "My ultrastat"
    expected = MAIN_SETTINGS_MINIMAL.copy()
    expected["room_conf"] = [ROOM_1_SETTINGS]
    expected["use_adjacency"] = False
    assert result["data"] == expected
    assert result["options"] == {}
    assert len(mock_setup_entry.mock_calls) == 1

    config_entry = hass.config_entries.async_entries(DOMAIN)[0]
    assert config_entry.data == expected
    assert config_entry.options == {}
    assert config_entry.title == "My ultrastat"


@pytest.mark.parametrize("platform", PLATFORMS)
async def test_maximal_config_flow(
    hass: HomeAssistant, mock_setup_entry: AsyncMock, platform
) -> None:
    """Test the config flow with all optional inputs."""

    # User Step
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    assert not result["errors"]

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        MAIN_SETTINGS_MAXIMAL,
    )
    await hass.async_block_till_done()

    # Boiler Settings Step
    assert result["type"] is FlowResultType.FORM
    assert not result["errors"]
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        BOILER_SETTINGS_MAXIMAL,
    )
    await hass.async_block_till_done()

    # ROOM 1
    assert result["type"] is FlowResultType.FORM
    assert not result["errors"]
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        ROOM_1_SETTINGS,
    )
    await hass.async_block_till_done()

    # ROOM 2
    assert result["type"] is FlowResultType.FORM
    assert not result["errors"]
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        ROOM_2_SETTINGS,
    )
    await hass.async_block_till_done()

    # ROOM 3
    assert result["type"] is FlowResultType.FORM
    assert not result["errors"]
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        ROOM_3_SETTINGS,
    )
    await hass.async_block_till_done()

    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == "My ultrastat"
    expected = MAIN_SETTINGS_MAXIMAL.copy()
    expected["room_conf"] = [ROOM_1_SETTINGS, ROOM_2_SETTINGS, ROOM_3_SETTINGS]
    expected["boiler_conf"] = BOILER_SETTINGS_MAXIMAL
    expected["use_adjacency"] = False  # TODO remove onvce adjacency is added
    assert result["data"] == expected
    assert result["options"] == {}
    assert len(mock_setup_entry.mock_calls) == 1

    config_entry = hass.config_entries.async_entries(DOMAIN)[0]
    assert config_entry.data == expected
    assert config_entry.options == {}
    assert config_entry.title == "My ultrastat"


def get_suggested(schema, key):
    """Get suggested value for key in voluptuous schema."""
    for k in schema:
        if k == key:
            if k.description is None or "suggested_value" not in k.description:
                return None
            return k.description["suggested_value"]
    # Wanted key absent from schema
    raise KeyError(f"Key `{key}` is missing from schema")


@pytest.mark.skip
@pytest.mark.parametrize("platform", ["sensor"])
async def test_options(hass: HomeAssistant, platform) -> None:
    """Test reconfiguring."""
    input_sensor_1_entity_id = "sensor.input1"
    input_sensor_2_entity_id = "sensor.input2"

    # Setup the config entry
    config_entry = MockConfigEntry(
        data={},
        domain=DOMAIN,
        options={
            "entity_id": input_sensor_1_entity_id,
            "name": "My ultrastat",
        },
        title="My ultrastat",
    )
    config_entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    result = await hass.config_entries.options.async_init(config_entry.entry_id)
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "init"
    schema = result["data_schema"].schema
    assert get_suggested(schema, "entity_id") == input_sensor_1_entity_id

    result = await hass.config_entries.options.async_configure(
        result["flow_id"],
        user_input={
            "entity_id": input_sensor_2_entity_id,
        },
    )
    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["data"] == {
        "entity_id": input_sensor_2_entity_id,
        "name": "My ultrastat",
    }
    assert config_entry.data == {}
    assert config_entry.options == {
        "entity_id": input_sensor_2_entity_id,
        "name": "My ultrastat",
    }
    assert config_entry.title == "My ultrastat"

    # Check config entry is reloaded with new options
    await hass.async_block_till_done()

    # Check the entity was updated, no new entity was created
    assert len(hass.states.async_all()) == 1

    # TODO Check the state of the entity has changed as expected
    state = hass.states.get(f"{platform}.my_ultrastat")
    assert state.attributes == {}
