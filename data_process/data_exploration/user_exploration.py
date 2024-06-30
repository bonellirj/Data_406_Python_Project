import pandas as pd

import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans




def anlise_1(db_conn):

    query = "SELECT top 10 * FROM dbo.[Users-21-05-24]"

    data_frame = pd.read_sql(query, db_conn)

    if data_frame is not None:
        # print(data_frame.head())
        # print(data_frame.info())
        # print(data_frame.describe())
        # print(data_frame.nunique())
        
        # plt.hist(data_frame['Time_in_seconds'], bins=30, color='blue', edgecolor='black')

        # plt.title('Histograma de Time in Seconds')
        # plt.xlabel('Time in Seconds')
        # plt.ylabel('Frequencia')

        # plt.show()
        
        sns.set(style="whitegrid")

        plt.figure(figsize=(10, 6))
        
        sns.histplot(data_frame['Time_in_seconds'], color="skyblue", binwidth=100, kde=True)

        plt.title('Histograma de Time in Seconds', fontsize=15)
        plt.xlabel('Time in Seconds', fontsize=12)
        plt.ylabel('Frequencia', fontsize=12)

        plt.show()
        

        kmeans = KMeans(n_clusters=4) 
        data_frame['Cluster'] = kmeans.fit_predict(data_frame[['Time_in_seconds', 'Gestures_as_int']])

        sns.set(style="whitegrid")
        plt.figure(figsize=(10, 6))
        palette = sns.color_palette('hsv', n_colors=len(data_frame['Cluster'].unique())) 

        scatter = sns.scatterplot(data=data_frame, x='Time_in_seconds', y='Gestures_as_int', hue='Cluster', palette=palette, s=100, legend=None)
        plt.title('Clusters de Usuarios por Tempo e Gestos', fontsize=15)
        plt.xlabel('Time in Seconds', fontsize=12)
        plt.ylabel('Gestures as Integer', fontsize=12)

        centers = kmeans.cluster_centers_
        plt.scatter(centers[:, 0], centers[:, 1], c='red', s=200, alpha=0.75, marker='X')

        plt.show()
    
    else :
        print("No data returned")


