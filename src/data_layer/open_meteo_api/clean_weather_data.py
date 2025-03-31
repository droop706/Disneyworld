import pandas as pd

class WeatherDataCleaner:
    def __init__(self, df_weather_cleaned):
        """
        Initialize the cleaner with a weather DataFrame.
        """
        self.df_weather_cleaned = df_weather_cleaned

    def clean_data(self):
        """
        Cleans the weather DataFrame.
        Returns:
        - pd.DataFrame: Cleaned weather DataFrame
        """
        if self.df_weather_cleaned is None or self.df_weather_cleaned.empty:
            print('No data to clean')
            return None

        # Convert date column to proper datetime format
        if 'date' in self.df_weather_cleaned.columns:
            self.df_weather_cleaned['date'] = pd.to_datetime(self.df_weather_cleaned['date'])

        # Rename columns for consistency
        self.df_weather_cleaned.rename(columns={'date': 'datetime'}, inplace=True)

        # Delete time column
        self.df_weather_cleaned.drop(columns=['time'], inplace=True)

        return self.df_weather_cleaned
