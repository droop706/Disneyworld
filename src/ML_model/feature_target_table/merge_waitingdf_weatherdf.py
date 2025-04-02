from src.data_layer.open_meteo_api.clean_weather_data import WeatherDataCleaner
from src.data_layer.open_meteo_api.connect_api import WeatherDataFromAPI
from src.data_layer.waiting_times_attractions.clean_waitingtime_data import WaitingTimesCleaner
from src.data_layer.waiting_times_attractions.read_waitingtime_data import WaitingTimesDataLoader
import pandas as pd

class MergeWaitingDFWeatherDF:
    def __init__(self, waiting_df, weather_df):
        self.waiting_df = waiting_df
        self.weather_df = weather_df

    def merge_df(self):
        merged_df = pd.merge(self.weather_df, self.waiting_df, on='datetime', how='inner')
        return merged_df

