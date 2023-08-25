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

                # set device name if provided
                self.device_name = self.data["data"].get("name")

                # determine if we have any Airlink data
                self.has_airlink = any(cond["data_structure_type"] == 6 for cond in self.data["data"]["conditions"])
                self.aqi_algorithm = None

                # determine if we have any duplicate data_structure_types
                duplicate_structure_types = defaultdict(list)
                for condition in self.data["data"]["conditions"]:
                    duplicate_structure_types[condition["data_structure_type"]].append(condition["lsid"])
                self.duplicates = {k: v for k, v in duplicate_structure_types.items() if len(v) > 1}
                self.labels = {}

            except Exception:
                errors["base"] = "cannot_connect"
            else:
                # begin the remaining flow
                return await self.async_device_name()

        return self.async_show_form(step_id='user', data_schema=vol.Schema(schema), errors=errors)

    async def async_device_name(self, user_input=None):
        if self.device_name:
            _LOGGER.debug("Device name provided in fetch data: %s", self.device_name)
            await self.async_set_unique_id(self.device_name)
            self._abort_if_unique_id_configured()
            return await self.async_airlink()
        else:
            _LOGGER.debug("Device name not provided in fetch data, prompting user for device name...")
            return await self.async_step_device_name()

    async def async_airlink(self, user_input=None):
        if not self.has_airlink:
            _LOGGER.debug("Device does not support AQI, skipping AQI step...")
            return await self.async_lsid_labels()
        else:
            _LOGGER.debug("Device supports AQI, prompting user for AQI algorithm...")
            return await self.async_step_airlink()

    async def async_lsid_labels(self, user_input=None):
        if len(self.duplicates) == 0:
            _LOGGER.debug("No duplicate data_structure_types, skipping LSID label step...")
            return await self.async_complete_flow()
        else:
            _LOGGER.debug("Duplicate data_structure_types detected, prompting user for LSID labels...")
            return await self.async_step_lsid_labels()

    async def async_complete_flow(self):
        return self.async_create_entry(
            title=self.device_name,
            data={
                "host": self.host, 
                "aqi_algorithm": self.aqi_algorithm, 
                "lsid_labels": self.labels
            }
        )
    
    async def async_step_device_name(self, user_input=None):
        errors = {}
        schema = OrderedDict()
        schema[vol.Required('device_name')] = str

        if user_input is not None:
            self.device_name = user_input["device_name"]
            _LOGGER.debug("Device name provided by user: %s", self.device_name)
            await self.async_set_unique_id(self.device_name)
            self._abort_if_unique_id_configured()
            return await self.async_airlink()

        return self.async_show_form(step_id='device_name', data_schema=vol.Schema(schema), errors=errors)

    async def async_step_airlink(self, user_input=None):
        errors = {}
        schema = OrderedDict()

        supported_algorithms = {v['friendly_name']: k for k, v in AQI_ALGORITHMS.items()}
        schema[vol.Optional('aqi_algorithm', default='EPA_USA')] = vol.In(supported_algorithms)  # Make this Optional

        if user_input is not None:
            self.aqi_algorithm = user_input.get("aqi_algorithm", None)
            return await self.async_lsid_labels()

        return self.async_show_form(step_id='airlink', data_schema=vol.Schema(schema), errors=errors)

    async def async_step_lsid_labels(self, user_input=None):
        errors = {}
        schema = OrderedDict()

        # Generate schema fields for duplicates
        for data_structure_type, lsids in self.duplicates.items():
            for lsid in lsids:
                schema[vol.Required(f"label_{lsid}", default=f"Sensor {lsid}")] = str

        if user_input is not None:
            self.labels = {key.replace("label_", ""): value for key, value in user_input.items()}
            return await self.async_complete_flow()

        return self.async_show_form(step_id='lsid_labels', data_schema=vol.Schema(schema), errors=errors)

            
