[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

# Davis Instruments Local Integration for Home Assistant

Provides an all-local polling integration for Davis Instruments devices, including WeatherLink and AirLink.

Currently only supports V1 of the WeatherLink API, data structures 1, 3, 4, and 6. Fetches from the /v1/current_conditions endpoint on your Davis device.

Tested on WeatherLink Live and Airlink.

## Installation

### HACS install

- Use HACS, add this repo as a custom repository and install Davis Local integration.
- Restart Home Assistant

### Manual install

- Clone this repository to custom_components/davis_local in your .homeassistant directory
- Restart Home Assistant

### Setup

After adding the Davis Local integration, you will be prompted for some setup steps.

* **Host** Can be hostname or IP address of your Davis device
* **Device Name** Only prompted if no name is present under data.name in your Davis payload
* **Airlink Setup** If the device is an Airlink (returns data_structure_type: 6, with air quality data), then you will be prompted for your preferred AQI Algorithm. Currently only supports US EPA.
* **Multi-Sensor Setup** If your device has multiple sensors of the same data type, you will be prompted to label each conflicting sensor. See **Multi-Sensor Setup** below.

#### Multi-Sensor Setup
Some Davis devices can receive conditions data from other transmitters, such as a Vantage Pro base station with an ancillary Sensor Transmitter. 
This is referred to as having two "Sensor Suites," and they may report identical conditions payloads, which can only be distinquished by the "lsid" (logical sensor ID) and "txid" (transmitter ID) fields.

Therefore, this integration will detect if two sensors conflict, and ask you to label them. By default, the LSID for each sensor is used, but it's reccomended that you label them something descriptive, such as "Main" and "Wind".

Sensors returning "null" field values will be assumed to not have that particular capability, and those entities will be omitted. However, some fields will be set to "0" even if they don't have that capability 
(such as rain totals on a non-rain collector). Further complicating matters, the base station may "inherit" data from other sensors, again creating a scenario where entities are duplicated.

Irrelevant, missing, or duplicate entities should be hidden manually by going to the entity configuration in Home Assistant, and untoggling "Visible."

## Additional documentation
[Weatherlink API V1 Documentation](https://weatherlink.github.io/weatherlink-live-local-api/)

## Similar Projects

If you're looking for a cloud-based WeatherLink integration, see the well-supported [Weatherlink Integration](https://github.com/astrandb/weatherlink) by astrandb, from which this project takes inspiration.

## TODO
- [ ] Figure out how translations can be used with custom LSID labels
- [ ] UDP real-time data support
- [ ] Support additional V1 data structures
- [ ] Support for WeatherLink API V2
- [ ] Configurable polling rate

## Disclaimer

The package and its author are not affiliated with Davis Instruments or Weatherlink. Use at your own risk.

## License

The package is released under the MIT license.
