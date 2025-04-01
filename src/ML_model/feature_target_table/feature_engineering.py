import pandas as pd
import numpy as np
from src.ML_model.feature_target_table.merge_waitingdf_weatherdf import MergeWaitingDFWeatherDF

class FeatureEngineering:
    def __init__(self, merged_df):
        self.df = merged_df.copy()

    def create_time_features(self):
        """Create time-based features like hour of day, day of week, and if it's weekend"""
        self.df['datetime'] = pd.to_datetime(self.df['datetime'])  # Ensure datetime format
        self.df['hour_of_day'] = self.df['datetime'].dt.hour.astype(str)
        self.df['day_of_week'] = self.df['datetime'].dt.weekday.astype(str)  # 0=Monday, 6=Sunday
        self.df['is_weekend'] = (self.df['day_of_week'].astype(int) >= 5)
        self.df['month'] = self.df['datetime'].dt.month.astype(str)

    def one_hot_encoder(self):
        self.df['weather_code'] = self.df['weather_code'].astype(str)
        self.df = pd.get_dummies(self.df, drop_first=True)
        return self.df

    def feature_engineer(self):
        """Execute feature engineering pipeline."""
        self.create_time_features()
        self.one_hot_encoder()
        self.df.drop(columns=['datetime'], inplace=True)
        return self.df

# Example Usage:
# fe = FeatureEngineering(merged_df)
# final_df = fe.feature_engineer()
