import os
import pandas as pd

class WaitingTimesDataLoader:
    def __init__(self, waiting_folder):
        """
        Initializes the DataLoader with a folder path.
        """
        self.waiting_folder = waiting_folder
        if not os.path.exists(self.waiting_folder):
            raise FileNotFoundError(f"Directory not found: {self.waiting_folder}")

    @classmethod
    def data_from_directory(cls):
        """
        Finds and sets the correct 'waiting times' folder path.
        """
        script_folder = os.path.dirname(os.path.abspath(__file__))  # This is in src/data_layer
        disney_world_folder = os.path.abspath(os.path.join(script_folder, "..", "..", ".."))

        waiting_folder = os.path.join(disney_world_folder, "data", "waiting times")

        return cls(waiting_folder)

    def load_waiting_times(self):
        """
        Loads all CSV files from the 'waiting times' folder.
        """
        waiting_times = []

        for attraction in os.listdir(self.waiting_folder):
            filename = os.path.join(self.waiting_folder, attraction)

            if not filename.endswith('.csv'):
                continue

            df = pd.read_csv(filename)
            if df.empty:
                continue

            df.insert(0, 'attraction', os.path.splitext(attraction)[0])
            waiting_times.append(df)

        if not waiting_times:
            raise ValueError("No valid data files found in the waiting times directory.")

        df_wait_raw = pd.concat(waiting_times, ignore_index=True)

        return df_wait_raw

    def load_attraction_names(self):
        """
        Loads and returns a list of attraction names based on the CSV filenames.
        """
        attraction_names = []

        for attraction in os.listdir(self.waiting_folder):
            filename = os.path.join(self.waiting_folder, attraction)

            if not filename.endswith('.csv'):
                continue

            # Extract the attraction name (remove file extension)
            attraction_names.append(os.path.splitext(attraction)[0])

        return attraction_names