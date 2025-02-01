# Importar librerías necesarias
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar el dataset Titanic
url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
df = pd.read_csv(url)

# Exploración inicial de los datos
print("Primeras filas del dataset:")
print(df.head())

print("\nInformación del dataset:")
print(df.info())

print("\nEstadísticas descriptivas:")
print(df.describe())

# Verificar valores nulos
print("\nValores nulos por columna:")
print(df.isnull().sum())

# Limpieza de datos
# Rellenar valores nulos en 'Age' con la mediana
df['Age'].fillna(df['Age'].median(), inplace=True)

# Rellenar valores nulos en 'Embarked' con la moda
df['Embarked'].fillna(df['Embarked'].mode()[0], inplace=True)

# Eliminar la columna 'Cabin' (demasiados valores nulos)
df.drop('Cabin', axis=1, inplace=True)

# Verificar valores nulos después de la limpieza
print("\nValores nulos después de la limpieza:")
print(df.isnull().sum())

# Análisis de la supervivencia
print("\nDistribución de la supervivencia:")
print(df['Survived'].value_counts())

# Visualización de la distribución de la supervivencia
plt.figure(figsize=(6, 4))
sns.countplot(x='Survived', data=df, palette='Set2')
plt.title('Distribución de la Supervivencia')
plt.xlabel('Sobrevivió (1: Sí, 0: No)')
plt.ylabel('Cantidad')
plt.show()

# Distribución de la edad por supervivencia
plt.figure(figsize=(8, 6))
sns.histplot(data=df, x='Age', hue='Survived', kde=True, palette='Set1', bins=20)
plt.title('Distribución de la Edad por Supervivencia')
plt.xlabel('Edad')
plt.ylabel('Frecuencia')
plt.show()

# Distribución de la tarifa pagada por supervivencia
plt.figure(figsize=(8, 6))
sns.boxplot(x='Survived', y='Fare', data=df, palette='Set3')
plt.title('Distribución de la Tarifa por Supervivencia')
plt.xlabel('Sobrevivió (1: Sí, 0: No)')
plt.ylabel('Tarifa')
plt.show()

# Relación entre clase de pasajero y supervivencia
plt.figure(figsize=(8, 6))
sns.countplot(x='Pclass', hue='Survived', data=df, palette='Set2')
plt.title('Supervivencia por Clase de Pasajero')
plt.xlabel('Clase de Pasajero')
plt.ylabel('Cantidad')
plt.legend(title='Sobrevivió', loc='upper right')
plt.show()

# Relación entre género y supervivencia
plt.figure(figsize=(8, 6))
sns.countplot(x='Sex', hue='Survived', data=df, palette='Set1')
plt.title('Supervivencia por Género')
plt.xlabel('Género')
plt.ylabel('Cantidad')
plt.legend(title='Sobrevivió', loc='upper right')
plt.show()

# Correlación entre variables numéricas
plt.figure(figsize=(8, 6))
sns.heatmap(df.corr(), annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Mapa de Calor de Correlaciones')
plt.show()