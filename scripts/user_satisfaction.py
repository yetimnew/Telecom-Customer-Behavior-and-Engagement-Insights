import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from sklearn.metrics import pairwise_distances


class UserSatisfactionAnalysis:
    def __init__(self, data):
        """
        Initialize the analysis class with the dataset.

        Parameters:
        data (DataFrame): Input dataset loaded from a file.
        """
        self.data = data

    def calculate_scores(self, engagement_centroid, experience_centroid):
        """
        Calculate engagement, experience, and satisfaction scores for each user.

        Parameters:
        engagement_centroid (array): Centroid coordinates for the least engaged cluster.
        experience_centroid (array): Centroid coordinates for the worst experience cluster.

        Returns:
        DataFrame: Updated data with scores.
        """
        # Define features for engagement and experience
        engagement_features = ['Activity Duration DL (ms)', 'Activity Duration UL (ms)']
        experience_features = ['Avg RTT DL (ms)', 'Avg RTT UL (ms)', 'TCP DL Retrans. Vol (Bytes)']

        # Calculate engagement scores
        self.data['Engagement_Score'] = pairwise_distances(
            self.data[engagement_features],
            np.array(engagement_centroid).reshape(1, -1)
        ).flatten()

        # Calculate experience scores
        self.data['Experience_Score'] = pairwise_distances(
            self.data[experience_features],
            np.array(experience_centroid).reshape(1, -1)
        ).flatten()

        # Calculate satisfaction scores
        self.data['Satisfaction_Score'] = (self.data['Engagement_Score'] + self.data['Experience_Score']) / 2

        return self.data

    def cluster_satisfaction(self, k=2):
        """
        Perform k-means clustering on satisfaction scores.

        Parameters:
        k (int): Number of clusters.

        Returns:
        DataFrame: Updated data with cluster assignments.
        """
        kmeans = KMeans(n_clusters=k, random_state=42)
        self.data['Satisfaction_Cluster'] = kmeans.fit_predict(
            self.data[['Satisfaction_Score']]
        )
        return self.data

    def regression_model(self):
        """
        Build a regression model to predict satisfaction scores.

        Returns:
        LinearRegression: Trained regression model.
        """
        X = self.data[['Engagement_Score', 'Experience_Score']]
        y = self.data['Satisfaction_Score']
        model = LinearRegression()
        model.fit(X, y)
        print(f"Regression Coefficients: {model.coef_}")
        print(f"Intercept: {model.intercept_}")
        print(f"R² Score: {model.score(X, y)}")
        return model

    def visualize_clusters(self):
        """
        Visualize satisfaction clusters using engagement and experience scores.
        """
        plt.figure(figsize=(10, 6))
        for cluster in self.data['Satisfaction_Cluster'].unique():
            cluster_data = self.data[self.data['Satisfaction_Cluster'] == cluster]
            plt.scatter(
                cluster_data['Engagement_Score'],
                cluster_data['Experience_Score'],
                label=f'Cluster {cluster}'
            )
        plt.xlabel('Engagement Score')
        plt.ylabel('Experience Score')
        plt.title('Satisfaction Clusters')
        plt.legend()
        plt.show()
