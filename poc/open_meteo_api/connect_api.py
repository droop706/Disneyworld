import requests

def get_weather_forecast():
    url = 'https://api.open-meteo.com/v1/forecast'

    # Get 14 day weather forecast
    parameters = {
        'latitude': 28.4237,
        'longitude': -81.5812,
        'daily': ('precipitation_sum,'
                  'uv_index_max,'
                  'temperature_2m_max,'
                  'temperature_2m_min,'
                  'weather_code,'
                  'sunshine_duration,'
                  'wind_speed_10m_max,'
        ),
        'timezone': 'America/New_York',
        'forecast_days': 16
    }
    response = requests.get(url, params=parameters)

    if response.status_code == 200:
        return response.json()
    else:
        print("Error fetching weather forecast")
        return None

weather_forecast_data = get_weather_forecast()

if weather_forecast_data:
    print(weather_forecast_data)