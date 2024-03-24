import os, sys
try:
    sys.path.append('./inkyphat-mods/src')
    import inky_mod as inky
except:
    print('WARNING: inkyphat-mods not found. Cannot use fast screen updates.')
    import inky
import requests
from PIL import Image, ImageDraw, ImageFont
import time


#TODO: show weather alerts for location (if any are in place)


def getsize(font, text):
    _, _, right, bottom = font.getbbox(text)
    return (right, bottom)


def wrap(quote, width, font):
    words = quote.split(" ")
    reflowed = ''
    line_length = 0

    for i in range(len(words)):
        word = words[i] + " "
        word_length = getsize(font, word)[0]
        line_length += word_length

        if line_length < width:
            reflowed += word
        else:
            line_length = word_length
            reflowed = reflowed[:-1] + "\n" + word

    reflowed = reflowed.rstrip()
    return reflowed


class WeatherScreen:
    def __init__(self, location, headers):
        self.location = location
        self.headers = headers
        self.forecast_endpoint = None
        self.hourly_forecast_endpoint = None
        self.weekly_forecast = None
        self.hourly_forecast = None
        self.periods = None
        self.display = inky.InkyWHAT('red')
        self.img = Image.new("P", self.display.resolution)

    def get_endpoints(self):
        r = requests.get(f'https://api.weather.gov/points/{self.location[0]},{self.location[1]}/', headers=self.headers)
        # query lat, lon of desired forecast location, returns forecast endpoints at grid cells for for local NWS office's forecast model
        properties = r.json()['properties']
        forecast_endpoint = properties['forecast']
        hourly_forecast_endpoint = properties['forecastGridData']
        print(f"endpoints: {forecast_endpoint}, {hourly_forecast_endpoint}")
        self.forecast_endpoint = forecast_endpoint
        self.hourly_forecast_endpoint = hourly_forecast_endpoint
        return forecast_endpoint, hourly_forecast_endpoint

    def get_weekly_forecast(self):
        """Retrieve 7-day forecast from NWS API"""
        print('Retrieving 7-day forecast')
        if not self.forecast_endpoint:
            raise IOError('No endpoints set. Run self.get_endpoints() first.')
        r = requests.get(self.forecast_endpoint, headers=self.headers)
        print(r.status_code)
        if r.status_code != 200:
            print(r.text)
        forecast = r.json()
        return forecast

    def get_hourly_forecast(self):
        """Retrieve hourly forecast from NWS API"""
        print('Retrieving hourly forecast')
        if not self.hourly_forecast_endpoint:
            raise IOError('No endpoints set. Run self.get_endpoints() first.')
        r = requests.get(self.hourly_forecast_endpoint, headers=self.headers)
        print(r.status_code)
        forecast = r.json()
        return forecast

    def update_forecasts(self):
        """Get endpoints (in case changed) and update forecast attributes"""
        self.get_endpoints()
        self.weekly_forecast = self.get_weekly_forecast()
        self.hourly_forecast = self.get_hourly_forecast()
        self.periods = [self.weekly_forecast['properties']['periods'][i] for i in range(14)]
        return

    def get_nws_icon(self, icon_url, icon_size=127):
        # get NWS icon
        icon = Image.open(requests.get(icon_url.replace('medium', 'large'), stream=True).raw)
        icon = icon.resize((icon_size, icon_size), resample=Image.Resampling.BICUBIC)
        # convert icon to red/black/white color palette
        pal_img = Image.new("P", (1, 1))
        pal_img.putpalette((255, 255, 255, 0, 0, 0, 255, 0, 0) + (0, 0, 0) * 252)
        icon = icon.convert("RGB").quantize(palette=pal_img)
        return icon

    def make_image(self, frame_i=0, hpad=5, vpad=5, h=15, large_font=17, small_font=14):
        """
        hpad, vpad: horizontal and vertical padding
        h: text height
        """
        # initialize image and drawing/text display
        self.img = Image.new("P", self.display.resolution)
        draw = ImageDraw.Draw(self.img)
        font = ImageFont.truetype("FreeSansBold", large_font)
        small_font = ImageFont.truetype("FreeSansBold", small_font)
        # add icons, short forecast for next 3 forecast periods
        for i, period in enumerate(self.periods[:3]):
            # place icon
            icon_size = 127
            icon = self.get_nws_icon(period['icon'], icon_size=icon_size)
            self.img.paste(icon, (hpad * (i + 1) + icon.width * i, vpad + h))
            # place period name
            message = period['name']
            draw.text((hpad * (i + 1) + icon.width * (i + 0.5), vpad), message, self.display.BLACK, font, anchor='mt')
            # place short forecast
            message = wrap(period['shortForecast'], icon_size, small_font)
            # cut to two lines if longer
            if len(message.split("\n")) > 2:
                message = "\n".join(message.split("\n")[:2])
            bbox = draw.textbbox((0, 0), message, small_font)
            draw.text((hpad * (i + 1) - bbox[2]//2 + icon.width * (i + 0.5), vpad + h + icon.height), message, self.display.BLACK, small_font, align='center')
            # place temp for high/low
            message = f"{period['temperature']} °{period['temperatureUnit']}"
            draw.text((hpad * (i + 1) + icon.width * (i + 0.5), 2 * vpad + 3 * h + icon.height), message, self.display.BLACK, font, anchor='mt')

        # add text for detailed forecast
        font = ImageFont.truetype("FreeSansBold", 16)
        x, y = 5, 205
        message = wrap(f"{self.periods[frame_i]['name']}: {self.periods[frame_i]['detailedForecast']}", self.display.width - 10, font)
        draw.text((x, y), message, self.display.BLACK, font)
        bbox = draw.textbbox((x, y), message, font)
        y = bbox[-1]
        return self.img

    def update_screen(self, fast=True, *args, **kwargs):
        # make image
        self.make_image(*args, **kwargs)
        # write to display and update
        self.img.save('weather_image.png')
        self.display.set_image(self.img)
        if fast:
            self.display.fast_show(style=self.display.BLACK)
        else:
            self.display.show() # busy_wait=False)
        return
