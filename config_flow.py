from collections import OrderedDict,defaultdict
import logging
import voluptuous as vol
from homeassistant import config_entries

from . import async_fetch_data, DOMAIN
from .aqi_algorithms import ALGORITHMS as AQI_ALGORITHMS

_LOGGER = logging.getLogger(__name__)

class DavisInstrumentsConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None):
        errors = {}
        schema = OrderedDict()
        schema[vol.Required('host')] = str

        if user_input is not None:
            self.host = user_input["host"]
            try:
                self.data = await async_fetch_data(self.host)
                self.device_name = self.data["data"].get("name")
            except Exception:
                errors["base"] = "cannot_connect"
            else:
                if self.device_name:
                    _LOGGER.debug("Device name provided in fetch data: %s", self.device_name)
                    await self.async_set_unique_id(self.device_name)
                    self._abort_if_unique_id_configured()
                    return await self.async_step_aqi()
                else:
                    _LOGGER.debug("Device name not provided in fetch data, prompting user for device name...")
                    return await self.async_step_device_name()

        return self.async_show_form(step_id='user', data_schema=vol.Schema(schema), errors=errors)
    
    async def async_step_device_name(self, user_input=None):
        errors = {}
        schema = OrderedDict()
        schema[vol.Required('device_name')] = str

        if user_input is not None:
            self.device_name = user_input["device_name"]
            _LOGGER.debug("Device name provided by user: %s", self.device_name)
            await self.async_set_unique_id(self.device_name)
            self._abort_if_unique_id_configured()
            return await self.async_step_aqi()

        return self.async_show_form(step_id='device_name', data_schema=vol.Schema(schema), errors=errors)
    
    async def async_step_aqi(self, user_input=None):
        errors = {}
        schema = OrderedDict()

        # Check for duplicate data_structure_types
        duplicate_structure_types = defaultdict(list)
        for condition in self.data["data"]["conditions"]:
            duplicate_structure_types[condition["data_structure_type"]].append(condition["lsid"])

        self.duplicates = {k: v for k, v in duplicate_structure_types.items() if len(v) > 1}
        _LOGGER.debug("Duplicate data_structure_types: %s", self.duplicates)

        # Check if any conditions object has data_structure_type = 6
        if any(cond["data_structure_type"] == 6 for cond in self.data["data"]["conditions"]):
            _LOGGER.debug("Device supports AQI, prompting user for AQI algorithm...")
            supported_algorithms = {v['friendly_name']: k for k, v in AQI_ALGORITHMS.items()}
            schema[vol.Optional('aqi_algorithm', default='EPA_USA')] = vol.In(supported_algorithms)  # Make this Optional

        if user_input is not None:
            self.aqi_algorithm = user_input.get("aqi_algorithm", None)
            if self.duplicates:
                return await self.async_step_label()
            else:
                return self.async_create_entry(
                    title=self.device_name, 
                    data={"host": self.host, "aqi_algorithm": self.aqi_algorithm}
                )

        return self.async_show_form(step_id='aqi', data_schema=vol.Schema(schema), errors=errors)

    async def async_step_label(self, user_input=None):
        errors = {}
        schema = OrderedDict()

        # Generate schema fields for duplicates
        for data_structure_type, lsids in self.duplicates.items():
            for lsid in lsids:
                schema[vol.Required(f"label_{lsid}", default=f"Sensor {lsid}")] = str

        if user_input is not None:
            labels = {key.replace("label_", ""): value for key, value in user_input.items()}
            return self.async_create_entry(
                title=self.data["data"]["name"],
                data={"host": self.host, "aqi_algorithm": self.aqi_algorithm, "labels": labels}
            )

        return self.async_show_form(step_id='label', data_schema=vol.Schema(schema), errors=errors)