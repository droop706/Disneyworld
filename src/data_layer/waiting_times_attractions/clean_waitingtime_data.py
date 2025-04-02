import pandas as pd

class WaitingTimesCleaner:
    def __init__(self, df_wait_raw):
        self.df_wait_raw = df_wait_raw

    def clean_data(self):
        """
        Clean the waiting times data by removing outliers and transforming datetime columns.
        General operation so using self to store
        Returns:
        - pd.DataFrame: Partially cleaned DataFrame (before bucketing into 1 hour intervals).
        """
        self.df_wait_cleaned = self.df_wait_raw.copy()

        # Remove date en SACTMIN column, these will not be used
        self.df_wait_cleaned = self.df_wait_cleaned.drop(columns=['date', 'SACTMIN'])

        # Remove outliers in posted wait times (SPOSTMIN)
        self.df_wait_cleaned = self.df_wait_cleaned[(self.df_wait_cleaned.SPOSTMIN >= -998.99) | (self.df_wait_cleaned.SPOSTMIN.isnull())]

        # Convert date columns to datetime
        self.df_wait_cleaned['datetime'] = pd.to_datetime(self.df_wait_cleaned['datetime'], format='%Y-%m-%d %H:%M:%S')

        # Fill in missing SPOSTMIN values
        self.df_wait_cleaned['SPOSTMIN'] = self.df_wait_cleaned['SPOSTMIN'].ffill()
        self.df_wait_cleaned.dropna(subset=['SPOSTMIN'], inplace=True)

        return self.df_wait_cleaned

    # These are specific ML operations so passing data as arguments (not .self)
    def bucketize_to_hourly(self):
        """
        Groups the waiting times data into 1 hour buckets.

        Parameters:
        - df_wait_cleaned (pd.DataFrame): DataFrame with cleaned waiting times.

        Returns:
        - pd.DataFrame: Aggregated DataFrame with hourly bins.
        """
        self.df_wait_cleaned['datetime'] = self.df_wait_cleaned['datetime'].dt.floor('H')
        self.df_wait_cleaned = self.df_wait_cleaned[(self.df_wait_cleaned['datetime'].dt.hour >= 7) & (self.df_wait_cleaned['datetime'].dt.hour <= 22)]

        # Aggregate by hour (mean wait time per hour)
        df_hourly = self.df_wait_cleaned.groupby(['attraction', 'datetime']).agg(
            {'SPOSTMIN': 'mean'}).reset_index()

        return df_hourly

    def pivot_attractions(self, df_hourly):
        """
        Pivot the attraction data (SPOSTMIN) to have separate columns for each attraction.

        Parameters:
        - df_hourly (pd.DataFrame): DataFrame for model input with waiting times per hour.

        Returns:
        - pd.DataFrame: Pivoted DataFrame with columns for each attraction's waiting time.
        """
        # Pivot data to separate columns for each attraction's waiting time (SPOSTMIN) and is_closed status
        df_pivoted = df_hourly.pivot_table(index='datetime',
                                            columns='attraction',
                                            values='SPOSTMIN').reset_index()

        df_pivoted.columns = ['datetime'] + [f"SPOSTMIN_{col}" for col in df_pivoted.columns[1:]]

        return df_pivoted

    def clean_and_prepare_data(self):
        """
        Perform the entire cleaning and preparation pipeline:
        clean, bucketize, pivot.
        This pipeline is useful for creating the machine learning model features table next

        Returns:
        - pd.DataFrame: Final cleaned and pivoted DataFrame ready for ML.
        """
        df_wait_cleaned = self.clean_data()  # Clean the raw data
        df_hourly = self.bucketize_to_hourly()  # Aggregate to hourly
        df_pivoted = self.pivot_attractions(df_hourly)
        df_pivoted.fillna(0, inplace=True)

        return df_pivoted
