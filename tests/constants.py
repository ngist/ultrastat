from homeassistant.const import CONF_NAME, CONF_TEMPERATURE_UNIT, UnitOfTemperature
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
    CONF_TEMP_ENTITY,
    CONF_WIND_DIRECTION_ENTITY,
    CONF_WIND_SPEED_ENTITY,
    CONF_CLIMATE_ENTITY,
    CONF_COOLING_CALL_ENTITY,
    CONF_HUMIDIFY_CALL_ENTITY,
    CONF_DEHUMIDIFY_CALL_ENTITY,
    ControlMode,
)
# NOMINAL

MAIN_SETTINGS_MINIMAL = {
    CONF_NAME: "My ultrastat",
    CONF_NUM_ROOMS: 1,
    CONF_BOILER: False,
    # CONF_ADJACENCY: False, #TODO re-enable one adjacency is added back
    CONF_CONTROL_MODE: ControlMode.COMFORT,
    CONF_TEMPERATURE_UNIT: UnitOfTemperature.FAHRENHEIT,
}

MAIN_SETTINGS_MAXIMAL = {
    CONF_NAME: "My UniStat",
    CONF_NUM_ROOMS: 3,
    CONF_BOILER: True,
    # CONF_ADJACENCY: False, #TODO re-enable one adjacency is added back
    CONF_CONTROL_MODE: ControlMode.COMFORT,
    CONF_TEMPERATURE_UNIT: UnitOfTemperature.FAHRENHEIT,
    CONF_OUTDOOR_SENSORS: {
        CONF_TEMP_ENTITY: "sensor.outside_temp",
        CONF_HUMIDITY_ENTITY: "sensor.outside_humidity",
        CONF_WIND_SPEED_ENTITY: "sensor.wind_speed",
        CONF_WIND_DIRECTION_ENTITY: "sensor.wind_direction",
        CONF_SOLAR_FLUX_ENTITY: "sensor.solar_irradiance",
    },
}

BOILER_SETTINGS_MAXIMAL = {
    CONF_HEATING_CALL_ENTITY: ["switch.zone1"],
    CONF_AREA: ["living_room", "kitchen"],
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
    CONF_AREA: "living_room",
    CONF_TEMP_ENTITY: "sensor.room1_temp",
}
ROOM_2_SETTINGS = {
    CONF_AREA: "kitchen",
    CONF_TEMP_ENTITY: "sensor.room2_temp",
}

ROOM_3_SETTINGS = {
    CONF_AREA: "bedroom",
    CONF_TEMP_ENTITY: "sensor.room3_temp",
    CONF_HUMIDITY_ENTITY: "sensor.room3_humidity",
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

# OFF Nominal

ROOM_1_SETTINGS_HUMIDITY = {
    CONF_AREA: "living_room",
    CONF_TEMP_ENTITY: "sensor.room1_temp",
    CONF_HUMIDITY_ENTITY: "sensor.room1_humidity",
}
ROOM_2_DUPE_AREA = {
    CONF_AREA: "living_room",
    CONF_TEMP_ENTITY: "sensor.room2_temp",
}
ROOM_2_DUPE_TEMP_INSIDE = {
    CONF_AREA: "kitchen",
    CONF_TEMP_ENTITY: "sensor.room1_temp",
}
ROOM_2_DUPE_TEMP_OUTSIDE = {
    CONF_AREA: "kitchen",
    CONF_TEMP_ENTITY: "sensor.outside_temp",
}
ROOM_2_DUPE_TEMP_BOILER = {
    CONF_AREA: "kitchen",
    CONF_TEMP_ENTITY: "sensor.inlet_temp",
}
ROOM_2_DUPE_HUMIDITY_INSIDE = {
    CONF_AREA: "kitchen",
    CONF_TEMP_ENTITY: "sensor.room2_temp",
    CONF_HUMIDITY_ENTITY: "sensor.room1_humidity",
}
ROOM_2_DUPE_HUMIDITY_OUTSIDE = {
    CONF_AREA: "kitchen",
    CONF_TEMP_ENTITY: "sensor.room2_temp",
    CONF_HUMIDITY_ENTITY: "sensor.room1_humidity",
}
