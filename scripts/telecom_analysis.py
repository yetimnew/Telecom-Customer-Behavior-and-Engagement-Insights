import pandas as pd
from sqlalchemy import create_engine

class TelecomAnalysis:
    def __init__(self, database, password, table_name):
        """
        Initialize with database name, password, and table name.
        """
        self.database = database
        self.password = password
        self.table_name = table_name
        self.engine = create_engine(f"postgresql://postgres:{password}@localhost:5432/{database}")
        self.data = None

    def load_data(self):
        """
        Load data from the PostgreSQL database.
        """
        query = f"SELECT * FROM {self.table_name}"
        self.data = pd.read_sql(query, self.engine)
        print("Data loaded successfully!")
        return self.data

    def explore_data(self):
        """
        Perform basic exploration on the dataset.
        """
        if self.data is not None:
            print("\nDataset Info:")
            print(self.data.info())
            print("\nDataset Description:")
            print(self.data.describe())
        else:
            print("No data loaded for exploration.")

    def find_top_handsets(self, n=10):
        """
        Identify the top N handsets used by customers.
        """
        if self.data is not None:
            if 'Handset Type' in self.data.columns:
                top_handsets = self.data['Handset Type'].value_counts().head(n)
                print(f"\nTop {n} Handsets:\n", top_handsets)
                return top_handsets
            else:
                print("Warning: 'Handset Type' column not found in the dataset.")
                return None
        else:
            print("No data loaded.")

    def find_top_manufacturers(self, n=3):
        """
        Identify the top N handset manufacturers.
        """
        if self.data is not None:
            if 'Handset Manufacturer' in self.data.columns:
                top_manufacturers = self.data['Handset Manufacturer'].value_counts().head(n)
                print(f"\nTop {n} Handset Manufacturers:\n", top_manufacturers)
                return top_manufacturers
            else:
                print("Warning: 'Handset Manufacturer' column not found in the dataset.")
                return None
        else:
            print("No data loaded.")

    def find_top_handsets_per_manufacturer(self, manufacturers, n=5):
        """
        Identify the top N handsets for each manufacturer.
        """
        if self.data is not None:
            if 'Handset Manufacturer' in self.data.columns and 'Handset Type' in self.data.columns:
                result = {}
                for manufacturer in manufacturers:
                    top_handsets = (
                        self.data[self.data['Handset Manufacturer'] == manufacturer]['Handset Type']
                        .value_counts()
                        .head(n)
                    )
                    result[manufacturer] = top_handsets
                return result
            else:
                print("Required columns not found: 'Handset Manufacturer' or 'Handset Type'.")
                return None
        else:
            print("No data loaded.")

    def aggregate_user_metrics(self):
        """
        Aggregate per user: number of xDR sessions, total download/upload data, total data volume,
        and average session duration.
        """
        if self.data is not None:
            # Use the exact column names from the dataset
            if 'MSISDN/Number' in self.data.columns:
                user_metrics = self.data.groupby('MSISDN/Number').agg(
                    total_sessions=('bearer id', 'count'),  # Ensure 'bearer id' exists
                    total_download=('Total DL (Bytes)', 'sum'),  # Ensure 'Total DL (Bytes)' exists
                    total_upload=('Total UL (Bytes)', 'sum'),  # Ensure 'Total UL (Bytes)' exists
                    total_data_volume=('Total DL (Bytes)', 'sum'),  # Same as total_download
                    average_duration=('Dur. (s)', 'mean')  # Ensure 'Dur. (s)' exists
                )
                print("\nAggregated User Metrics:")
                print(user_metrics.head())
                return user_metrics
            else:
                print("Column 'MSISDN/Number' not found in the dataset.")
        else:
            print("No data loaded.")
