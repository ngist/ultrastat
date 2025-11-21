"""Constants for the UniStat integration."""

from enum import StrEnum

DOMAIN = "unistat"

# General Purpose (used multiple forms)
CONF_TEMP_ENTITY = "temp_entity"
CONF_HUMIDITY_ENTITY = "humidity_entity"
CONF_CLIMATE_ENTITY = "climate_entity"

# Main Settings
CONF_CONTROL_MODE = "control_mode"
CONF_NUM_ROOMS = "num_rooms"
CONF_ADJACENCY = "use_adjacency"
CONF_BOILER = "has_boiler"
CONF_WIND_SPEED_ENTITY = "wind_speed_entity"
CONF_WIND_DIRECTION_ENTITY = "wind_direction_entity"
CONF_SOLAR_FLUX_ENTITY = "solar_flux_entity"
CONF_OUTDOOR_SENSORS = "outdoor_sensors"

# Room Specific Settings
CONF_AREA = "area"
CONF_HEATING_CALL_ENTITY = "heat_call_entity"
CONF_COOLING_CALL_ENTITY = "cooling_call_entity"
CONF_DEHUMIDIFY_CALL_ENTITY = "dehumidify_call_entity"
CONF_HUMIDIFY_CALL_ENTITY = "humidify_call_entity"
CONF_HEATING = "heating"
CONF_COOLING = "cooling"
CONF_HUMIDIFICATION = "humidification"
CONF_DEHUMIDIFICATION = "dehumidification"

# Boiler Specific Settings
CONF_BOILER_BTUH = "boiler_btuh"
CONF_BOILER_METER = "boiler_meter"
CONF_BOILER_UNIT_COST = "boiler_unit_cost"
CONF_BOILER_INTLET_TEMP_ENTITY = "boiler_inlet_temp"
CONF_BOILER_OUTLET_TEMP_ENTITY = "boiler_outlet_temp"


class ControlMode(StrEnum):
    """Thermostat Modes."""

    COMFORT = "Comfort"
    ECO = "Eco"
    BUDGET = "Budget"
