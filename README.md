## inky-weather

Simple scripts for displaying National Weather Service forecasts on Inky WHAT and PHAT e-ink displays.

<p align="center"><img src='https://github.com/klarrieu/inky-weather/blob/main/inky-weather-example.jpg' width="400"></img></p>

## Setup

1. Clone this repository and navigate to its directory:
```
git clone https://github.com/klarrieu/inky-weather.git
cd inky-weather
```

2. Install [`inky`](https://github.com/pimoroni/inky) and/or [`inkyphat-mods`](https://github.com/mattdesl/inkyphat-mods) (recommended to update the display more quickly):
```
pip3 install inky[rpi,example-depends]
git clone https://github.com/mattdesl/inkyphat-mods.git
```

3. Make a `user_config.txt` text file (can modify `user_config_example.txt`) with your email ([for NWS API headers](https://www.weather.gov/documentation/services-web-api)) and desired forecast location `(lat, lon)`:

```
user_email: 'username@example.com'
location: (39.123, -120.456)
```

## Examples

- `weather.py`: Retrieves forecast and updates the display once. This script can be scheduled to run periodically e.g. using `crontab`.
- `weather-continuous.py`: Cycles through detailed forecasts and periodically updates. Can also be scheduled to run continuously from boot with `crontab`.
- `WeatherScreen.py`: Contains class definition used to manage retrieving forecast and updating the display.

## Issues

If have any issues using this, or want to add features, feel free to open an [issue](https://github.com/klarrieu/inky-weather/issues) and reach out to me.
