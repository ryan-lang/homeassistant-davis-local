import logging
from pathlib import Path
import json
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.components.sensor import STATE_CLASS_MEASUREMENT
from homeassistant.const import (
    UnitOfLength,
    UnitOfVolumetricFlux,
)
from homeassistant.components.sensor.const import (
    SensorDeviceClass
)

from . import DOMAIN
from .aqi_algorithms import ALGORITHMS as AQI_ALGORITHMS
from .data_structure_types import (
    RAIN_COUNT,
    RAIN_COUNT_PER_HOUR,
    DATA_STRUCTURE_ENTITIES
)

_LOGGER = logging.getLogger(__name__)

def find_condition_by_lsid(conditions, lsid):
    return next((condition for condition in conditions if condition.get('lsid') == lsid), None)

def find_rain_size_by_lsid(conditions, lsid):
    condition = find_condition_by_lsid(conditions, lsid)
    if condition:
        return condition.get("rain_size", None)
    return None

def get_rain_unit(coordinator, lsid, unit):
    conditions = coordinator.data.get("data", {}).get("conditions", [])
    rain_size = find_rain_size_by_lsid(conditions, lsid)
    if rain_size == 1 or rain_size == 4:
        if unit == RAIN_COUNT_PER_HOUR:
            return UnitOfVolumetricFlux.INCHES_PER_HOUR
        elif unit == RAIN_COUNT:
            return UnitOfLength.INCHES
    elif rain_size == 2 or rain_size == 3:
        if unit == RAIN_COUNT_PER_HOUR:
            return UnitOfVolumetricFlux.MILLIMETERS_PER_HOUR
        elif unit == RAIN_COUNT:
            return UnitOfLength.MILLIMETERS
    
    return None

def get_rain_lambda(coordinator, lsid):
    conditions = coordinator.data.get("data", {}).get("conditions", [])
    rain_size = find_rain_size_by_lsid(conditions, lsid)
    if rain_size == 1:
        return lambda x: x * 0.01
    elif rain_size == 2:
        return lambda x: x * 0.2
    elif rain_size == 3:
        return lambda x: x * 0.1
    elif rain_size == 4:
        return lambda x: x * 0.001
    
    return lambda x: x

# TODO: obviously this is dumb, but I haven't been able 
# to find how to load translations from a custom component,
# so that an interpolated entity name can still benefit from translations.
# this seemed like the easiest way to have some drop-in replacement in the future
def load_sensor_translations():
    json_file_path = Path(__file__).parent / "translations" / "en.json"
    with json_file_path.open('r') as f:
        data = json.load(f)
    return data.get("entity", {}).get("sensor", {})

class DavisSensor(CoordinatorEntity, SensorEntity):
    _attr_has_entity_name = True
    
    def __init__(self, coordinator, device_info, lsid, lsid_label, entity_config):
        super().__init__(coordinator)
        self._device_info = device_info
        self._lsid = lsid
        self._lsid_label = lsid_label
        self._entity_config = entity_config
        self._state = None

    @property
    def name(self):
        if self._lsid_label is None:
            return self._entity_config.get("entity_translation")
        else:
            return f"{self._entity_config.get('entity_translation')} {self._lsid_label}"
    
    @property
    def unique_id(self):
        domain, device_id = next(iter(self._device_info['identifiers']))
        return f"{device_id}_{self._lsid}_{self._entity_config['entity']}"

    @property
    def state(self):
        conditions = self.coordinator.data.get("data", {}).get("conditions", [])
        condition = find_condition_by_lsid(conditions, self._lsid)
        return condition.get(self._entity_config['entity']) if condition else None

    @property
    def extra_state_attributes(self):
        attributes = {"lsid": self._lsid}
        conditions = self.coordinator.data.get("data", {}).get("conditions", [])
        condition = find_condition_by_lsid(conditions, self._lsid)
        if condition:
            txid = condition.get("txid", None)
            if txid is not None:
                attributes["txid"] = txid

        return attributes
    
    @property
    def native_value(self):
        unit = self._entity_config.get("unit")

        # special unit handling for rain, where units are
        # specified in the rain_size field
        if unit == RAIN_COUNT_PER_HOUR or unit == RAIN_COUNT:
            return get_rain_lambda(self.coordinator, self._lsid)(self.state)
        else:
            return self.state

    @property
    def unit_of_measurement(self):
        unit = self._entity_config.get("unit")

        # special unit handling for rain, where units are
        # specified in the rain_size field
        if unit == RAIN_COUNT_PER_HOUR or unit == RAIN_COUNT:
            return get_rain_unit(self.coordinator, self._lsid, unit)
        else:
            return unit

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
    def __init__(self, coordinator, device_info, lsid, lsid_label, entity_config, aqi_algorithm):
        super().__init__(coordinator, device_info, lsid, lsid_label, entity_config)
        self._aqi_algorithm = aqi_algorithm

    @property
    def state(self):
        conditions = self.coordinator.data.get("data", {}).get("conditions", [])
        condition = find_condition_by_lsid(conditions, self._lsid)
        aqi_class = AQI_ALGORITHMS.get(self._aqi_algorithm, AQI_ALGORITHMS["EPA_USA"])['class']
        
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
        "configuration_url": f"http://{config_entry.data['host']}/v1/current_conditions",
    }

    _LOGGER.debug("Setting up entities for %s", device_name)
    _LOGGER.debug("Coordinator data: %s", coordinator.data)

    sensor_translations = load_sensor_translations()

    entities = []
    for condition in coordinator.data.get("data", {}).get("conditions", []):
        lsid = condition["lsid"]
        data_structure_type = condition.get("data_structure_type", 0)
        lsid_label = config_entry.data.get("lsid_labels", {}).get(str(lsid), None)

        _LOGGER.debug("Processing condition with lsid: %s (label=%s) and data_structure_type: %s", lsid, lsid_label, data_structure_type)

        for entity_config in DATA_STRUCTURE_ENTITIES.get(data_structure_type, []):

            # validate that the entity has a value in our payload before initializing
            if entity_config['entity'] not in condition:
                _LOGGER.debug("Skipping entity %s because it is not present in the payload for lsid %s", entity_config['entity'], lsid)
            else:
                entity_config['entity_translation'] = sensor_translations.get(entity_config['entity'], {}).get("name", entity_config['entity'])

                _LOGGER.debug("Creating entity for config: %s", entity_config)
                entities.append(DavisSensor(coordinator, device_info, lsid, lsid_label, entity_config))

        # Airlink (dst = 6) can compute AQI
        if data_structure_type == 6:
            aqi_algorithm = config_entry.data.get('aqi_algorithm', 'EPA_USA')  # Default to EPA_USA
            entities.append(DavisAQISensor(coordinator, device_info, lsid, lsid_label, {
                'entity': 'nowcast_aqi',
                "friendly_name": "Nowcast AQI",
                "icon": "mdi:air-filter", 
                "device_class": SensorDeviceClass.AQI, 
                "unit": "",
                "state_class": STATE_CLASS_MEASUREMENT}, aqi_algorithm))

    async_add_entities(entities)
