from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.const import (
    TEMP_FAHRENHEIT,
    PERCENTAGE,
    DEGREE,
    CONCENTRATION_MICROGRAMS_PER_CUBIC_METER
)

from . import DOMAIN

DATA_STRUCTURE_TYPE_6 = {
    "temp": {"unit": TEMP_FAHRENHEIT, "icon": "mdi:thermometer", "device_class": "temperature"},
    "hum": {"unit": PERCENTAGE, "icon": "mdi:water-percent", "device_class": "humidity"},
    "dew_point": {"unit": TEMP_FAHRENHEIT, "icon": "mdi:weather-fog", "device_class": "temperature"},
    "wet_bulb": {"unit": TEMP_FAHRENHEIT, "icon": "mdi:water", "device_class": "temperature"},
    "heat_index": {"unit": TEMP_FAHRENHEIT, "icon": "mdi:thermometer-alert", "device_class": "temperature"},
    "pm_1_last": {"unit": CONCENTRATION_MICROGRAMS_PER_CUBIC_METER, "icon": "mdi:air-filter", "device_class": None},
    # Add other entities for data_structure_type 6 here...
}

class DavisSensor(CoordinatorEntity, Entity):
    def __init__(self, coordinator, device_name, lsid, entity_type, attributes):
        super().__init__(coordinator)
        self._name = f"{device_name} {lsid} {entity_type}"
        self._lsid = lsid
        self._entity_type = entity_type
        self._attributes = attributes
        self._state = None

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        conditions = [condition for condition in self.coordinator.data.get("data", {}).get("conditions", []) if condition["lsid"] == self._lsid]
        if conditions:
            return conditions[0].get(self._entity_type)
        return None

    @property
    def unit_of_measurement(self):
        return self._attributes.get("unit")

    @property
    def icon(self):
        return self._attributes.get("icon")

    @property
    def device_class(self):
        return self._attributes.get("device_class")

async def async_setup_entry(hass, config_entry, async_add_entities):
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    device_name = config_entry.title

    entities = []
    for condition in coordinator.data.get("data", {}).get("conditions", []):
        lsid = condition["lsid"]
        data_structure_type = condition.get("data_structure_type")

        if data_structure_type == 6:  # The type you specified
            for entity_type, attributes in DATA_STRUCTURE_TYPE_6.items():
                if entity_type in condition:
                    entities.append(DavisSensor(coordinator, device_name, lsid, entity_type, attributes))

    async_add_entities(entities)
