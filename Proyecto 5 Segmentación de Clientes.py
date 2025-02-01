# Importar librerías necesarias
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from mpl_toolkits.mplot3d import Axes3D  # Para gráficos 3D

# Cargar el dataset de Kaggle (Mall Customer Segmentation Data)
url = "https://raw.githubusercontent.com/plotly/datasets/master/Mall_Customers.csv"
df = pd.read_csv(url)

# Mostrar las primeras filas del dataset
print("Dataset de clientes del centro comercial:")
print(df.head())

# Seleccionar características para el clustering
# Usaremos 'Annual Income (k$)', 'Spending Score (1-100)', y 'Age'
X = df[['Annual Income (k$)', 'Spending Score (1-100)', 'Age']]

# Estandarizar las características
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Determinar el número óptimo de clusters usando el coeficiente de silueta
silhouette_scores = []
for i in range(2, 11):  # Probamos de 2 a 10 clusters
    kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42)
    cluster_labels = kmeans.fit_predict(X_scaled)
    silhouette_avg = silhouette_score(X_scaled, cluster_labels)
    silhouette_scores.append(silhouette_avg)
    print(f"Coeficiente de silueta para {i} clusters: {silhouette_avg:.2f}")

# Graficar los coeficientes de silueta
plt.figure(figsize=(8, 5))
plt.plot(range(2, 11), silhouette_scores, marker='o', linestyle='--')
plt.title('Coeficiente de Silueta para Determinar el Número Óptimo de Clusters')
plt.xlabel('Número de Clusters')
plt.ylabel('Coeficiente de Silueta')
plt.show()

# Aplicar K-Means con el número óptimo de clusters (elegimos 5 basado en el coeficiente de silueta)
n_clusters = 5
kmeans = KMeans(n_clusters=n_clusters, init='k-means++', random_state=42)
df['Cluster'] = kmeans.fit_predict(X_scaled)

# Mostrar los resultados de la segmentación
print("\nSegmentación de clientes:")
print(df[['CustomerID', 'Annual Income (k$)', 'Spending Score (1-100)', 'Age', 'Cluster']])

# Evaluar la calidad del clustering con el coeficiente de silueta
silhouette_avg = silhouette_score(X_scaled, df['Cluster'])
print(f"\nCoeficiente de Silueta Final: {silhouette_avg:.2f}")

# Visualización 3D de los clusters
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
for cluster in range(n_clusters):
    ax.scatter(df[df['Cluster'] == cluster]['Annual Income (k$)'],
               df[df['Cluster'] == cluster]['Spending Score (1-100)'],
               df[df['Cluster'] == cluster]['Age'],
               label=f'Cluster {cluster}')
ax.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], kmeans.cluster_centers_[:, 2],
           s=200, c='red', marker='X', label='Centroides')
ax.set_title('Segmentación de Clientes (3D)')
ax.set_xlabel('Ingreso Anual (k$)')
ax.set_ylabel('Puntaje de Gastos (1-100)')
ax.set_zlabel('Edad')
ax.legend()
plt.show()