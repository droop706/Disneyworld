class WaitingTimesDataLoader:
    def __init__(self):
        """
        Initializes the DataLoader with a folder path.
        Parameters:
        - waiting_folder (str): Path to the waiting times folder
        """
        self.wating_folder = waiting_folder
        if not os.path.exists(self.waiting_folder):
            raise FileNotFoundError(f"Directory not found: {self.waiting_folder}")


        @classmethod
        def data_from_directory(cls, base_folder=None):
            """
            Class method to initialize DataLoader from the project's base directory.
            This method automatically sets up the folder paths based on the project structure.

            Parameters:
            - base_folder (str, optional): Base directory of the project.
                If None, defaults to the script's directory.

            Returns:
            - DataLoader: An instance of DataLoader initialized with the proper folder.
            """
            if base_folder is None:
                base_folder = os.path.dirname(os.path.abspath(__file__))

            waiting_folder = os.path.join(base_folder, "Disney_World", "data", "waiting times")

            return cls(waiting_folder)

        def load_waiting_times(self):
            """
            Loads all CSV files from the 'waiting times' folder.

            Returns:
            - pd.DataFrame: Combined DataFrame of all waiting times.
            """
            waiting_times = []

            # Loop through all files in the waiting times folder
            for attraction in tqdm(os.listdir(self.waiting_folder), desc="Loading wait times"):
                filename = os.path.join(self.waiting_folder, attraction)

                # Ensure it's a CSV file
                if not filename.endswith('.csv'):
                    continue

                df = pd.read_csv(filename)
                if df.empty:
                    continue

                # Insert attraction name (file name without .csv)
                df.insert(0, 'attraction', os.path.splitext(attraction)[0])
                waiting_times.append(df)

            if not waiting_times:
                raise ValueError("No valid data files found in the waiting times directory.")

            df_wait_raw = pd.concat(waiting_times, ignore_index=True)
            return df_wait_raw

