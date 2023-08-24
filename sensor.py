import logging
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.components.sensor import STATE_CLASS_MEASUREMENT
from homeassistant.const import (
    TEMP_FAHRENHEIT,
    PERCENTAGE,
    CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    TIME_SECONDS,
    DEVICE_CLASS_TIMESTAMP
)

from . import DOMAIN
from .aqi_algorithms import ALGORITHMS as AQI_ALGORITHMS

_LOGGER = logging.getLogger(__name__)

DATA_STRUCTURE_ENTITIES = {
    6: [
        {"entity": "temp", "friendly_name": "Temperature", "unit": TEMP_FAHRENHEIT, "icon": "mdi:thermometer", "device_class": "temperature", "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "hum", "friendly_name": "Humidity", "unit": PERCENTAGE, "icon": "mdi:water-percent", "device_class": "humidity", "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "dew_point", "friendly_name": "Dew Point", "unit": TEMP_FAHRENHEIT, "icon": "mdi:weather-rainy", "device_class": "temperature", "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "wet_bulb", "friendly_name": "Wet Bulb", "unit": TEMP_FAHRENHEIT, "icon": "mdi:water", "device_class": "temperature", "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "heat_index", "friendly_name": "Heat Index", "unit": TEMP_FAHRENHEIT, "icon": "mdi:weather-sunny", "device_class": "temperature", "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "pm_1_last", "friendly_name": "PM 1 Last", "unit": CONCENTRATION_MICROGRAMS_PER_CUBIC_METER, "icon": "mdi:air-filter", "device_class": None, "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "pm_2p5_last", "friendly_name": "PM 2.5 Last", "unit": CONCENTRATION_MICROGRAMS_PER_CUBIC_METER, "icon": "mdi:air-filter", "device_class": None, "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "pm_10_last", "friendly_name": "PM 10 Last", "unit": CONCENTRATION_MICROGRAMS_PER_CUBIC_METER, "icon": "mdi:air-filter", "device_class": None, "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "pm_1", "friendly_name": "PM 1", "unit": CONCENTRATION_MICROGRAMS_PER_CUBIC_METER, "icon": "mdi:air-filter", "device_class": None, "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "pm_2p5", "friendly_name": "PM 2.5", "unit": CONCENTRATION_MICROGRAMS_PER_CUBIC_METER, "icon": "mdi:air-filter", "device_class": None, "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "pm_2p5_last_1_hour", "friendly_name": "PM 2.5", "unit": CONCENTRATION_MICROGRAMS_PER_CUBIC_METER, "icon": "mdi:air-filter", "device_class": None, "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "pm_2p5_last_3_hours", "friendly_name": "PM 2.5", "unit": CONCENTRATION_MICROGRAMS_PER_CUBIC_METER, "icon": "mdi:air-filter", "device_class": None, "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "pm_2p5_last_24_hours", "friendly_name": "PM 2.5", "unit": CONCENTRATION_MICROGRAMS_PER_CUBIC_METER, "icon": "mdi:air-filter", "device_class": None, "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "pm_2p5_nowcast", "friendly_name": "PM 2.5", "unit": CONCENTRATION_MICROGRAMS_PER_CUBIC_METER, "icon": "mdi:air-filter", "device_class": None, "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "pm_10", "friendly_name": "PM 10", "unit": CONCENTRATION_MICROGRAMS_PER_CUBIC_METER, "icon": "mdi:air-filter", "device_class": None, "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "pm_10_last_1_hour", "friendly_name": "PM 2.5", "unit": CONCENTRATION_MICROGRAMS_PER_CUBIC_METER, "icon": "mdi:air-filter", "device_class": None, "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "pm_10_last_3_hours", "friendly_name": "PM 2.5", "unit": CONCENTRATION_MICROGRAMS_PER_CUBIC_METER, "icon": "mdi:air-filter", "device_class": None, "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "pm_10_last_24_hours", "friendly_name": "PM 2.5", "unit": CONCENTRATION_MICROGRAMS_PER_CUBIC_METER, "icon": "mdi:air-filter", "device_class": None, "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "pm_10_nowcast", "friendly_name": "PM 2.5", "unit": CONCENTRATION_MICROGRAMS_PER_CUBIC_METER, "icon": "mdi:air-filter", "device_class": None, "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "last_report_time", "friendly_name": "Last Report Time", "unit": TIME_SECONDS, "icon": "mdi:clock-outline", "device_class": DEVICE_CLASS_TIMESTAMP, "state_class": None},
        {"entity": "pct_pm_data_last_1_hour", "friendly_name": "PM Data Last 1 Hour (%)", "unit": PERCENTAGE, "icon": "mdi:chart-bar", "device_class": None, "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "pct_pm_data_last_3_hours", "friendly_name": "PM Data Last 3 Hours (%)", "unit": PERCENTAGE, "icon": "mdi:chart-bar", "device_class": None, "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "pct_pm_data_nowcast", "friendly_name": "PM Data Nowcast (%)", "unit": PERCENTAGE, "icon": "mdi:chart-bar", "device_class": None, "state_class": STATE_CLASS_MEASUREMENT},
        {"entity": "pct_pm_data_last_24_hours", "friendly_name": "PM Data Last 24 Hours (%)", "unit": PERCENTAGE, "icon": "mdi:chart-bar", "device_class": None, "state_class": STATE_CLASS_MEASUREMENT},
    ],
    # Add more data_structure_types here if needed
}

def find_condition_by_lsid(conditions, lsid):
    return next((condition for condition in conditions if condition.get('lsid') == lsid), None)

class DavisSensor(CoordinatorEntity, Entity):
    def __init__(self, coordinator, device_info, lsid, entity_config):
        super().__init__(coordinator)
        self._device_info = device_info
        self._lsid = lsid
        self._entity_config = entity_config
        self._state = None

    @property
    def unique_id(self):
        domain, device_id = next(iter(self._device_info['identifiers']))
        return f"{device_id}_{self._entity_config['entity']}"

    @property
    def name(self):
        return f"{self._device_info['name']} {self._entity_config['entity']}"

    @property
    def state(self):
        conditions = self.coordinator.data.get("data", {}).get("conditions", [])
        condition = find_condition_by_lsid(conditions, self._lsid)
        return condition.get(self._entity_config['entity']) if condition else None

    @property
    def device_state_attributes(self):
        attributes = {}
        conditions = self.coordinator.data.get("data", {}).get("conditions", [])
        condition = find_condition_by_lsid(conditions, self._lsid)
        if condition:
            lsid = condition.get("lsid", None)
            if lsid is not None:
                attributes["lsid"] = lsid
            
            txid = condition.get("txid", None)
            if txid is not None:
                attributes["txid"] = txid

        return attributes

    @property
    def unit_of_measurement(self):
        return self._entity_config.get("unit")

    @property
    def icon(self):
        return self._entity_config.get("icon")

    @property
    def device_class(self):
        return self._entity_config.get("device_class")
    
    @property
    def state_class(self):
        return self._entity_config.get("state_class")

    @property
    def device_info(self):
        return self._device_info
    
class DavisAQISensor(DavisSensor):
    def __init__(self, coordinator, device_info, lsid, entity_config, aqi_algorithm):
        super().__init__(coordinator, device_info, lsid, entity_config)
        self._aqi_algorithm = aqi_algorithm

    @property
    def state(self):
        conditions = self.coordinator.data.get("data", {}).get("conditions", [])
        condition = find_condition_by_lsid(conditions, self._lsid)
        aqi_class = AQI_ALGORITHMS.get(self._aqi_algorithm, "EPA_USA")['class']
        
        if condition:
            pm25 = condition.get("pm_2p5_nowcast", 0)
            pm10 = condition.get("pm_10_nowcast", 0)
            return aqi_class().calculate(pm25, pm10)
        return None
    
async def async_setup_entry(hass, config_entry, async_add_entities):
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    device_name = config_entry.title
    device_id = coordinator.data.get("data", {}).get("did", "unknown")

    device_info = {
        "identifiers": {(DOMAIN, device_id)},
        "name": device_name,
        "manufacturer": "Davis Instruments",
        # Additional fields can go here
    }

    _LOGGER.debug("Setting up entities for %s", device_name)
    _LOGGER.debug("Coordinator data: %s", coordinator.data)

    entities = []
    for condition in coordinator.data.get("data", {}).get("conditions", []):
        lsid = condition["lsid"]
        data_structure_type = condition.get("data_structure_type", 0)
        
        _LOGGER.debug("Processing condition with lsid: %s and data_structure_type: %s", lsid, data_structure_type)

        for entity_config in DATA_STRUCTURE_ENTITIES.get(data_structure_type, []):
            _LOGGER.debug("Creating entity for config: %s", entity_config)
            entities.append(DavisSensor(coordinator, device_info, lsid, entity_config))

        # Airlink (dst = 6) can compute AQI
        if data_structure_type == 6:
            aqi_algorithm = config_entry.data.get('aqi_algorithm', 'EPA_USA')  # Default to EPA_USA
            entities.append(DavisAQISensor(coordinator, device_info, lsid, {'entity': 'nowcast_aqi'}, aqi_algorithm))

    async_add_entities(entities)
