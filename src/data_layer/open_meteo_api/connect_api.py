import requests
from weather_parameters import COMMON_PARAMETERS, HISTORICAL_PARAMETERS, HTTP_RESPONSE_SUCCESS

def get_forecasted_weather(forecast_days):
    url = 'https://api.open-meteo.com/v1/forecast'
    params = {**COMMON_PARAMETERS, "forecast_days": forecast_days}
    response = requests.get(url, params=params)

    if response.status_code == HTTP_RESPONSE_SUCCESS:
        return response.json()
    else:
        print("Error fetching weather forecast")
        return None


def get_historical_weather():
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {**COMMON_PARAMETERS, **HISTORICAL_PARAMETERS}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print("Error fetching historical weather data")
        return None

if __name__ == "__main__":
    forecast_days = int(input("Enter number of forecast days (max 16): "))
    weather_forecast_data = get_forecasted_weather(forecast_days)
    historical_forecast_data = get_historical_weather()

    if weather_forecast_data:
        print(weather_forecast_data)

    if historical_forecast_data:
        print(historical_forecast_data)