import requests
import pandas as pd
from .weather_parameters import COMMON_PARAMETERS, HISTORICAL_PARAMETERS, HTTP_RESPONSE_SUCCESS

class WeatherDataFromAPI:
    @staticmethod
    def get_forecasted_weather(forecast_days):
        url = 'https://api.open-meteo.com/v1/forecast'
        params = {**COMMON_PARAMETERS, 'forecast_days': forecast_days}
        response = requests.get(url, params=params)

        if response.status_code == HTTP_RESPONSE_SUCCESS:
            return WeatherDataFromAPI.json_to_dataframe(response.json())
        else:
            print('Error fetching weather forecast')
            return None

    @staticmethod
    def get_historical_weather():
        url = 'https://archive-api.open-meteo.com/v1/archive'
        params = {**COMMON_PARAMETERS, **HISTORICAL_PARAMETERS}
        response = requests.get(url, params=params)

        if response.status_code == HTTP_RESPONSE_SUCCESS:
            return WeatherDataFromAPI.json_to_dataframe(response.json())
        else:
            print('Error fetching historical weather data')
            return None

    @staticmethod
    def json_to_dataframe(weather_json):
        """Converts JSON weather data into DataFrame."""
        if not weather_json:
            print('No data to process')
            return None

        df_weather = pd.DataFrame(weather_json['hourly'])
        df_weather['date'] = pd.to_datetime(weather_json['hourly']['time'])

        return df_weather
