# coding: utf-8

from app import app, cache
import requests


cards = { 0: u"↓", 45: u"↙", 90: u"←", 135: u"↖", 180: u"↑", 225: u"↗", 270: u"→", 315: u"↘", 360: u"↓" }

@app.route('/weather/<location>', strict_slashes=False, methods=['GET'])
@cache.memoize(300)
def index(location):
    try:
        geo_url = 'https://maps.googleapis.com/maps/api/geocode/json'
        params = {'key': app.config['GOOGLE_API_KEY'], 'address': location}
        geo = requests.get(geo_url, params=params).json()['results'][0]
    except Exception as e:
        print(e)
        return "Google Geocoding API error"

    try:
        owm_url = 'https://api.openweathermap.org/data/2.5/onecall'
        params = {'lat': geo['geometry']['location']['lat'], 'lon': geo['geometry']['location']['lng'], 'format': 'json',
            'appid': app.config['OPENWEATHER_API_KEY'], 'exclude': 'minutely,hourly,daily', 'units': 'imperial'}
        weather = requests.get(owm_url, params=params).json()
    except Exception as e:
        print(e)
        return "OpenWeatherMap API error"

    try:
        direction = cards.get(float(weather['current']['wind_deg']),
            cards[min(cards.keys(), key=lambda k: abs(k - float(weather['current']['wind_deg'])))])

        weather['current']['weather'][0]['description'] = weather['current']['weather'][0]['description'].replace('intensity ', '')
        weather['current']['wind_gust'] = weather['current'].get('wind_gust', weather['current']['wind_speed'])

        return u"{current[temp]:.0f}\u00b0F({current[feels_like]:.0f}\u00b0F) " \
            u"{current[weather][0][description]} {direction}{current[wind_gust]:.0f}mph " \
            u"{current[humidity]:.0f}%".format(direction=direction, **weather)
    except Exception as e:
        print(e)
        return "Error parsing weather data"

