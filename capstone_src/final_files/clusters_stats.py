# %%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Function to calculate cluster proportions and statistics
def calculate_proportions_and_stats(df, clustering_process):
    # Calculate the proportion of each cluster
    cluster_counts = df['Cluster'].value_counts()
    total_samples = df.shape[0]
    cluster_proportions = cluster_counts / total_samples
    cluster_proportions_df = cluster_proportions.reset_index()
    cluster_proportions_df.columns = ['Cluster', f'Proportion_Clustering_{clustering_process}']
    
    # Add a new column for Time in Minutes per Session
    df['Time_in_min_per_session'] = df['Time_in_sec_per_session'] / 60
    
    # Calculate statistics for each cluster
    cluster_stats = df.groupby('Cluster').agg({
        'Time_in_sec_per_session': ['mean', 'median', 'max', 'min'],
        'Time_in_min_per_session': ['mean', 'median', 'max', 'min'],
        'Gestures_per_session': ['mean', 'median', 'max', 'min'],
        'Sessions_per_month': ['mean', 'median', 'max', 'min']
    })
    
    # Rename the columns
    cluster_stats.columns = ['_'.join(col).strip() for col in cluster_stats.columns.values]
    cluster_stats.reset_index(inplace=True)
    
    # Combine proportions and statistics
    combined_stats = pd.merge(cluster_proportions_df, cluster_stats, on='Cluster', how='outer')
    combined_stats['Clustering_Process'] = clustering_process
    
    # Save the combined DataFrame to a CSV file
    combined_stats.to_csv(f'combined_cluster_statistics_{clustering_process}.csv', index=False)
    
    # Display the combined DataFrame
    print(f"Combined statistics for Clustering Process {clustering_process}:")
    print(combined_stats)
    
    return combined_stats



# Function to calculate weighted cluster proportions and statistics
def calculate_weighted_proportions_and_stats(clustered_df, original_df, clustering_process):

    # Merge the original dataset with the clustered data on the index
    df = clustered_df.join(original_df.drop(columns=['Cluster','Time_in_sec_per_session'])) # getting original gestures per session and session per month
    
    # Calculate the proportion of each cluster
    cluster_counts = df['Cluster'].value_counts()
    total_samples = df.shape[0]
    cluster_proportions = cluster_counts / total_samples
    cluster_proportions_df = cluster_proportions.reset_index()
    cluster_proportions_df.columns = ['Cluster', f'Proportion_Clustering_{clustering_process}']
    
    # Add a new column for Time in Minutes per Session
    df['Time_in_min_per_session'] = df['Time_in_sec_per_session'] / 60
    
    # Calculate statistics for each cluster
    cluster_stats = df.groupby('Cluster').agg({
        'Time_in_sec_per_session': ['mean', 'median', 'max', 'min'],
        'Time_in_min_per_session': ['mean', 'median', 'max', 'min'],
        'Gestures_per_session': ['mean', 'median', 'max', 'min'],
        'Sessions_per_month': ['mean', 'median', 'max', 'min']
    })
    
    # Rename the columns
    cluster_stats.columns = ['_'.join(col).strip() for col in cluster_stats.columns.values]
    cluster_stats.reset_index(inplace=True)
    
    # Combine proportions and statistics
    combined_stats = pd.merge(cluster_proportions_df, cluster_stats, on='Cluster', how='outer')
    combined_stats['Clustering_Process'] = clustering_process
    
    # Save the combined DataFrame to a CSV file
    combined_stats.to_csv(f'combined_weighted_cluster_statistics_{clustering_process}.csv', index=False)
    
    # Display the combined DataFrame
    print(f"Combined weighted statistics for Clustering Process {clustering_process}:")
    print(combined_stats)
    
    return combined_stats

#%%
# Load the datasets with clusters
fact_users_with_clusters_1 = pd.read_csv('fact_users_with_clusters_1.csv')
fact_users_with_clusters_2 = pd.read_csv('fact_users_with_clusters_2.csv')
fact_users_with_clusters_3 = pd.read_csv('fact_users_with_clusters_3.csv')
fact_users_with_clusters_4 = pd.read_csv('fact_users_with_clusters_4.csv')


#%%
# Calculate proportions and statistics for each clustering process
combined_stats_1 = calculate_proportions_and_stats(fact_users_with_clusters_1, 1)

#%%
combined_stats_2 = calculate_weighted_proportions_and_stats(fact_users_with_clusters_2,fact_users_with_clusters_1.iloc[:, :-1] ,2)
combined_stats_3 = calculate_weighted_proportions_and_stats(fact_users_with_clusters_3,fact_users_with_clusters_1.iloc[:, :-1], 3)
combined_stats_4 = calculate_weighted_proportions_and_stats(fact_users_with_clusters_4, fact_users_with_clusters_1.iloc[:, :-1],4)


#%%
# Visualize the proportions for each clustering process
for i, proportions in enumerate([combined_stats_1, combined_stats_2, combined_stats_3, combined_stats_4], start=1):
    plt.figure(figsize=(10, 6))
    proportions.set_index('Cluster')[f'Proportion_Clustering_{i}'].plot(kind='bar')
    plt.title(f'Proportion of Each Cluster (Clustering {i})')
    plt.xlabel('Cluster')
    plt.ylabel('Proportion')
    plt.tight_layout()
    plt.show()
# %%
