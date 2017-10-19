# EnvIO
EnvIO attempts to be a generic solution for interfacing various peripherals to the Raspberry Pi running OctoPrint. Beside user-friendly management and configuration of external sensors and output devices, soon* EnvIO will provide an interface for managing output devices behaviour through logical and arithmetic equations utilizing input from the sensors and OctoPrint itself.

For example, below equations would turn on a fan if temperature surpasses 40°C degrees and shut down power if either temperature reaches 80°C or smoke is detected:
> ### Example:
> relay_fan := temperature_sensor > 40 
> 
> relay_power := temperature_sensor < 80 AND NOT smoke_sensor



---
*As for now it only supports DS18B20 temperature sensor and any kind of discrete sensors such as MQ2 smoke detector.

## Setup

Install via the bundled [Plugin Manager](https://github.com/foosel/OctoPrint/wiki/Plugin:-Plugin-Manager)
or manually using this URL:

    https://github.com/Styku/EnvIO/archive/master.zip

**TODO:** Describe how to install plugin.

## Configuration

**TODO:** Describe configuration.
