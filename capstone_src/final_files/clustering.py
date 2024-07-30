#%%
import pandas as pd

# Load the fact_users dataset
fact_users = pd.read_csv('fact_users.csv')

# Generate the Time_in_sec_per_session column
fact_users['Time_in_sec_per_session'] = fact_users['Time in app Seconds'] / fact_users['Sessions']

# Generate the Gestures_per_session column
fact_users['Gestures_per_session'] = fact_users['Gestures'] / fact_users['Sessions']

# Generate the Sessions_per_month column
fact_users['Sessions_per_month'] = fact_users['Sessions'] / 3

# Remove outliers
fact_users = fact_users[(fact_users['Time_in_sec_per_session'] < 4000) &
                        (fact_users['Gestures_per_session'] < 1250 ) &
                        (fact_users['Sessions_per_month'] < 2000)]

# Check for missing values in the new columns
print("Missing values per column in new columns:")
print(fact_users[['Sessions_per_month', 'Gestures_per_session', 'Time_in_sec_per_session']].isnull().sum())

# Treat missing values by filling with the median
fact_users['Sessions_per_month'].fillna(fact_users['Sessions_per_month'].median(), inplace=True)
fact_users['Gestures_per_session'].fillna(fact_users['Gestures_per_session'].median(), inplace=True)
fact_users['Time_in_sec_per_session'].fillna(fact_users['Time_in_sec_per_session'].median(), inplace=True)

fact_users.head()

#%%
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from clustering_utils import elbow_method, perform_clustering, plot_clusters, plot_weighted_clusters

#%%
# Set parameters
X = fact_users[['Time_in_sec_per_session', 'Gestures_per_session', 'Sessions_per_month']]

#################################################################################################

#%%

# Determine the optimal number of clusters using the Elbow method on the training set
elbow_method(X, max_clusters=10, random_state=42)

#%%

# Clustering 1

# Same weight for all

# Set number of clusters
optimal_clusters = 4  # Based on Elbow method and business goals

#%%
fact_users_with_clusters = perform_clustering(X, optimal_clusters)
plot_clusters(fact_users_with_clusters)
fact_users_with_clusters.to_csv('fact_users_with_clusters_1.csv', index=False)
#%%
#%
#################################################################################################

#%%

# Clustering 2

# Increase the weight of Gestures_per_session
weight_factor_gestures = 15
fact_users['Weighted_Gestures_per_session'] = fact_users['Gestures_per_session'] * weight_factor_gestures

#%%
# Increase the weight of Sessions_per_month
weight_factor_sessions = 20
fact_users['Weighted_Sessions_per_month'] = fact_users['Sessions_per_month'] * weight_factor_sessions

# Select relevant columns for clustering
X = fact_users[['Time_in_sec_per_session', 'Weighted_Gestures_per_session', 'Weighted_Sessions_per_month']]

#%%
# Determine the optimal number of clusters using the Elbow method
elbow_method(X, max_clusters=10, random_state=42)

#%%
# Perform clustering with new weights

fact_users_with_clusters = perform_clustering(X, optimal_clusters)
#%%
plot_weighted_clusters(fact_users_with_clusters, fact_users)


# Save the dataset with clusters
fact_users_with_clusters.to_csv('fact_users_with_clusters_2.csv', index=False)


#################################################################################################


#%%

# Clustering 3

# Increase the weight of Gestures_per_session
weight_factor_gestures = 15
fact_users['Weighted_Gestures_per_session'] = fact_users['Gestures_per_session'] * weight_factor_gestures

# Increase the weight of Sessions_per_month
weight_factor_sessions = 200
fact_users['Weighted_Sessions_per_month'] = fact_users['Sessions_per_month'] * weight_factor_sessions

# Select relevant columns for clustering
X = fact_users[['Time_in_sec_per_session', 'Weighted_Gestures_per_session', 'Weighted_Sessions_per_month']]

#%%
# Determine the optimal number of clusters using the Elbow method
#elbow_method(X, max_clusters=10, random_state=42)

#%%
# Perform clustering with new weights

fact_users_with_clusters = perform_clustering(X, optimal_clusters)
plot_weighted_clusters(fact_users_with_clusters, fact_users)
# Save the dataset with clusters
fact_users_with_clusters.to_csv('fact_users_with_clusters_3.csv', index=False)

#########################################################################################

# %%

# Clustering 4

# Increase the weight of Gestures_per_session
weight_factor_gestures = 150
fact_users['Weighted_Gestures_per_session'] = fact_users['Gestures_per_session'] * weight_factor_gestures

# Increase the weight of Sessions_per_month
weight_factor_sessions = 20
fact_users['Weighted_Sessions_per_month'] = fact_users['Sessions_per_month'] * weight_factor_sessions

# Select relevant columns for clustering
X = fact_users[['Time_in_sec_per_session', 'Weighted_Gestures_per_session', 'Weighted_Sessions_per_month']]

#%%
# Determine the optimal number of clusters using the Elbow method
#elbow_method(X, max_clusters=10, random_state=42)

#%%
# Perform clustering with new weights

fact_users_with_clusters = perform_clustering(X, optimal_clusters)
plot_weighted_clusters(fact_users_with_clusters, fact_users)
#%%
# Save the dataset with clusters
fact_users_with_clusters.to_csv('fact_users_with_clusters_4.csv', index=False)
# %%

#########################################################################################
