import pandas as pd
from src.data_layer.open_meteo_api.clean_weather_data import WeatherDataCleaner
from src.data_layer.open_meteo_api.connect_api import WeatherDataFromAPI
from src.data_layer.waiting_times_attractions.clean_waitingtime_data import WaitingTimesCleaner
from src.data_layer.waiting_times_attractions.read_waitingtime_data import WaitingTimesDataLoader
from src.ML_model.feature_target_table.merge_waitingdf_weatherdf import MergeWaitingDFWeatherDF
from src.ML_model.feature_target_table.feature_engineering import FeatureEngineering
from src.ML_model.model.XGBoost_model_train import XGBoostTrainer
from src.ML_model.model.XGBoost_model_predict import XGBoostPredictor

# Get the weather data
forecast_days = int(input('Enter number of forecast days (max 16): '))
forecast_weather_data = WeatherDataFromAPI.get_forecasted_weather(forecast_days)
historical_weather_data = WeatherDataFromAPI.get_historical_weather()

# Clean the weather data
if forecast_weather_data is not None:
    forecast_weather_data = WeatherDataCleaner(forecast_weather_data).clean_data()
    print('Cleaned Forecasted Data:\n', forecast_weather_data.head())
    print('Cleaned Forecasted Data:\n', forecast_weather_data.tail())
print(forecast_weather_data.shape)

if historical_weather_data is not None:
    historical_weather_data = WeatherDataCleaner(historical_weather_data).clean_data()
    print('Cleaned Historical Data:\n', historical_weather_data.head())
    print('Cleaned Forecasted Data:\n', historical_weather_data.tail())


# Load attraction data
data_loader = WaitingTimesDataLoader.data_from_directory()
df_wait_raw = data_loader.load_waiting_times()
attraction_names = data_loader.load_attraction_names()

# Clean atraction data
waiting_cleaner = WaitingTimesCleaner(df_wait_raw)
df_wait_cleaned = waiting_cleaner.clean_and_prepare_data()

# Print result
print(df_wait_cleaned.head(50))
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

trainer = XGBoostTrainer(feature_df)
trainer.hyperparameter_tuning()  # This updates trainer.best_params
trainer.train_model()  # Train using the best parameters
evaluate = trainer.evaluate_model()
print(evaluate)

#
features_prediction = FeatureEngineering(forecast_weather_data)
features_prediction_df = features_prediction.feature_engineer()
datetime_df = forecast_weather_data[['datetime']]
print(features_prediction_df.head(50))
print(features_prediction_df.columns)

# Check number of rows in feature dataframe
print(f"Feature DataFrame Shape: {features_prediction_df.shape}")


predictor = XGBoostPredictor()
prediction = predictor.predict(features_prediction_df, datetime_df, attraction_names)
# Check number of rows in predictions
print(f"Prediction Shape: {prediction.shape}")

# Print first few rows of predictions
print(prediction.head(50))

prediction['date'] = prediction['datetime'].dt.date  # Creates a new 'date' column

# Group by date and calculate the mean for each attraction
df_daily_mean = prediction.groupby("date").mean().reset_index()

# Display the result
print(df_daily_mean.head(50))

total_mean_per_attraction = df_daily_mean.mean(numeric_only=True)

# Display the result
print(total_mean_per_attraction)