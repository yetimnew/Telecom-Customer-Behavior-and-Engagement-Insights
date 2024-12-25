import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

class UserEngagement:
    def __init__(self, data):
        """
        Initialize with dataset.

        Parameters:
        data (DataFrame): Input dataset loaded from the database.
        """
        self.data = data

    def aggregate_metrics(self):
        """
        Aggregate session frequency, session duration, and total traffic per user.

        Returns:
        DataFrame: Aggregated metrics.
        """
        aggregated_data = self.data.groupby('MSISDN/Number').agg({
            'Dur. (ms)': 'sum',
            'Total DL (Bytes)': 'sum',
            'Total UL (Bytes)': 'sum'
        }).reset_index()
        aggregated_data.rename(columns={
            'Dur. (ms)': 'total_duration',
            'Total DL (Bytes)': 'total_download',
            'Total UL (Bytes)': 'total_upload'
        }, inplace=True)
        return aggregated_data

    def normalize_metrics(self, aggregated_data):
        """
        Normalize metrics using Min-Max Scaling.

        Parameters:
        aggregated_data (DataFrame): Aggregated metrics.

        Returns:
        DataFrame: Normalized metrics.
        """
        scaler = MinMaxScaler()
        metrics = aggregated_data[['total_duration', 'total_download', 'total_upload']]
        normalized_metrics = scaler.fit_transform(metrics)
        normalized_df = pd.DataFrame(normalized_metrics, columns=metrics.columns)
        return pd.concat([aggregated_data[['MSISDN/Number']], normalized_df], axis=1)

    def perform_clustering(self, normalized_data, k=3):
        """
        Perform k-means clustering on normalized data.

        Parameters:
        normalized_data (DataFrame): Normalized metrics.
        k (int): Number of clusters.

        Returns:
        DataFrame: Data with cluster assignments.
        """
        kmeans = KMeans(n_clusters=k, random_state=42)
        clusters = kmeans.fit_predict(normalized_data[['total_duration', 'total_download', 'total_upload']])
        normalized_data['cluster'] = clusters
        return normalized_data

    def compute_cluster_stats(self, clustered_data):
        """
        Compute statistics for each cluster.

        Parameters:
        clustered_data (DataFrame): Data with cluster assignments.

        Returns:
        DataFrame: Cluster statistics.
        """
        return clustered_data.groupby('cluster').agg({
            'total_duration': ['min', 'max', 'mean', 'sum'],
            'total_download': ['min', 'max', 'mean', 'sum'],
            'total_upload': ['min', 'max', 'mean', 'sum']
        })

    def aggregate_app_traffic(self):
        """
        Aggregate user traffic per application.

        Returns:
        DataFrame: Traffic data per application.
        """
        app_columns = [
            'Social Media DL (Bytes)', 'Social Media UL (Bytes)',
            'Google DL (Bytes)', 'Google UL (Bytes)',
            'Email DL (Bytes)', 'Email UL (Bytes)',
            'Youtube DL (Bytes)', 'Youtube UL (Bytes)',
            'Netflix DL (Bytes)', 'Netflix UL (Bytes)',
            'Gaming DL (Bytes)', 'Gaming UL (Bytes)',
            'Other DL (Bytes)', 'Other UL (Bytes)'
        ]
        traffic_data = self.data.groupby('MSISDN/Number')[app_columns].sum().reset_index()
        return traffic_data

    def elbow_method(self, normalized_data, max_k=10):
        """
        Use the elbow method to find the optimal number of clusters.

        Parameters:
        normalized_data (DataFrame): Normalized metrics.
        max_k (int): Maximum number of clusters to test.

        Returns:
        None: Displays the elbow plot.
        """
        distortions = []
        for k in range(1, max_k + 1):
            kmeans = KMeans(n_clusters=k, random_state=42)
            kmeans.fit(normalized_data[['total_duration', 'total_download', 'total_upload']])
            distortions.append(kmeans.inertia_)

        plt.figure(figsize=(8, 5))
        plt.plot(range(1, max_k + 1), distortions, marker='o')
        plt.title('Elbow Method for Optimal k')
        plt.xlabel('Number of Clusters (k)')
        plt.ylabel('Distortion')
        plt.show()
