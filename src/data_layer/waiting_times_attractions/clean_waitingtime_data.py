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

        # Remove outliers in actual wait times (SACTMIN) and posted wait times (SPOSTMIN)
        self.df_wait_cleaned = self.df_wait_cleaned[((self.df_wait_cleaned.SACTMIN >= -1000) & (self.df_wait_cleaned.SACTMIN < 360)) | (self.df_wait_cleaned.SACTMIN.isnull())]
        self.df_wait_cleaned = self.df_wait_cleaned[(self.df_wait_cleaned.SPOSTMIN >= -998.99) | (self.df_wait_cleaned.SPOSTMIN.isnull())]

        # Convert date columns to datetime
        self.df_wait_cleaned['date'] = pd.to_datetime(self.df_wait_cleaned['date'], format='%m/%d/%Y')
        self.df_wait_cleaned['datetime'] = pd.to_datetime(self.df_wait_cleaned['datetime'], format='%Y-%m-%d %H:%M:%S')

        # Fill in missing SPOSTMIN values
        self.df_wait_cleaned['SPOSTMIN'] = self.df_wait_cleaned['SPOSTMIN'].ffill()

        return self.df_wait_cleaned

    # These are specific ML operations so passing data as arguments (not .self)
    def bucketize_to_hourly(self):
        """
        Groups the waiting times data into 1 hour buckets.

        Parameters:
        - df_wait (pd.DataFrame): DataFrame with cleaned waiting times.

        Returns:
        - pd.DataFrame: Aggregated DataFrame with hourly bins.
        """
        self.df_wait_cleaned['datetime'] = self.df_wait_cleaned['datetime'].dt.floor('H')

        # Aggregate by hour (mean wait time per hour)
        df_hourly = self.df_wait_cleaned.groupby(['attraction', 'datetime']).agg({
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

    def add_is_closed_column(self, df_wait_ML):
        """
        Adds a column to indicate ride closures (is_closed).

        Parameters:
        - df_wait_ML (pd.DataFrame): DataFrame for model input.

        Returns:
        - pd.DataFrame: DataFrame with the 'is_closed' column added.
        """
        # Create 'is_closed' column: 1 if SPOSTMIN is NaN
        df_wait_ML['is_closed'] = df_wait_ML['SPOSTMIN'].isna().astype(int)

        # Optionally mark closures with -1 for SPOSTMIN if needed
        #df_wait_ML['SPOSTMIN'] = df_wait_ML['SPOSTMIN'].fillna(-1)

        return df_wait_ML

    def pivot_attractions(self, df_wait_ML):
        """
        Pivot the attraction data (SPOSTMIN and is_closed) to have separate columns for each attraction.

        Parameters:
        - df_wait_ML (pd.DataFrame): DataFrame for model input with waiting times and closures.

        Returns:
        - pd.DataFrame: Pivoted DataFrame with columns for each attraction's waiting time and closure status.
        """
        # Pivot data to separate columns for each attraction's waiting time (SPOSTMIN) and is_closed status
        df_pivoted = df_wait_ML.pivot_table(index='datetime',
                                            columns='attraction',
                                            values=['SPOSTMIN', 'is_closed']).reset_index()
        df_pivoted.columns = ['_'.join(col).strip() if isinstance(col, tuple) and col[0] != 'datetime' else col[0] for col in df_pivoted.columns]


        return df_pivoted

    def clean_and_prepare_data(self):
        """
        Perform the entire cleaning and preparation pipeline:
        clean, bucketize, add closure flag, pivot.
        This pipeline is useful for creating the machine learning model features table next

        Returns:
        - pd.DataFrame: Final cleaned and pivoted DataFrame ready for ML.
        """
        df_wait_cleaned = self.clean_data()  # Clean the raw data
        df_hourly = self.bucketize_to_hourly()  # Aggregate to hourly
        df_wait_ML = self.remove_columns(df_hourly)  # Remove unnecessary columns

        # Add is_closed flag and pivot the table
        df_wait_ML = self.add_is_closed_column(df_wait_ML)
        df_pivoted = self.pivot_attractions(df_wait_ML)

        return df_pivoted
