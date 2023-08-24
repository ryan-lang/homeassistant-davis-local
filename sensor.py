import logging
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.components.sensor import STATE_CLASS_MEASUREMENT
from homeassistant.const import (
    TEMP_FAHRENHEIT,
    PERCENTAGE
    # DEGREE,
    # CONCENTRATION_MICROGRAMS_PER_CUBIC_METER
)

from . import DOMAIN

_LOGGER = logging.getLogger(__name__)

DATA_STRUCTURE_ENTITIES = {
    6: [
        {"entity": "temp", "unit": TEMP_FAHRENHEIT, "icon": "mdi:thermometer", "device_class": "temperature", "state_class":STATE_CLASS_MEASUREMENT},
        {"entity": "hum", "unit": PERCENTAGE, "icon": "mdi:water-percent", "device_class": "humidity", "state_class":STATE_CLASS_MEASUREMENT},
        {"entity": "dew_point", "unit": TEMP_FAHRENHEIT, "icon": "mdi:weather-rainy", "device_class": "temperature", "state_class":STATE_CLASS_MEASUREMENT},
        # Add more here...
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
        return f"{self._device_info['identifiers'][0]}_{self._entity_config['entity']}"

    @property
    def name(self):
        return f"{self._device_info['name']} {self._entity_config['entity']}"

    @property
    def state(self):
        conditions = self.coordinator.data.get("data", {}).get("conditions", [])
        condition = find_condition_by_lsid(conditions, self._lsid)
        return condition.get(self._entity_config['entity']) if condition else None

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

    async_add_entities(entities)
