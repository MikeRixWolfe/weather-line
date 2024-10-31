# coding: utf-8

from app import app, cache
import requests


cards = { 0: u"↓", 45: u"↙", 90: u"←", 135: u"↖", 180: u"↑", 225: u"↗", 270: u"→", 315: u"↘", 360: u"↓" }

ww = { 0: "clear skies", 1: "mostly clear skies", 2: "partly cloudy skies", 3: "overcast skies", 45: "fog", 48: "depositing rime fog",
       51: "light drizzle", 53: "drizzle", 55: "dense drizzle", 56: "light freezing drizzle", 57: "dense freezing drizzle",
       61: "light rain", 63: "rain", 65: "heavy rain", 66: "light freezing rain", 67: "heavy freezing rain",
       71: "light snow", 73: "moderate snow", 75: "heavy snow", 77: "snow grains",
       80: "light rain showers", 81: "moderate rain showers", 82: "heavy rain showers", 85: "light snow showers", 86: "heavy snow showers",
       95: "thunderstorms", 96: "thunderstorms with hail", 99: "heavy thunderstorms with hail" }


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
        meteo_url = 'https://api.open-meteo.com/v1/forecast'
        params = {'latitude': geo['geometry']['location']['lat'], 'longitude': geo['geometry']['location']['lng'],
            'current': 'temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m,wind_direction_10m,wind_gusts_10m',
            'temperature_unit': 'fahrenheit', 'wind_speed_unit': 'mph' }
        weather = requests.get(meteo_url, params=params).json()
    except Exception as e:
        print(e)
        return "Meteo API error"

    try:
        direction = cards.get(float(weather['current']['wind_direction_10m']),
            cards[min(cards.keys(), key=lambda k: abs(k - float(weather['current']['wind_direction_10m'])))])

        weather['current']['wind_gusts_10m'] = weather['current'].get('wind_gusts_10m', weather['current']['wind_speed_10m'] + 1)
        weather['current']['description'] = ww[weather['current']['weather_code']]

        return u"{current[temperature_2m]:.0f}\u00b0F({current[apparent_temperature]:.0f}\u00b0F) {current[description]} " \
            u"{direction}{current[wind_speed_10m]:.0f}/{current[wind_gusts_10m]:.0f}mph " \
            u"{current[relative_humidity_2m]:.0f}%".format(direction=direction, **weather)
    except Exception as e:
        print(e)
        return "Error parsing weather data"

