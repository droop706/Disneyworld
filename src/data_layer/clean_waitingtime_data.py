class WaitingTimesCleaner:
    def __init__(self, df_wait_raw):
        self.df_wait_raw = df_wait_raw

    def clean_data(self):
        """
        Clean the waiting times data by removing outliers and transforming datetime columns.

        Returns:
        - pd.DataFrame: Cleaned waiting times DataFrame.
        """
        df_wait = self.df_wait_raw.copy()

        # Cleaning the actual waiting times (removing outliers)
        df_wait = df_wait[((df_wait.SACTMIN >= -1000) & (df_wait.SACTMIN < 360)) | (df_wait.SACTMIN.isnull())]

        # Removing outliers from posted waiting times (attraction closed at -999)
        df_wait = df_wait[(df_wait.SPOSTMIN >= -998.99) | (df_wait.SPOSTMIN.isnull())]

        # Convert date and datetime to datetime objects
        df_wait['date'] = pd.to_datetime(df_wait.date, format='%m/%d/%Y')
        df_wait['datetime'] = pd.to_datetime(df_wait.datetime, format='%Y-%m-%d %H:%M:%S')

        # Print how many rows were removed
        print(f"Removed {len(self.df_wait_raw) - len(df_wait)} rows")

        return df_wait
