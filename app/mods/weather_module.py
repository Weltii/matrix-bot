import re
from config import open_weather_map as conf
import requests
import json

units = "metric"
lang = "de"
city_default = "Nuuk"


def get_current_weather(city=city_default):
    """
    Returns the current weather in the specified city
    :param city:
    :return:
    """
    city.strip()
    if len(city) <= 0:
        city = city_default
    url = (
        "http://api.openweathermap.org/data/2.5/weather?q="
        + city
        + "&APPID="
        + conf.get("user_id")
        + "&units="
        + units
        + "&lang="
        + lang
    )
    weather = get_weather(url)
    if str(weather["cod"]) == "200":
        return (
            "Wetter in: " + str(weather["name"]) + "\n"
            "Aktuelle Temperatur: " + str(weather["main"]["temp"]) + "°C\n"
            "Beschreibung des Wetters: " +
                str(weather["weather"][0]["description"])
        )
    return 'Unknown City "' + city + '"!'


def get_weather(url):
    data = requests.get(url)
    binary = data.content
    return json.loads(binary)


def get_weather_for_cities(input: str):
    arguments=input.split(" ")
    del arguments[0]
    length=len(arguments)
    if length > 0:
        ret=""
        if length > 1:
            ret="Die Auswahl an Wetterdaten: \n"
        for argument in arguments:
            ret += get_current_weather(argument)
            ret += "\n\n"
        return ret
    else:
        return get_current_weather(city_default)

    return get_current_weather(city_default)
