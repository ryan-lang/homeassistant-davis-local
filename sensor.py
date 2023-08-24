import logging
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
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
        {"entity": "temp", "unit": TEMP_FAHRENHEIT, "icon": "mdi:thermometer", "device_class": "temperature"},
        {"entity": "hum", "unit": PERCENTAGE, "icon": "mdi:water-percent", "device_class": "humidity"},
        {"entity": "dew_point", "unit": TEMP_FAHRENHEIT, "icon": "mdi:weather-rainy", "device_class": "temperature"},
        # Add more here...
    ],
    # Add more data_structure_types here if needed
}

class DavisSensor(CoordinatorEntity, Entity):
    def __init__(self, coordinator, device_name, lsid, entity_config):
        super().__init__(coordinator)
        self._name = f"{device_name} {lsid} {entity_config['entity']}"
        self._lsid = lsid
        self._entity_config = entity_config
        self._state = None

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self.coordinator.data.get("data", {}).get("conditions", [{}])[0].get(self._entity_config['entity'])

    @property
    def unit_of_measurement(self):
        return self._entity_config.get("unit")

    @property
    def icon(self):
        return self._entity_config.get("icon")

    @property
    def device_class(self):
        return self._entity_config.get("device_class")

async def async_setup_entry(hass, config_entry, async_add_entities):
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    device_name = config_entry.title

    _LOGGER.debug("Setting up entities for %s", device_name)
    _LOGGER.debug("Coordinator data: %s", coordinator.data)

    entities = []
    for condition in coordinator.data.get("data", {}).get("conditions", []):
        lsid = condition["lsid"]
        data_structure_type = condition.get("data_structure_type", 0)
        
        _LOGGER.debug("Processing condition with lsid: %s and data_structure_type: %s", lsid, data_structure_type)

        for entity_config in DATA_STRUCTURE_ENTITIES.get(data_structure_type, []):
            _LOGGER.debug("Creating entity for config: %s", entity_config)
            entities.append(DavisSensor(coordinator, device_name, lsid, entity_config))

    async_add_entities(entities)
