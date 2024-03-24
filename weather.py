#!/bin/python
from WeatherScreen import WeatherScreen


if __name__ == "__main__":
    # read user config file
    with open('user_config.txt') as f:
        lines = f.read().splitlines()
        config = dict([line.split(':') for line in lines])
        email = eval(config['user_email'])
        location = eval(config['location'])
    # URL headers for requests to NWS API
    headers = {'User-Agent': f'weather display,{email}', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'}

    ws = WeatherScreen(location=location, headers=headers)
    ws.update_forecasts()
    ws.update_screen(fast=True)
