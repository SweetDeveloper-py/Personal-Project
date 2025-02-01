# Importar librerías necesarias
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE  # Para balanceo de clases

# Cargar el dataset
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00222/bank-additional.zip"
data = pd.read_csv(url, sep=";")

# Exploración rápida de los datos
print(data.head())
print(data.info())

# Preprocesamiento de datos
# Convertir variables categóricas a numéricas
label_encoders = {}
for column in data.select_dtypes(include=['object']).columns:
    le = LabelEncoder()
    data[column] = le.fit_transform(data[column])
    label_encoders[column] = le

# Separar características (X) y variable objetivo (y)
X = data.drop("y", axis=1)  # Características
y = data["y"]  # Variable objetivo (1: Suscrito, 0: No suscrito)

# Dividir el dataset en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Balanceo de clases usando SMOTE
smote = SMOTE(random_state=42)
X_train_balanced, y_train_balanced = smote.fit_resample(X_train, y_train)

# Optimización de hiperparámetros con GridSearchCV
param_grid = {
    'n_estimators': [50, 100, 200],  # Número de árboles
    'max_depth': [None, 10, 20],     # Profundidad máxima del árbol
    'min_samples_split': [2, 5, 10], # Mínimo de muestras para dividir un nodo
    'class_weight': [None, 'balanced']  # Balanceo de clases
}

model = RandomForestClassifier(random_state=42)
grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=3, scoring='accuracy', n_jobs=-1)
grid_search.fit(X_train_balanced, y_train_balanced)

# Mejores hiperparámetros
print("Mejores hiperparámetros:", grid_search.best_params_)

# Entrenar el modelo con los mejores hiperparámetros
best_model = grid_search.best_estimator_
best_model.fit(X_train_balanced, y_train_balanced)

# Realizar predicciones
y_pred = best_model.predict(X_test)

# Evaluar el modelo
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))

# Importancia de las características
feature_importances = pd.Series(best_model.feature_importances_, index=X.columns)
print("Feature Importances:\n", feature_importances.sort_values(ascending=False))

# Selección de características basada en importancia
selected_features = feature_importances[feature_importances > 0.01].index
print("Características seleccionadas:\n", selected_features)