import pandas as pd
from src.data_layer.open_meteo_api.clean_weather_data import WeatherDataCleaner
from src.data_layer.open_meteo_api.connect_api import WeatherDataFromAPI
from src.data_layer.waiting_times_attractions.clean_waitingtime_data import WaitingTimesCleaner
from src.data_layer.waiting_times_attractions.read_waitingtime_data import WaitingTimesDataLoader
from src.ML_model.feature_target_table.merge_waitingdf_weatherdf import MergeWaitingDFWeatherDF
from src.ML_model.feature_target_table.feature_engineering import FeatureEngineering


# Get the weather data
#orecast_days = int(input('Enter number of forecast days (max 16): '))
#forecast_weather_data = WeatherDataFromAPI.get_forecasted_weather(forecast_days)
historical_weather_data = WeatherDataFromAPI.get_historical_weather()

# Clean the weather data
#if forecast_weather_data is not None:
    #forecast_weather_data = WeatherDataCleaner(forecast_weather_data).clean_data()
    #print('Cleaned Forecasted Data:\n', forecast_weather_data.head())
    #print('Cleaned Forecasted Data:\n', forecast_weather_data.tail())

if historical_weather_data is not None:
    historical_weather_data = WeatherDataCleaner(historical_weather_data).clean_data()
    print('Cleaned Historical Data:\n', historical_weather_data.head())
    print('Cleaned Forecasted Data:\n', historical_weather_data.tail())


# Load attraction data
data_loader = WaitingTimesDataLoader.data_from_directory()
df_wait_raw = data_loader.load_waiting_times()

# Clean atraction data
waiting_cleaner = WaitingTimesCleaner(df_wait_raw)
df_wait_cleaned = waiting_cleaner.clean_and_prepare_data()

# Print result
print(df_wait_cleaned.head())
print(df_wait_cleaned.columns)

# Merge dataframes together
merger = MergeWaitingDFWeatherDF(df_wait_cleaned, historical_weather_data)
merged_df = merger.merge_df()
print(merged_df.head(50))
print(merged_df.columns)

feature = FeatureEngineering(merged_df)
feature_df = feature.feature_engineer()

print(feature_df.head())
print(feature_df.columns)

#print(feature_df['visibility'].head())
#print(type(feature_df['visibility']))

#print(feature_df['weather_code'].head())
#print(type(feature_df['weather_code']))
