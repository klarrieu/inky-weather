#!/bin/python
from WeatherScreen import WeatherScreen
import time


if __name__ == "__main__":
    # read user config file
    with open('user_config.txt') as f:
        lines = f.read().splitlines()
        config = dict([line.split(':') for line in lines])
        email = eval(config['user_email'])
        location = eval(config['location'])
    # URL headers for requests to NWS API
    headers = {'User-Agent': f'weather display,{email}', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'}

    # time to get new forecast from NWS API
    update_time = 60 * 15  # 15 minutes
    # time to cycle through each detailed forecast
    cycle_time = 15  # 15 seconds

    # initialize WeatherScreen object
    ws = WeatherScreen(location=location, headers=headers)
    ws.update_forecasts()
    ws.update_screen(fast=False)
    #
    t0 = time.time()
    while True:
        if time.time() - t0 > update_time:
            ws.update_forecasts()
            t0 = time.time()
        for frame_i in range(3):
            ws.update_screen(frame_i=frame_i, fast=True)
            time.sleep(cycle_time)
