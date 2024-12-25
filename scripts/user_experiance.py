import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt


class UserExperienceAnalysis:
    def __init__(self, data):
        """
        Initialize the analysis class with the dataset.

        Parameters:
        data (DataFrame): Input dataset loaded from a file.
        """
        self.data = data

    def aggregate_metrics(self):
        """
        Aggregate user experience metrics per customer (MSISDN/Number).

        Returns:
        DataFrame: Aggregated metrics per customer.
        """
        aggregated_data = self.data.groupby('MSISDN/Number').agg({
            'Avg RTT DL (ms)': 'mean',
            'Avg RTT UL (ms)': 'mean',
            'Avg Bearer TP DL (kbps)': 'mean',
            'Avg Bearer TP UL (kbps)': 'mean',
            'Handset Type': 'first',
            'Total DL (Bytes)': 'sum',
            'Total UL (Bytes)': 'sum'
        }).reset_index()
        return aggregated_data

    def clean_data(self, aggregated_data):
        """
        Clean the aggregated data by handling missing values and outliers.

        Parameters:
        aggregated_data (DataFrame): Aggregated metrics.

        Returns:
        DataFrame: Cleaned data.
        """
        # Fill missing values
        for col in ['Avg RTT DL (ms)', 'Avg RTT UL (ms)', 'Avg Bearer TP DL (kbps)', 'Avg Bearer TP UL (kbps)']:
            aggregated_data[col].fillna(aggregated_data[col].mean(), inplace=True)

        # Treat outliers using IQR method
        for col in ['Avg RTT DL (ms)', 'Avg RTT UL (ms)', 'Avg Bearer TP DL (kbps)', 'Avg Bearer TP UL (kbps)']:
            q1 = aggregated_data[col].quantile(0.25)
            q3 = aggregated_data[col].quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            aggregated_data[col] = np.clip(aggregated_data[col], lower_bound, upper_bound)

        return aggregated_data

    def plot_metric_distribution(self, data, group_col, value_col, title):
        """
        Plot the distribution of a metric grouped by another column.

        Parameters:
        data (DataFrame): Input data for plotting.
        group_col (str): Column to group data by.
        value_col (str): Metric column to visualize.
        title (str): Title of the plot.
        """
        distribution = data.groupby(group_col)[value_col].mean()
        distribution.plot(kind='bar', title=title, figsize=(10, 6))
        plt.xlabel(group_col)
        plt.ylabel(value_col)
        plt.show()

    def perform_kmeans_clustering(self, data, feature_columns, n_clusters=3):
        """
        Perform K-means clustering on the specified features.

        Parameters:
        data (DataFrame): Input data for clustering.
        feature_columns (list): List of feature columns to use for clustering.
        n_clusters (int): Number of clusters for K-means.

        Returns:
        DataFrame: Data with cluster assignments.
        """
        scaler = StandardScaler()
        scaled_features = scaler.fit_transform(data[feature_columns])
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        data['Experience_Cluster'] = kmeans.fit_predict(scaled_features)
        return data

    def save_results(self, data, output_path):
        """
        Save the processed results to a CSV file.

        Parameters:
        data (DataFrame): Data to save.
        output_path (str): File path for saving.
        """
        data.to_csv(output_path, index=False)


# Example usage:
if __name__ == "__main__":
    # Load the dataset
    file_path = "telecom_data.csv"  # Replace with your file path
    data = pd.read_csv(file_path)

    # Initialize the analysis pipeline
    analysis = UserExperienceAnalysis(data)

    # Step 1: Aggregate data
    aggregated_data = analysis.aggregate_metrics()

    # Step 2: Clean data
    cleaned_data = analysis.clean_data(aggregated_data)

    # Step 3: Plot distribution of throughput
    analysis.plot_metric_distribution(cleaned_data, 'Handset Type', 'Avg Bearer TP DL (kbps)', 
                                      "Average Throughput (DL) per Handset Type")

    # Step 4: Perform clustering
    clustered_data = analysis.perform_kmeans_clustering(cleaned_data, 
                                                         ['Avg RTT DL (ms)', 'Avg RTT UL (ms)', 
                                                          'Avg Bearer TP DL (kbps)', 'Avg Bearer TP UL (kbps)'], 
                                                         n_clusters=3)

    # Step 5: Save results
    analysis.save_results(clustered_data, "user_experience_analysis_results.csv")
