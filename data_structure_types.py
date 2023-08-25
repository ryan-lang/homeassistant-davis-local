from homeassistant.components.sensor import STATE_CLASS_MEASUREMENT
from homeassistant.const import (
    TEMP_FAHRENHEIT,
    PERCENTAGE,
    CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    TIME_SECONDS,
    UnitOfSpeed,
    UnitOfLength,
    UnitOfIrradiance,
    UnitOfPressure,
    DEGREE
)
from homeassistant.components.sensor.const import (
    SensorDeviceClass
)

RAIN_COUNT = "rain_count"
RAIN_COUNT_PER_HOUR = "rain_count_per_hour"

DATA_STRUCTURE_ENTITIES = {
    1: [
        {"entity": "temp", "unit": TEMP_FAHRENHEIT, "icon": "mdi:thermometer", "device_class": SensorDeviceClass.TEMPERATURE, "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "hum", "unit": PERCENTAGE, "icon": "mdi:water-percent", "device_class": SensorDeviceClass.HUMIDITY, "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "dew_point", "unit": TEMP_FAHRENHEIT, "icon": "mdi:weather-rainy", "device_class": SensorDeviceClass.TEMPERATURE, "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "wet_bulb", "unit": TEMP_FAHRENHEIT, "icon": "mdi:thermometer", "device_class": SensorDeviceClass.TEMPERATURE, "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "heat_index", "unit": TEMP_FAHRENHEIT, "icon": "mdi:weather-sunny", "device_class": SensorDeviceClass.TEMPERATURE, "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "wind_chill", "unit": TEMP_FAHRENHEIT, "icon": "mdi:weather-windy", "device_class": SensorDeviceClass.TEMPERATURE, "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "thw_index", "unit": TEMP_FAHRENHEIT, "icon": "mdi:weather-sunny", "device_class": SensorDeviceClass.TEMPERATURE, "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "thsw_index", "unit": TEMP_FAHRENHEIT, "icon": "mdi:weather-sunny", "device_class": SensorDeviceClass.TEMPERATURE, "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "wind_speed_last", "unit": UnitOfSpeed.MILES_PER_HOUR, "icon": "mdi:weather-windy", "device_class": SensorDeviceClass.WIND_SPEED, "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "wind_dir_last", "unit": DEGREE, "icon": "mdi:compass", "device_class": None, "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "wind_speed_avg_last_1_min", "unit": UnitOfSpeed.MILES_PER_HOUR, "icon": "mdi:weather-windy", "device_class": SensorDeviceClass.WIND_SPEED, "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "wind_dir_scalar_avg_last_1_min", "unit": DEGREE, "icon": "mdi:compass", "device_class": None, "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "wind_speed_avg_last_2_min", "unit": UnitOfSpeed.MILES_PER_HOUR, "icon": "mdi:weather-windy", "device_class": SensorDeviceClass.WIND_SPEED, "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "wind_dir_scalar_avg_last_2_min", "unit": DEGREE, "icon": "mdi:compass", "device_class": None, "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "wind_speed_hi_last_2_min", "unit": UnitOfSpeed.MILES_PER_HOUR, "icon": "mdi:weather-windy", "device_class": SensorDeviceClass.WIND_SPEED, "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "wind_dir_at_hi_speed_last_2_min", "unit": DEGREE, "icon": "mdi:compass", "device_class": None, "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "wind_speed_avg_last_10_min", "unit": UnitOfSpeed.MILES_PER_HOUR, "icon": "mdi:weather-windy", "device_class": SensorDeviceClass.WIND_SPEED, "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "wind_dir_scalar_avg_last_10_min", "unit": DEGREE, "icon": "mdi:compass", "device_class": None, "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "wind_speed_hi_last_10_min", "unit": UnitOfSpeed.MILES_PER_HOUR, "icon": "mdi:weather-windy", "device_class": SensorDeviceClass.WIND_SPEED, "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "wind_dir_at_hi_speed_last_10_min", "unit": DEGREE, "icon": "mdi:compass", "device_class": None, "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "rain_size", "unit": RAIN_COUNT, "icon": "mdi:water", "device_class": SensorDeviceClass.ENUM, "state_class": None},
        {"entity": "rain_rate_last", "unit": RAIN_COUNT_PER_HOUR, "icon": "mdi:water", "device_class": SensorDeviceClass.PRECIPITATION_INTENSITY, "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "rain_rate_hi", "unit": RAIN_COUNT_PER_HOUR, "icon": "mdi:water", "device_class": SensorDeviceClass.PRECIPITATION_INTENSITY, "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "rainfall_last_15_min", "unit": RAIN_COUNT, "icon": "mdi:water", "device_class": SensorDeviceClass.PRECIPITATION, "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "rain_rate_hi_last_15_min", "unit": RAIN_COUNT_PER_HOUR, "icon": "mdi:water", "device_class": SensorDeviceClass.PRECIPITATION_INTENSITY, "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "rainfall_last_60_min", "unit": RAIN_COUNT, "icon": "mdi:water", "device_class": SensorDeviceClass.PRECIPITATION, "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "rainfall_last_24_hr", "unit": RAIN_COUNT, "icon": "mdi:water", "device_class": SensorDeviceClass.PRECIPITATION, "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "rain_storm", "unit": RAIN_COUNT, "icon": "mdi:water", "device_class": SensorDeviceClass.PRECIPITATION, "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "rain_storm_start_at", "icon": "mdi:calendar", "device_class": SensorDeviceClass.TIMESTAMP, "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "solar_rad", "unit": UnitOfIrradiance.WATTS_PER_SQUARE_METER, "icon": "mdi:solar-power", "device_class": SensorDeviceClass.IRRADIANCE, "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "uv_index", "unit": "", "icon": "mdi:weather-sunny", "device_class": None, "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "rx_state", "unit": "", "icon": "mdi:signal", "device_class": None, "state_class": None},
        {"entity": "trans_battery_flag", "unit": "", "icon": "mdi:battery", "device_class": None, "state_class": None},
        {"entity": "rainfall_daily", "unit": RAIN_COUNT, "icon": "mdi:water", "device_class": SensorDeviceClass.PRECIPITATION, "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "rainfall_monthly", "unit": RAIN_COUNT, "icon": "mdi:water", "device_class": SensorDeviceClass.PRECIPITATION, "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "rainfall_year", "unit": RAIN_COUNT, "icon": "mdi:water", "device_class": SensorDeviceClass.PRECIPITATION, "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "rain_storm_last", "unit": RAIN_COUNT, "icon": "mdi:water", "device_class": SensorDeviceClass.PRECIPITATION, "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "rain_storm_last_start_at", "icon": "mdi:calendar", "device_class": SensorDeviceClass.TIMESTAMP, "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "rain_storm_last_end_at", "icon": "mdi:calendar", "device_class": SensorDeviceClass.TIMESTAMP, "state_class": STATE_CLASS_MEASUREMENT}
    ],
    3: [
        {"entity": "bar_sea_level", "unit": UnitOfPressure.INHG, "icon": "mdi:gauge", "device_class": SensorDeviceClass.ATMOSPHERIC_PRESSURE, "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "bar_trend", "unit": UnitOfPressure.INHG, "icon": "mdi:trending-down", "device_class": SensorDeviceClass.ATMOSPHERIC_PRESSURE, "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "bar_absolute", "unit": UnitOfPressure.INHG, "icon": "mdi:gauge", "device_class": SensorDeviceClass.ATMOSPHERIC_PRESSURE, "state_class": STATE_CLASS_MEASUREMENT}
    ],
    4: [
        {"entity": "temp_in", "unit": TEMP_FAHRENHEIT, "icon": "mdi:thermometer", "device_class": SensorDeviceClass.TEMPERATURE, "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "hum_in", "unit": PERCENTAGE, "icon": "mdi:water-percent", "device_class": SensorDeviceClass.HUMIDITY, "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "dew_point_in", "unit": TEMP_FAHRENHEIT, "icon": "mdi:weather-rainy", "device_class": SensorDeviceClass.TEMPERATURE, "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "heat_index_in", "unit": TEMP_FAHRENHEIT, "icon": "mdi:weather-sunny", "device_class": SensorDeviceClass.TEMPERATURE, "state_class": STATE_CLASS_MEASUREMENT}
    ],
    6: [
        {"entity": "temp", "unit": TEMP_FAHRENHEIT, "icon": "mdi:thermometer", "device_class": SensorDeviceClass.TEMPERATURE, "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "hum", "unit": PERCENTAGE, "icon": "mdi:water-percent", "device_class": SensorDeviceClass.HUMIDITY, "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "dew_point", "unit": TEMP_FAHRENHEIT, "icon": "mdi:weather-rainy", "device_class": SensorDeviceClass.TEMPERATURE, "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "wet_bulb", "unit": TEMP_FAHRENHEIT, "icon": "mdi:water", "device_class": SensorDeviceClass.TEMPERATURE, "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "heat_index", "unit": TEMP_FAHRENHEIT, "icon": "mdi:weather-sunny", "device_class": SensorDeviceClass.TEMPERATURE, "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "pm_1_last", "unit": CONCENTRATION_MICROGRAMS_PER_CUBIC_METER, "icon": "mdi:air-filter", "device_class": SensorDeviceClass.PM1, "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "pm_2p5_last", "unit": CONCENTRATION_MICROGRAMS_PER_CUBIC_METER, "icon": "mdi:air-filter", "device_class": SensorDeviceClass.PM25, "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "pm_10_last", "unit": CONCENTRATION_MICROGRAMS_PER_CUBIC_METER, "icon": "mdi:air-filter", "device_class": SensorDeviceClass.PM10, "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "pm_1", "unit": CONCENTRATION_MICROGRAMS_PER_CUBIC_METER, "icon": "mdi:air-filter", "device_class": SensorDeviceClass.PM1, "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "pm_2p5", "unit": CONCENTRATION_MICROGRAMS_PER_CUBIC_METER, "icon": "mdi:air-filter", "device_class": SensorDeviceClass.PM25, "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "pm_2p5_last_1_hour", "unit": CONCENTRATION_MICROGRAMS_PER_CUBIC_METER, "icon": "mdi:air-filter", "device_class": SensorDeviceClass.PM25, "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "pm_2p5_last_3_hours", "unit": CONCENTRATION_MICROGRAMS_PER_CUBIC_METER, "icon": "mdi:air-filter", "device_class": SensorDeviceClass.PM25, "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "pm_2p5_last_24_hours", "unit": CONCENTRATION_MICROGRAMS_PER_CUBIC_METER, "icon": "mdi:air-filter", "device_class": SensorDeviceClass.PM25, "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "pm_2p5_nowcast", "unit": CONCENTRATION_MICROGRAMS_PER_CUBIC_METER, "icon": "mdi:air-filter", "device_class": SensorDeviceClass.PM25, "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "pm_10", "unit": CONCENTRATION_MICROGRAMS_PER_CUBIC_METER, "icon": "mdi:air-filter", "device_class": SensorDeviceClass.PM10, "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "pm_10_last_1_hour", "unit": CONCENTRATION_MICROGRAMS_PER_CUBIC_METER, "icon": "mdi:air-filter", "device_class": SensorDeviceClass.PM10, "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "pm_10_last_3_hours", "unit": CONCENTRATION_MICROGRAMS_PER_CUBIC_METER, "icon": "mdi:air-filter", "device_class": SensorDeviceClass.PM10, "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "pm_10_last_24_hours", "unit": CONCENTRATION_MICROGRAMS_PER_CUBIC_METER, "icon": "mdi:air-filter", "device_class": SensorDeviceClass.PM10, "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "pm_10_nowcast", "unit": CONCENTRATION_MICROGRAMS_PER_CUBIC_METER, "icon": "mdi:air-filter", "device_class": SensorDeviceClass.PM10, "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "last_report_time", "unit": TIME_SECONDS, "icon": "mdi:clock-outline", "device_class": SensorDeviceClass.TIMESTAMP, "state_class": None},
        {"entity": "pct_pm_data_last_1_hour", "unit": PERCENTAGE, "icon": "mdi:chart-bar", "device_class": None, "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "pct_pm_data_last_3_hours", "unit": PERCENTAGE, "icon": "mdi:chart-bar", "device_class": None, "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "pct_pm_data_nowcast", "unit": PERCENTAGE, "icon": "mdi:chart-bar", "device_class": None, "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "pct_pm_data_last_24_hours", "unit": PERCENTAGE, "icon": "mdi:chart-bar", "device_class": None, "state_class": STATE_CLASS_MEASUREMENT},
    ]
}