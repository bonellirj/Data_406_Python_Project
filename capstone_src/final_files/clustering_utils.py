# clustering_utils.py

import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans

def elbow_method(X, max_clusters=10, random_state=42):
    """
    Calculate and plot distortions for different numbers of clusters using the Elbow method.

    Parameters:
    X (DataFrame or array-like): The data to be clustered.
    max_clusters (int): The maximum number of clusters to test.
    random_state (int): The seed used by the random number generator.
    """
    distortions = []
    K = range(2, max_clusters + 1)

    for k in K:
        kmeans = KMeans(n_clusters=k, random_state=random_state)
        kmeans.fit(X)
        distortions.append(kmeans.inertia_)

    # Plot the Elbow method result
    plt.figure(figsize=(10, 6))
    plt.plot(K, distortions, 'bx-')
    plt.xlabel('Number of clusters')
    plt.ylabel('Distortion')
    plt.title('Elbow Method For Optimal k')
    plt.tight_layout()
    plt.show()


def perform_clustering(data, num_clusters):
    """
    Perform clustering on the given dataset with the specified number of clusters.
    
    Parameters:
    data (pd.DataFrame): The dataset to be clustered.
    num_clusters (int): The number of clusters to form.
    
    Returns:
    pd.DataFrame: The dataset with an additional 'Cluster' column.
    """
    # Perform clustering 
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    data['Cluster'] = kmeans.fit_predict(data)
    return data



def plot_clusters(data):
    """
    Plot the clusters for the given dataset.
    
    Parameters:
    data (pd.DataFrame): The dataset containing the cluster information.
    """
    # Plot Time_in_sec_per_session vs Gestures_per_session
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='Time_in_sec_per_session', y='Gestures_per_session', hue='Cluster',
                    data=data, palette='viridis')
    plt.title('Clustering of Users')
    plt.xlabel('Time in Seconds per Session')
    plt.ylabel('Gestures per Session')
    plt.show()

    # Plot Sessions_per_month vs Gestures_per_session
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='Sessions_per_month', y='Gestures_per_session', hue='Cluster',
                    data=data, palette='viridis')
    plt.title('Clustering of Users')
    plt.xlabel('Sessions per Month')
    plt.ylabel('Gestures per Session')
    plt.show()

    # Plot Time_in_sec_per_session vs Sessions_per_month
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='Time_in_sec_per_session', y='Sessions_per_month', hue='Cluster',
                    data=data, palette='viridis')
    plt.title('Clustering of Users')
    plt.xlabel('Time in Seconds per Session')
    plt.ylabel('Sessions per Month')
    plt.show()


def plot_weighted_clusters(data, original_data):
    """
    Plot the weighted clusters for the given dataset.
    
    Parameters:
    data (pd.DataFrame): The dataset containing the cluster information.
    original_data (pd.DataFrame): The original dataset containing the columns for plotting.
    """
    # Plot Time_in_sec_per_session vs Gestures_per_session
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='Time_in_sec_per_session', y='Gestures_per_session', hue='Cluster',
                    data=original_data.join(data['Cluster']), palette='viridis')
    plt.title('Clustering of Users')
    plt.xlabel('Time in Seconds per Session')
    plt.ylabel('Gestures per Session')
    plt.show()

    # Plot Sessions_per_month vs Gestures_per_session
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='Sessions_per_month', y='Gestures_per_session', hue='Cluster',
                    data=original_data.join(data['Cluster']), palette='viridis')
    plt.title('Clustering of Users')
    plt.xlabel('Sessions per Month')
    plt.ylabel('Gestures per Session')
    plt.show()

    # Plot Time_in_sec_per_session vs Sessions_per_month
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='Time_in_sec_per_session', y='Sessions_per_month', hue='Cluster',
                    data=original_data.join(data['Cluster']), palette='viridis')
    plt.title('Clustering of Users')
    plt.xlabel('Time in Seconds per Session')
    plt.ylabel('Sessions per Month')
    plt.show()
