"""Test the UltraStat integration."""

from custom_components.ultrastat.const import (
    CONF_ADJACENCY,
    CONF_BOILER,
    CONF_ROOM_TEMP_ENTITIES,
    DOMAIN,
)
import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from homeassistant.components.climate import ClimateEntityFeature, HVACMode
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er


@pytest.mark.parametrize("platform", ["climate"])
async def test_setup_and_remove_config_entry(
    hass: HomeAssistant,
    entity_registry: er.EntityRegistry,
    platform: str,
) -> None:
    """Test setting up and removing a config entry."""
    input_sensor_entity_id = "sensor.input"
    ultrastat_entity_id = f"{platform}.my_ultrastat"

    # Setup the config entry
    config_entry = MockConfigEntry(
        data={
            CONF_ROOM_TEMP_ENTITIES: [input_sensor_entity_id],
            "name": "My ultrastat",
            "room_conf": [{}],
            CONF_BOILER: False,
            CONF_ADJACENCY: False,
        },
        domain=DOMAIN,
        options={},
        title="My ultrastat",
    )
    config_entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    # Check the entity is registered in the entity registry
    assert entity_registry.async_get(ultrastat_entity_id) is not None

    # Check the platform is setup correctly
    state = hass.states.get(ultrastat_entity_id)
    # TODO Check the state of the entity has changed as expected
    assert state.state == "off"
    assert state.attributes == {
        "current_temperature": None,
        "friendly_name": "My ultrastat",
        "hvac_modes": [
            HVACMode.OFF,
            HVACMode.COOL,
            HVACMode.HEAT,
            HVACMode.HEAT_COOL,
        ],
        "max_temp": 35.0,
        "min_temp": 7.0,
        "supported_features": ClimateEntityFeature(0),
    }

    # Remove the config entry
    assert await hass.config_entries.async_remove(config_entry.entry_id)
    await hass.async_block_till_done()

    # Check the state and entity registry entry are removed
    assert hass.states.get(ultrastat_entity_id) is None
    assert entity_registry.async_get(ultrastat_entity_id) is None
