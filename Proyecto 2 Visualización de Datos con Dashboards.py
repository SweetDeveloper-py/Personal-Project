# Pasos para ejecutar>

#Guardar el código en un archivo Python, por ejemplo, dashboard.py.
#Ejecuta el archivo con Python: python dashboard.py.
#Abre tu navegador y ve a http://127.0.0.1:8050/ para ver el dashboard en acción.

# Importar librerías necesarias
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Cargar el dataset Titanic
url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
df = pd.read_csv(url)

# Limpieza básica de datos
df['Age'].fillna(df['Age'].median(), inplace=True)
df['Embarked'].fillna(df['Embarked'].mode()[0], inplace=True)
df.drop('Cabin', axis=1, inplace=True)

# Crear una columna para el tamaño de la familia
df['FamilySize'] = df['SibSp'] + df['Parch'] + 1

# Crear una columna para agrupar la edad en rangos
df['AgeGroup'] = pd.cut(df['Age'], bins=[0, 18, 35, 50, 100], labels=['0-18', '19-35', '36-50', '51+'])

# Inicializar la aplicación Dash
app = dash.Dash(__name__)

# Diseño del dashboard
app.layout = html.Div([
    html.H1("Dashboard de Análisis del Titanic", style={'textAlign': 'center', 'color': '#2c3e50'}),
    
    # Filtros interactivos
    html.Div([
        html.Label("Selecciona el género:"),
        dcc.Dropdown(
            id='gender-selector',
            options=[
                {'label': 'Todos', 'value': 'all'},
                {'label': 'Masculino', 'value': 'male'},
                {'label': 'Femenino', 'value': 'female'}
            ],
            value='all',  # Valor por defecto
            style={'width': '50%', 'margin-bottom': '20px'}
        ),
        
        html.Label("Selecciona el rango de edad:"),
        dcc.RangeSlider(
            id='age-slider',
            min=0,
            max=80,
            step=1,
            marks={i: str(i) for i in range(0, 81, 10)},
            value=[0, 80],  # Valor por defecto
            tooltip={"placement": "bottom", "always_visible": True}
        )
    ], style={'padding': '20px', 'border': '1px solid #ddd', 'border-radius': '5px', 'margin-bottom': '20px'}),
    
    # Dropdown para seleccionar la variable a analizar
    html.Label("Selecciona una variable para analizar:"),
    dcc.Dropdown(
        id='variable-selector',
        options=[
            {'label': 'Clase de Pasajero (Pclass)', 'value': 'Pclass'},
            {'label': 'Género (Sex)', 'value': 'Sex'},
            {'label': 'Puerto de Embarque (Embarked)', 'value': 'Embarked'},
            {'label': 'Grupo de Edad (AgeGroup)', 'value': 'AgeGroup'},
            {'label': 'Tamaño de la Familia (FamilySize)', 'value': 'FamilySize'}
        ],
        value='Pclass',  # Valor por defecto
        style={'width': '50%', 'margin-bottom': '20px'}
    ),
    
    # Gráfico de barras para la distribución de la variable seleccionada
    dcc.Graph(id='bar-plot'),
    
    # Gráfico de dispersión para edad vs. tarifa, coloreado por supervivencia
    dcc.Graph(id='scatter-plot'),
    
    # Gráfico de caja para comparar la tarifa por clase de pasajero
    dcc.Graph(id='box-plot'),
    
    # Gráfico de pie para la distribución de la supervivencia
    dcc.Graph(id='pie-plot')
])

# Callback para actualizar los gráficos basados en la selección del usuario
@app.callback(
    [Output('bar-plot', 'figure'),
     Output('scatter-plot', 'figure'),
     Output('box-plot', 'figure'),
     Output('pie-plot', 'figure')],
    [Input('variable-selector', 'value'),
     Input('gender-selector', 'value'),
     Input('age-slider', 'value')]
)
def update_graphs(selected_variable, selected_gender, age_range):
    # Filtrar los datos según el género y el rango de edad seleccionados
    filtered_df = df[(df['Age'] >= age_range[0]) & (df['Age'] <= age_range[1])]
    if selected_gender != 'all':
        filtered_df = filtered_df[filtered_df['Sex'] == selected_gender]
    
    # Gráfico de barras: Distribución de la variable seleccionada
    bar_fig = px.histogram(filtered_df, x=selected_variable, color='Survived',
                           title=f'Distribución de {selected_variable} por Supervivencia',
                           labels={selected_variable: selected_variable, 'count': 'Cantidad'},
                           barmode='group')
    
    # Gráfico de dispersión: Edad vs. Tarifa, coloreado por supervivencia
    scatter_fig = px.scatter(filtered_df, x='Age', y='Fare', color='Survived',
                             title='Edad vs. Tarifa (Coloreado por Supervivencia)',
                             labels={'Age': 'Edad', 'Fare': 'Tarifa'})
    
    # Gráfico de caja: Tarifa por clase de pasajero
    box_fig = px.box(filtered_df, x='Pclass', y='Fare', color='Survived',
                     title='Distribución de la Tarifa por Clase de Pasajero',
                     labels={'Pclass': 'Clase de Pasajero', 'Fare': 'Tarifa'})
    
    # Gráfico de pie: Distribución de la supervivencia
    pie_fig = px.pie(filtered_df, names='Survived', title='Distribución de la Supervivencia',
                     labels={'Survived': 'Sobrevivió', 'value': 'Cantidad'})
    
    return bar_fig, scatter_fig, box_fig, pie_fig

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)