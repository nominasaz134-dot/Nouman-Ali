import requests
from config import API_KEY


BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"


def get_weather(city):
    """
    Fetch current weather data for a given city.
    Returns weather data if successful, otherwise None.
    """

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(BASE_URL, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            print("Error:", response.json().get("message"))
            return None

    except requests.exceptions.RequestException as e:
        print("Network Error:", e)
        return None


def get_forecast(city):
    """
    Fetch 5-day weather forecast.
    """

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(FORECAST_URL, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            print(response.json().get("message"))
            return None

    except requests.exceptions.RequestException as e:
        print(e)
        return None