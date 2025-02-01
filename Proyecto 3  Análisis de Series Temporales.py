# Importar librerías necesarias
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.statespace.sarimax import SARIMAX
from fbprophet import Prophet
from pmdarima import auto_arima
from sklearn.metrics import mean_squared_error, mean_absolute_error

# Cargar el dataset Air Passengers
url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/airline-passengers.csv"
df = pd.read_csv(url, parse_dates=['Month'], index_col='Month')

# Renombrar columnas para Prophet
df = df.rename(columns={'Passengers': 'y'})
df['ds'] = df.index

# Exploración inicial de los datos
print("Primeras filas del dataset:")
print(df.head())

# Visualización de la serie temporal
plt.figure(figsize=(10, 6))
plt.plot(df['y'], label='Pasajeros')
plt.title('Número Mensual de Pasajeros de Aerolíneas (1949-1960)')
plt.xlabel('Fecha')
plt.ylabel('Número de Pasajeros')
plt.legend()
plt.show()

# Descomposición de la serie temporal
decomposition = seasonal_decompose(df['y'], model='multiplicative')
decomposition.plot()
plt.suptitle('Descomposición de la Serie Temporal')
plt.show()

# Prueba de estacionariedad (Dickey-Fuller)
def test_stationarity(timeseries):
    result = adfuller(timeseries)
    print('Estadística ADF:', result[0])
    print('Valor p:', result[1])
    print('Valores críticos:')
    for key, value in result[4].items():
        print(f'   {key}: {value}')

print("\nPrueba de estacionariedad:")
test_stationarity(df['y'])

# Diferenciación para hacer la serie estacionaria
df['y_diff'] = df['y'].diff().dropna()
print("\nPrueba de estacionariedad después de la diferenciación:")
test_stationarity(df['y_diff'])

# Visualización de ACF y PACF
plt.figure(figsize=(12, 6))
plt.subplot(121)
plot_acf(df['y_diff'].dropna(), lags=40, ax=plt.gca())
plt.subplot(122)
plot_pacf(df['y_diff'].dropna(), lags=40, ax=plt.gca())
plt.suptitle('ACF y PACF de la Serie Diferenciada')
plt.show()

# Optimización de hiperparámetros para ARIMA usando auto_arima
auto_model = auto_arima(df['y'], seasonal=True, m=12, stepwise=True, trace=True)
print("\nMejores parámetros ARIMA/SARIMA encontrados:")
print(auto_model.summary())

# Dividir el dataset en entrenamiento y prueba
train_size = int(len(df) * 0.8)
train, test = df['y'][:train_size], df['y'][train_size:]

# Ajustar el modelo SARIMA con los parámetros encontrados
sarima_model = SARIMAX(train, order=auto_model.order, seasonal_order=auto_model.seasonal_order)
sarima_fit = sarima_model.fit()
print(sarima_fit.summary())

# Predicciones con SARIMA
predictions = sarima_fit.forecast(steps=len(test))
df['SARIMA_Predictions'] = np.nan
df['SARIMA_Predictions'].iloc[train_size:] = predictions

# Evaluación del modelo SARIMA
mse_sarima = mean_squared_error(test, predictions)
mae_sarima = mean_absolute_error(test, predictions)
print(f"\nError Cuadrático Medio (MSE) - SARIMA: {mse_sarima:.2f}")
print(f"Error Absoluto Medio (MAE) - SARIMA: {mae_sarima:.2f}")

# Visualización de las predicciones SARIMA
plt.figure(figsize=(10, 6))
plt.plot(df['y'], label='Datos Reales')
plt.plot(df['SARIMA_Predictions'], label='Predicciones SARIMA', linestyle='--')
plt.title('Predicciones SARIMA vs Datos Reales')
plt.xlabel('Fecha')
plt.ylabel('Número de Pasajeros')
plt.legend()
plt.show()

# Validación cruzada para Prophet
def prophet_cross_validation(train, test):
    errors = []
    for i in range(len(test)):
        # Entrenar el modelo con los datos hasta el punto actual
        prophet_model = Prophet(seasonality_mode='multiplicative')
        prophet_model.fit(train)
        
        # Predecir el siguiente punto
        future = prophet_model.make_future_dataframe(periods=1)
        forecast = prophet_model.predict(future)
        predicted_value = forecast['yhat'].iloc[-1]
        
        # Calcular el error
        true_value = test.iloc[i]
        errors.append(abs(true_value - predicted_value))
        
        # Actualizar el conjunto de entrenamiento
        train = pd.concat([train, test.iloc[[i]]])
    
    return np.mean(errors)

print("\nRealizando validación cruzada para Prophet...")
mae_prophet_cv = prophet_cross_validation(df[['ds', 'y']].iloc[:train_size], df[['ds', 'y']].iloc[train_size:])
print(f"Error Absoluto Medio (MAE) - Prophet (CV): {mae_prophet_cv:.2f}")

# Modelado con Prophet
prophet_model = Prophet(seasonality_mode='multiplicative')
prophet_model.fit(df[['ds', 'y']].dropna())

# Crear un dataframe futuro para predicciones
future = prophet_model.make_future_dataframe(periods=len(test))
forecast = prophet_model.predict(future)

# Evaluación del modelo Prophet
prophet_predictions = forecast['yhat'].iloc[train_size:]
mse_prophet = mean_squared_error(test, prophet_predictions)
mae_prophet = mean_absolute_error(test, prophet_predictions)
print(f"\nError Cuadrático Medio (MSE) - Prophet: {mse_prophet:.2f}")
print(f"Error Absoluto Medio (MAE) - Prophet: {mae_prophet:.2f}")

# Visualización de las predicciones Prophet
plt.figure(figsize=(10, 6))
plt.plot(df['y'], label='Datos Reales')
plt.plot(forecast['ds'], forecast['yhat'], label='Predicciones Prophet', linestyle='--')
plt.fill_between(forecast['ds'], forecast['yhat_lower'], forecast['yhat_upper'], alpha=0.2)
plt.title('Predicciones Prophet vs Datos Reales')
plt.xlabel('Fecha')
plt.ylabel('Número de Pasajeros')
plt.legend()
plt.show()

# Comparación de ambos modelos
plt.figure(figsize=(10, 6))
plt.plot(df['y'], label='Datos Reales')
plt.plot(df['SARIMA_Predictions'], label='Predicciones SARIMA', linestyle='--')
plt.plot(forecast['ds'], forecast['yhat'], label='Predicciones Prophet', linestyle='--')
plt.title('Comparación de Predicciones: SARIMA vs Prophet')
plt.xlabel('Fecha')
plt.ylabel('Número de Pasajeros')
plt.legend()
plt.show()