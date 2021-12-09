# coding: utf-8

from datetime import datetime, timedelta
from flask import render_template
from app import app
import requests


cards = { 0: u"↑", 45: u"↗", 90: u"→", 135: u"↙", 180: u"↓", 225: u"↙", 270: u"←", 315: u"↗", 360: u"↑" }


@app.route('/weather/<location>', strict_slashes=False, methods=['GET'])
def index(location):

    try:
        geo_url = 'https://maps.googleapis.com/maps/api/geocode/json'
        params = {'key': app.config['GOOGLE_API_KEY'], 'address': location}
        geo = requests.get(geo_url, params=params).json()['results'][0]
    except:
        return "Google Geocoding API error, please try again in a few minutes."

    try:
        owm_url = 'https://api.openweathermap.org/data/2.5/onecall'
        params = {'lat': geo['geometry']['location']['lat'], 'lon': geo['geometry']['location']['lng'],
            'appid': app.config['OPENWEATHER_API_KEY'], 'exclude': 'minutely,hourly,daily', 'units': 'imperial', 'format': 'json'}
        weather = requests.get(owm_url, params=params).json()
    except:
        return "OpenWeather API error, please try again in a few minutes."

    try:
        direction = cards.get(float(weather['current']['wind_deg']),
            cards[min(cards.keys(), key=lambda k: abs(k - float(weather['current']['wind_deg'])))])

        return u"{current[temp]:.0f}\u00b0F({current[feels_like]:.0f}\u00b0F) " \
            u"{current[weather][0][description]} {direction}{current[wind_speed]:.0f}MPH " \
            u"{current[humidity]:.0f}%".format(direction=direction, **weather)
    except:
        return "Error: unable to find weather data for location."

