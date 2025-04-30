import pandas as pd

class WaitingTimesCleaner:
    def __init__(self, df_wait_raw):
        self.df_wait_raw = df_wait_raw

    def clean_data(self):
        """
        Clean the waiting times data by removing outliers and transforming datetime columns.

        Returns:
        - pd.DataFrame: Partially cleaned DataFrame (before bucketing into 1 hour intervals).
        """
        df_wait_cleaned = self.df_wait_raw.copy()

        # Remove outliers in actual wait times (SACTMIN) and posted wait times (SPOSTMIN)
        df_wait_cleaned = df_wait_cleaned[((df_wait_cleaned.SACTMIN >= -1000) & (df_wait_cleaned.SACTMIN < 360)) | (df_wait_cleaned.SACTMIN.isnull())]
        df_wait_cleaned = df_wait_cleaned[(df_wait_cleaned.SPOSTMIN >= -998.99) | (df_wait_cleaned.SPOSTMIN.isnull())]

        # Convert date columns to datetime
        df_wait_cleaned['date'] = pd.to_datetime(df_wait_cleaned['date'], format='%m/%d/%Y')
        df_wait_cleaned['datetime'] = pd.to_datetime(df_wait_cleaned['datetime'], format='%Y-%m-%d %H:%M:%S')

        # Fill in missing SPOSTMIN values
        df_wait_cleaned['SPOSTMIN'] = df_wait_cleaned['SPOSTMIN'].ffill()

        return df_wait_cleaned

    def bucketize_to_hourly(self, df_wait_cleaned):
        """
        Groups the waiting times data into 1 hour buckets.

        Parameters:
        - df_wait (pd.DataFrame): DataFrame with cleaned waiting times.

        Returns:
        - pd.DataFrame: Aggregated DataFrame with hourly bins.
        """
        df_wait_cleaned['hour'] = df_wait_cleaned['datetime'].dt.floor('H')

        # Aggregate by hour (mean wait time per hour)
        df_hourly = df_wait_cleaned.groupby(['attraction', 'hour']).agg({
            'SACTMIN': 'mean',
            'SPOSTMIN': 'mean',
            'date': 'first'
        }).reset_index()

        return df_hourly

    def remove_columns(self, df_hourly):
        """
        Removes columns not neede for ML model.

        Parameters:
        - df_hourly (pd.DataFrame): DataFrame buckethed waiting times.

        Returns:
        - pd.DataFrame: Dataframe with date and SACTMIN columns removed.
        """
        # Drop unnecessary columns for ML model
        df_wait_ML = df_hourly.drop(columns=['date', 'SACTMIN'])

        return df_wait_ML



