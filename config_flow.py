import logging
from homeassistant import config_entries
from homeassistant.core import callback
import voluptuous as vol

from . import async_fetch_data, DOMAIN  # Import from __init__.py

_LOGGER = logging.getLogger(__name__)

class DavisInstrumentsConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Davis Instruments."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""

        errors = {}

        if user_input is not None:
            host = user_input["host"]

            # Validate the host by attempting to fetch data
            try:
                await async_fetch_data(host)
            except Exception:
                errors["base"] = "cannot_connect"
            else:
                # Assuming unique ID is formed by host
                await self.async_set_unique_id(host)
                self._abort_if_unique_id_configured()

                return self.async_create_entry(title=host, data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required("host"): str,
                }
            ),
            errors=errors,
        )
