from clean_weather_data import WeatherDataCleaner
from connect_api import WeatherDataFromAPI  # Your API class

# Get the weather data
forecast_days = int(input('Enter number of forecast days (max 16): '))
forecast_weather_data = WeatherDataFromAPI.get_forecasted_weather(forecast_days)
historical_weather_data = WeatherDataFromAPI.get_historical_weather()

# Clean the weather data
if forecast_weather_data is not None:
    forecast_weather_data = WeatherDataCleaner(forecast_weather_data).clean_data()
    print('Cleaned Forecasted Data:\n', forecast_weather_data.head())
    print('Cleaned Forecasted Data:\n', forecast_weather_data.tail())

if historical_weather_data is not None:
    historical_weather_data = WeatherDataCleaner(historical_weather_data).clean_data()
    print('Cleaned Historical Data:\n', historical_weather_data.head())
    print('Cleaned Forecasted Data:\n', historical_weather_data.tail())
