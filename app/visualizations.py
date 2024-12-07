import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA
from sklearn.cluster import DBSCAN

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


import matplotlib
matplotlib.use('Agg')  # Force non-GUI backend


# Generate 20 unique colors using a colormap
def generate_colors(num_colors):
    colors = list(mcolors.TABLEAU_COLORS.values())  # Start with Tableau colors
    while len(colors) < num_colors:
        # Extend the color list with additional distinct colors
        colors.extend(plt.cm.tab20.colors)
    return colors[:num_colors]


def visualize_clustering(df):
    if df.empty:
        raise ValueError("The dataset is empty. Cannot create clustering visualization.")
    
    if len(df) < 3:
        raise ValueError("Insufficient data for clustering. At least 3 rows are required.")

    # 'date_time': fields[0],
    # 'incident_number': fields[1],
    # 'location': fields[2],
    # 'nature': fields[3],
    # 'incident_ori': fields[4]

    # Encode the 'nature' column
    le = LabelEncoder()
    df['nature_encoded'] = le.fit_transform(df['nature'])
    df['location_encoded'] = le.fit_transform(df['location'])
    df['incident_ori_encoded'] = le.fit_transform(df['incident_ori'])
    
    # datetime, creating a category of 4 parts of the day basing on the hours
    df['date_time'] = pd.to_datetime(df['date_time'])
    df['date_time_encoded'] = df['date_time'].apply(lambda x: 'morning' if 5 <= x.hour < 12 else 'afternoon' if 12 <= x.hour < 17 else 'evening' if 17 <= x.hour < 21 else 'night')

    #label encoding the date_time_encoded
    df['date_time_encoded'] = le.fit_transform(df['date_time_encoded'])


    # Apply KMeans clustering
    kmeans = KMeans(n_clusters=4, random_state=42)
    # Apply DBSCAN clustering
    dbscan = DBSCAN(eps=7, min_samples=5)
    df['cluster'] = dbscan.fit_predict(df[['nature_encoded', 'location_encoded', 'incident_ori_encoded', 'date_time_encoded']])
    #df['cluster'] = kmeans.fit_predict(df[['nature_encoded', 'location_encoded', 'incident_ori_encoded', 'date_time_encoded']])

    print(df['cluster'].value_counts())

    # Perform PCA on the encoded columns
    pca = PCA(n_components=2)
    principal_components = pca.fit_transform(df[['nature_encoded', 'location_encoded', 'incident_ori_encoded', 'date_time_encoded']])
    df['pca1'] = principal_components[:, 0]
    df['pca2'] = principal_components[:, 1]

    # Scatter plot for PCA components
    plt.figure(figsize=(10, 6))

    # Generate 20 unique colors
    num_clusters = df['cluster'].nunique()
    colors = generate_colors(num_clusters)

    for i, cluster_id in enumerate(df['cluster'].unique()):
        cluster_data = df[df['cluster'] == cluster_id]
        plt.scatter(
            cluster_data['pca1'], 
            cluster_data['pca2'], 
            color=colors[i % len(colors)],  # Assign a unique color to each cluster
            label=f'Cluster {cluster_id}',
            s=50,  # Size of points
            edgecolor='k'  # Add black edge to points
        )

    plt.title("Clustering Visualization with PCA")
    plt.xlabel("PCA Component 1")
    plt.ylabel("PCA Component 2")
    plt.legend(
        title="Clusters", 
        loc='center left', 
        bbox_to_anchor=(1, 0.5),  # Position legend outside the plot
        fontsize='small'
    )
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    
    return base64.b64encode(img.getvalue()).decode()

    # # Check the quality of clustering using Silhouette Score
    # silhouette_avg = silhouette_score(df[['nature_encoded']], df['cluster'])
    # print(f"Silhouette Score: {silhouette_avg:.2f}")
    
    # if silhouette_avg < 0.5:
    #     print("Warning: The Silhouette Score is low, indicating poor cluster separation. Consider adjusting the number of clusters or features.")

    # # Analyze cluster content
    # print("Cluster Contents:")
    # for cluster_id in df['cluster'].unique():
    #     cluster_data = df[df['cluster'] == cluster_id]
    #     print(f"Cluster {cluster_id}:")
    #     print(cluster_data['nature'].value_counts())
    
    # # Scatter plot for clustering
    # plt.figure(figsize=(10, 6))
    # sns.scatterplot(
    #     data=df,
    #     x='nature_encoded',
    #     y=df.index,  # Use index or another meaningful column
    #     hue='cluster',
    #     palette='viridis'
    # )
    # plt.title("KMeans Clustering of Incidents")
    # plt.xlabel("Encoded Nature")
    # plt.ylabel("Incident Index")
    # plt.legend(title="Cluster")

    # img = io.BytesIO()
    # plt.savefig(img, format='png')
    # img.seek(0)
    # return base64.b64encode(img.getvalue()).decode()


# def visualize_bar_graph(df):
#     # Group by "Incident ORI" and count occurrences
#     ori_counts = df['incident_ori'].value_counts()

#     # Create a bar plot
#     plt.figure(figsize=(10, 6))
#     ori_counts.plot(kind='bar', color='lightcoral', edgecolor='black')
#     plt.title('Frequency of Incidents by ORI', fontsize=16)
#     plt.xlabel('Incident ORI', fontsize=14)
#     plt.ylabel('Frequency', fontsize=14)
#     plt.xticks(rotation=45, ha='right', fontsize=10)
#     plt.grid(axis='y', linestyle='--', alpha=0.7)

#     # Save the plot to a buffer
#     img = io.BytesIO()
#     plt.savefig(img, format='png')
#     img.seek(0)
#     plt.close()  # Close the plot to avoid display issues
#     return base64.b64encode(img.getvalue()).decode()


def visualize_bar_graph(df):
    # Bar plot for frequency of incidents by time of day
    time_of_day_counts = df['date_time_encoded'].value_counts().sort_index()
    time_of_day_labels = ['Morning', 'Afternoon', 'Evening', 'Night']
    time_of_day_counts.index = time_of_day_labels
    plt.figure(figsize=(10, 6))
    time_of_day_counts.plot(kind='bar', color='skyblue', edgecolor='black')
    plt.title('Frequency of Incidents by Time of Day', fontsize=16)
    plt.xlabel('Time of Day', fontsize=14)
    plt.ylabel('Frequency', fontsize=14)
    plt.xticks(rotation=0, fontsize=10)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    return base64.b64encode(img.getvalue()).decode()



def visualize_pie_chart(df):
    """
    Creates a pie chart for the nature of incidents and handles legend positioning.
    """
    # Count incidents by nature
    nature_counts = df['nature'].value_counts()

    # Combine small categories into 'Other'
    threshold = 0.03 * nature_counts.sum()
    small_categories = nature_counts[nature_counts < threshold].index
    nature_counts = nature_counts.groupby(lambda x: x if x not in small_categories else 'Other').sum()

    # Generate the pie chart
    plt.figure(figsize=(8, 6))
    wedges, texts, autotexts = plt.pie(
        nature_counts,
        autopct='%1.1f%%',
        startangle=90,
        textprops={'fontsize': 8},
    )
    plt.legend(
        wedges,
        nature_counts.index,
        title="Nature",
        loc="center left",
        bbox_to_anchor=(1, 0, 0.5, 1)
    )
    plt.axis('equal')  # Equal aspect ratio ensures the pie chart is circular

    # Save the plot to a buffer, ensuring the legend is included
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    plt.close()  # Close the plot to avoid memory issues
    return base64.b64encode(img.getvalue()).decode()

