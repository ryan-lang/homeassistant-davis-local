from datetime import timedelta
import logging

import aiohttp
import async_timeout
import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import aiohttp_client, update_coordinator

DOMAIN = "davis_instruments"
_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = vol.Schema({DOMAIN: vol.Schema({})}, extra=vol.ALLOW_EXTRA)

DEFAULT_SCAN_INTERVAL = timedelta(minutes=1)

async def async_fetch_data(host):
    """Fetch data from Davis Instruments endpoint."""
    url = f"http://{host}/your_endpoint_here"

    async with aiohttp.ClientSession() as session:
        try:
            async with async_timeout.timeout(10):
                async with session.get(url) as response:
                    return await response.json()
        except aiohttp.ClientError as err:
            _LOGGER.warning("Error fetching data: %s", err)
            raise update_coordinator.UpdateFailed("Error fetching data")

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Davis Instruments integration."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Davis Instruments from a config entry."""

    host = entry.data["host"]

    coordinator = update_coordinator.DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="Davis Instruments",
        update_method=lambda: async_fetch_data(host),
        update_interval=DEFAULT_SCAN_INTERVAL,
    )

    # Fetch initial data
    await coordinator.async_refresh()

    if not coordinator.last_update_success:
        return False

    hass.data[DOMAIN] = {
        "coordinator": coordinator,
    }

    # You would typically initialize your platforms here
    # hass.async_create_task(hass.config_entries.async_forward_entry_setup(entry, "sensor"))

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    # Remove the entry from the `hass.data` dict
    hass.data.pop(DOMAIN)

    return True
