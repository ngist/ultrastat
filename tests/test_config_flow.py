"""Test the UltraStat config flow."""

from unittest.mock import AsyncMock

from .constants import (
    MAIN_SETTINGS_MINIMAL,
    MAIN_SETTINGS_MAXIMAL,
    BOILER_SETTINGS_MAXIMAL,
    ROOM_1_SETTINGS,
    ROOM_2_SETTINGS,
    ROOM_3_SETTINGS,
    ROOM_1_SETTINGS_HUMIDITY,
    ROOM_2_DUPE_TEMP_OUTSIDE,
    ROOM_2_DUPE_AREA,
    ROOM_2_DUPE_HUMIDITY_INSIDE,
    ROOM_2_DUPE_HUMIDITY_OUTSIDE,
    ROOM_2_DUPE_TEMP_BOILER,
    ROOM_2_DUPE_TEMP_INSIDE,
)
from custom_components.ultrastat.const import (
    DOMAIN,
)
import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType

pytestmark = pytest.mark.usefixtures("mock_setup_entry")


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
    assert result["title"] == "My UniStat"
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
    assert config_entry.title == "My UniStat"


DUPLICATE_CASES = [
    (ROOM_2_DUPE_AREA, "area_reused"),
    (ROOM_2_DUPE_TEMP_INSIDE, "temp_sensor_reused"),
    (ROOM_2_DUPE_TEMP_OUTSIDE, "temp_sensor_reused"),
    (ROOM_2_DUPE_TEMP_BOILER, "temp_sensor_reused"),
    (ROOM_2_DUPE_HUMIDITY_INSIDE, "humidity_sensor_reused"),
    (ROOM_2_DUPE_HUMIDITY_OUTSIDE, "humidity_sensor_reused"),
]


@pytest.mark.parametrize("platform", PLATFORMS)
@pytest.mark.parametrize("bad_room,expected_error", DUPLICATE_CASES)
async def test_config_flow_duplicate_area(
    hass: HomeAssistant, mock_setup_entry: AsyncMock, platform, bad_room, expected_error
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
        ROOM_1_SETTINGS_HUMIDITY,
    )
    await hass.async_block_till_done()

    # ROOM 2
    assert result["type"] is FlowResultType.FORM
    assert not result["errors"]
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        bad_room,
    )
    await hass.async_block_till_done()
    assert result["type"] is FlowResultType.FORM
    assert expected_error == result["errors"]["base"]


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
            "name": "My UniStat",
        },
        title="My UniStat",
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
        "name": "My UniStat",
    }
    assert config_entry.data == {}
    assert config_entry.options == {
        "entity_id": input_sensor_2_entity_id,
        "name": "My UniStat",
    }
    assert config_entry.title == "My UniStat"

    # Check config entry is reloaded with new options
    await hass.async_block_till_done()

    # Check the entity was updated, no new entity was created
    assert len(hass.states.async_all()) == 1

    # TODO Check the state of the entity has changed as expected
    state = hass.states.get(f"{platform}.my_unistat")
    assert state.attributes == {}
