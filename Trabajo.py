import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Cargar datos
file_path = 'shopping_trends.csv'
data = pd.read_csv(file_path)

st.title("Estudio de Tendencias de Compra en los EEUU")

st.image("banner.jpg", use_container_width=True)

st.markdown(
    "Este archivo permite explorar datos de compras en los Estados Unidos utilizando diversas visualizaciones.\n"
    "El conjunto de datos ofrece una visión completa de las tendencias de compra de los consumidores, con el fin de identificar patrones y comportamientos en las compras al por menor.\n"
    "Incluye información detallada sobre las transacciones en diferentes categorías de productos, datos demográficos de los clientes y los canales de compra utilizados.\n"
    "Se proporcionarán visualizaciones de datos que permitan obtener conclusiones acerca del funcionamiento del sector, orientando la visualización de la información en los siguientes aspectos:\n"
    "- Obtener información acerca del perfil del comprador.\n"
    "- Observar qué productos tienen un mejor rendimiento en ventas.\n"
    "- Comportamiento de compra por regiones."
)

# Configuración global de fondo blanco para gráficos interactivos
plotly_layout = dict(template='plotly_white')


st.header("1. Información acerca del comprador")
st.markdown("A continuación representan aquellos datos de utilidad para identificar el tipo de compradores y segmentos que hay en el sector.")

# Pregunta 1: ¿Cuál es la distribución de las edades de los clientes?
st.subheader("Distribución de las edades de los clientes")
fig1, ax1 = plt.subplots()
sns.histplot(data['Age'], kde=True, bins=15, color='#1E90FF', ax=ax1)  # Azul suave
ax1.set_title("Distribución de las Edades")
ax1.set_xlabel("Edad")
ax1.set_ylabel("Frecuencia")
st.pyplot(fig1)

# Pregunta 2: ¿Cómo son las ventas por género?
st.subheader("Ventas por Género")
st.markdown("Comparamos las ventas totales entre géneros.")

# Crear un desplegable para filtrar por ubicación
locations = data['Location'].unique()
selected_location = st.selectbox("Selecciona una Ubicación:", options=["Todas"] + list(locations), index=0, key="location_filter")

# Filtrar datos según la ubicación seleccionada
filtered_data = data.copy()
if selected_location != "Todas":
    filtered_data = filtered_data[filtered_data['Location'] == selected_location]

# Calcular las ventas totales por género después de aplicar el filtro
gender_sales = filtered_data.groupby('Gender')['Purchase Amount (USD)'].sum().sort_values()

fig2 = px.bar( gender_sales,  orientation='v', 
    title=f"Ventas por Género{' - ' + selected_location if selected_location != 'Todas' else ''}",
    labels={'value': 'Ventas Totales (USD)', 'index': 'Género'})
fig2.update_traces(marker_color='#1E90FF')  # Azul profundo
fig2.update_layout( plotly_layout,  showlegend=False,  xaxis_title="Género",  yaxis_title="Ventas Totales (USD)")
st.plotly_chart(fig2)

st.subheader("Segmentación en función de Edad y Género")
st.markdown("Los filtros se aplicarán a los 2 gráficos siguientes")

# Crear desplegable para filtrar por género
genders = data['Gender'].unique()
selected_gender = st.selectbox("Selecciona un Género:", options=["Todos"] + list(genders), index=0, key="gender_filter")

# Crear desplegable para filtrar por rango de edad
age_ranges = {
    "Menores de 20": (0, 20),
    "20-30": (20, 30),
    "30-40": (30, 40),
    "40-50": (40, 50),
    "50-60": (50, 60),
    "60-70": (60, 70),
    "Mayores de 70": (70, float('inf'))
}
selected_age_range = st.selectbox("Selecciona un Rango de Edad:", options=["Todos"] + list(age_ranges.keys()), index=0, key="age_filter")

# Filtrar datos según género seleccionado
filtered_data = data.copy()
if selected_gender != "Todos":
    filtered_data = filtered_data[filtered_data['Gender'] == selected_gender]

# Filtrar datos según rango de edad seleccionado
if selected_age_range != "Todos":
    min_age, max_age = age_ranges[selected_age_range]
    filtered_data = filtered_data[(filtered_data['Age'] >= min_age) & (filtered_data['Age'] < max_age)]

# Pregunta 3: ¿Cuánto gastan en promedio los clientes por categoría?
st.subheader("Gastos Promedio por Categoría")
st.markdown("Analizamos los gastos promedio de los clientes en las diferentes categorías.")

# Filtrar datos para el segundo gráfico según los mismos filtros de género y rango de edad
filtered_data_2 = data.copy()
if selected_gender != "Todos":
    filtered_data_2 = filtered_data_2[filtered_data_2['Gender'] == selected_gender]
if selected_age_range != "Todos":
    min_age, max_age = age_ranges[selected_age_range]
    filtered_data_2 = filtered_data_2[(filtered_data_2['Age'] >= min_age) & (filtered_data_2['Age'] < max_age)]

# Calcular el gasto promedio por categoría después de aplicar los filtros
avg_spending = filtered_data_2.groupby('Category')['Purchase Amount (USD)'].mean().sort_values()

# Crear el gráfico de barras horizontales
fig3 = px.bar( avg_spending,  orientation='h', title=f"Gasto Promedio por Categoría{' - ' + selected_gender if selected_gender != 'Todos' else ''}{' - ' + selected_age_range if selected_age_range != 'Todos' else ''}",
    labels={'value': 'Gasto Promedio (USD)', 'index': 'Categoría'})
fig3.update_traces(marker_color='#1E90FF')  # Azul más intenso
fig3.update_layout( plotly_layout,  showlegend=False,  xaxis_title="Gasto Promedio (USD)",  yaxis_title="Categoría")

# Mostrar el gráfico
st.plotly_chart(fig3)

# Pregunta 4: ¿Cuál es la proporción de métodos de pago preferidos?
st.subheader("Métodos de Pago Preferidos")
st.markdown("Conocemos la proporción de los métodos de pago más populares.")

# Calcular proporción de métodos de pago preferidos
payment_counts = filtered_data['Preferred Payment Method'].value_counts()

fig4 = px.pie(
    values=payment_counts.values,
    names=payment_counts.index,
    title=f"Métodos de Pago Preferidos{' - ' + selected_gender if selected_gender != 'Todos' else ''}{' - ' + selected_age_range if selected_age_range != 'Todos' else ''}",
    color_discrete_sequence=['#1E90FF', '#4169E1', '#4682B4', '#5F9EA0', '#00BFFF', '#FFFFFF']
)


fig4.update_layout(plotly_layout, title="Métodos de Pago Preferidos", legend_title="Métodos de Pago")
st.plotly_chart(fig4)


# Pregunta 5: ¿Cuál es la relación entre la edad y el monto gastado?
st.subheader("Relación entre Edad y Monto Gastado")
st.markdown("Visualizamos si existe una correlación entre la edad de los clientes y su gasto, desglosado por categoría.")

# Crear desplegable para filtrar por categoría
categories = data['Category'].unique()
selected_category = st.selectbox("Selecciona una Categoría:", options=["Todas"] + list(categories), index=0, key="category_filter")

# Filtrar datos según la categoría seleccionada
filtered_data_3 = data.copy()
if selected_category != "Todas":
    filtered_data_3 = filtered_data_3[filtered_data_3['Category'] == selected_category]

# Agrupar datos por edad y género para calcular el gasto promedio
age_gender_grouped = filtered_data_3.groupby(['Age', 'Gender'])['Purchase Amount (USD)'].mean().reset_index()

# Crear el gráfico de líneas
fig5 = px.line(age_gender_grouped, x='Age',  y='Purchase Amount (USD)',  color='Gender', 
    title=f"Relación entre Edad y Monto Gastado{' - ' + selected_category if selected_category != 'Todas' else ''}",
    labels={'Age': 'Edad', 'Purchase Amount (USD)': 'Monto Gastado (USD)'},
    color_discrete_map={'Male': '#1E90FF', 'Female': '#FF69B4'} )
fig5.update_layout(plotly_layout, xaxis_title="Edad", yaxis_title="Monto Gastado Promedio (USD)")
st.plotly_chart(fig5)


st.header("2. Rendimiento en ventas de los productos")
st.markdown("A continuación representan aquellos datos de utilidad para identificar aquellos productos que venden en mayor cantidad"
             "y en que segmentos.")

# Pregunta 6
st.subheader("Top 10 Productos Más Vendidos")
st.markdown("Exploramos cuáles son los productos más populares, pudiendo filtrar por categoría y Estado.")

# Crear desplegables para filtrar por categoría y Estado
categories = data['Category'].unique()
locations = data['Location'].unique()

# Usamos claves únicas para los selectbox
selected_category = st.selectbox("Selecciona una Categoría:", options=["Todas"] + list(categories), index=0, key="top10_category_filter")
selected_location = st.selectbox("Selecciona un Estado:", options=["Todas"] + list(locations), index=0, key="top10_location_filter")

# Filtrar datos según la categoría y Estado seleccionadas
filtered_data = data.copy()
if selected_category != "Todas":
    filtered_data = filtered_data[filtered_data['Category'] == selected_category]
if selected_location != "Todas":
    filtered_data = filtered_data[filtered_data['Location'] == selected_location]

# Agrupar y calcular los 10 productos más vendidos
top_products = (filtered_data.groupby('Item Purchased')['Purchase Amount (USD)'].sum().sort_values(ascending=False).head(10))

# Crear gráfico
fig6 = px.bar(
    top_products,
    orientation='v',
    title=f"Top 10 Productos Más Vendidos{' - ' + selected_category if selected_category != 'Todas' else ''}{' en ' + selected_location if selected_location != 'Todas' else ''}",
    labels={'value': 'Ventas Totales (USD)', 'index': 'Producto'}
)
fig6.update_traces(marker_color='#1E90FF')  # Azul uniforme
fig6.update_layout(plotly_layout, showlegend=False, yaxis_title="Ventas Totales (USD)", xaxis_title="Producto")
st.plotly_chart(fig6)


# Pregunta 7: ¿Qué tallas son las más compradas por categoría?
st.subheader("Tallas Comprados por Categoría")
st.markdown("Visualizamos los tallas más populares dentro de cada categoría.")

size_order = ['S', 'M', 'L', 'XL']
data['Size'] = pd.Categorical(data['Size'], categories=size_order, ordered=True)

fig7 = px.histogram(data, x='Category', color='Size', barmode='group',
                    category_orders={'Size': size_order},  # Asegurarse de que respeta el orden definido
                    title="Tallas Comprados por Categoría", labels={'Category': 'Categoría', 'count': 'Cantidad'},
                    color_discrete_map={'S': '#1E90FF',  'M': '#D3D3D3','L': '#87CEEB','XL': '#4682B4'})
fig7.update_layout(plotly_layout, yaxis_title="Cantidad de Compras", xaxis_title="Categoría")
st.plotly_chart(fig7)

# Pregunta 8: ¿Se compra más con descuento o sin descuento?
st.subheader("Impacto del Descuento en las Ventas")
st.markdown("Analizamos si los descuentos afectan a el Importe Gastado.")

# Crear un desplegable para filtrar por categoría
categories = data['Category'].unique()
selected_category = st.selectbox("Selecciona una Categoría:", options=["Todas"] + list(categories), index=0, key="discount_filter")

if selected_category != "Todas":
    filtered_data = data[data['Category'] == selected_category]
else:
    filtered_data = data

fig8 = px.box(
    filtered_data, 
    x='Discount Applied', 
    y='Purchase Amount (USD)', 
    color='Discount Applied', 
    title=f"Distribución del Monto Gastado con y sin Descuento {'- ' + selected_category if selected_category != 'Todas' else ''}",
    labels={'Discount Applied': 'Descuento Aplicado', 'Purchase Amount (USD)': 'Monto de Compra (USD)'},
    color_discrete_map={'Yes': '#1E90FF', 'No': '#87CEEB'}
)

fig8.update_layout(
    plotly_layout, 
    showlegend=True, 
    yaxis_title="Monto de Compra (USD)", 
    xaxis_title="Descuento Aplicado"
)

st.plotly_chart(fig8)

fig8_1 = px.histogram(filtered_data,  x='Discount Applied',  color='Discount Applied', 
    title=f"Número de Ventas con y sin Descuento {'- ' + selected_category if selected_category != 'Todas' else ''}", 
    labels={'Discount Applied': 'Descuento Aplicado', 'count': 'Cantidad'}, 
    color_discrete_map={'Yes': '#1E90FF', 'No': '#87CEEB'})

fig8_1.update_layout(plotly_layout, showlegend=False, yaxis_title="Cantidad de Ventas", xaxis_title="Descuento Aplicado") 
st.plotly_chart(fig8_1)


st.header("3. Comportamiento de las ventas por región")
st.markdown("A continuación representan aquellos datos de utilidad para discernir el comportamiento de las ventas en las distintas regiones.")

# Diccionario de abreviaturas de los estados, necessario para las representación de los mapas)
state_abbreviations = {"Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", 
    "California": "CA", "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE", "Florida": "FL", "Georgia": "GA", "Hawaii": "HI", "Idaho": "ID", 
    "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD", 
    "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS", "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV", 
    "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM", "New York": "NY", "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK", 
    "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC", "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT", 
    "Vermont": "VT", "Virginia": "VA", "Washington": "WA", "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY" }

st.subheader("Análisis de Ventas Totales por Estado")
st.markdown("Exploramos qué ubicaciones generan mayores ventas.")


# Crear un desplegable único para filtrar por categoría
categories = data['Category'].unique()
selected_category = st.selectbox("Selecciona una Categoría:", options=["Todas"] + list(categories), index=0, key="unified_category_filter")
data_filtered = data if selected_category == "Todas" else data[data['Category'] == selected_category]
location_total_sales = (data_filtered.groupby('Location')['Purchase Amount (USD)'].sum().sort_values(ascending=False).head(10))

# Pregunta 9: Ventas Totales por Estado

# Crear un mapa coroplético basado en el monto total de ventas por estado
state_sales = data.groupby('Location')['Purchase Amount (USD)'].sum().reset_index()
state_sales['Location'] = state_sales['Location'].apply(lambda x: state_abbreviations.get(x.title(), x))

fig9_map1 = px.choropleth(
    state_sales,
    locations='Location',
    locationmode="USA-states",
    color='Purchase Amount (USD)',
    hover_name='Location',
    title="Mapa de Ventas Totales por Estado",
    color_continuous_scale=px.colors.sequential.Blues,
    labels={'Purchase Amount (USD)': 'Ventas Totales (USD)'}
)

fig9_map1.update_layout(
    geo=dict(scope='usa'),
    coloraxis_colorbar=dict(title="Ventas Totales (USD)")
)

st.plotly_chart(fig9_map1)


fig9 = px.bar(location_total_sales, orientation='v', 
              title=f"Top 10 Estados con Más Ventas {' - ' + selected_category if selected_category != 'Todas' else ''}",
              labels={'value': 'Ventas Totales (USD)', 'index': 'Estado'})
fig9.update_traces(marker_color='#1E90FF')
fig9.update_layout(showlegend=False, yaxis_title="Ventas Totales (USD)", xaxis_title="Estados", xaxis_tickangle=-45)
st.plotly_chart(fig9)

# Transformar la columna 'Location' a abreviaturas de los estados para el mapa de ventas totales
location_total_sales_df = location_total_sales.reset_index()
location_total_sales_df['Location'] = location_total_sales_df['Location'].apply(lambda x: state_abbreviations.get(x.title(), x))

# Crear un mapa de choropleth para resaltar los estados con más ventas totales
fig9_map2 = px.choropleth(location_total_sales_df, locations='Location', locationmode="USA-states", hover_name='Location',
                         color_discrete_sequence=['#1E90FF'],  scope="usa",
                         title="Mapa de Top 10 Estados con Más Ventas")  
fig9_map2.update_traces(marker_line_color='black', marker_line_width=0.5, showscale=False)
fig9_map2.update_layout(geo=dict(scope='usa'))
st.plotly_chart(fig9_map2)

st.subheader("Análisis de Importe Medio por Estado")
st.markdown("Exploramos cuales son los estados con mayor importe medio por compra realizada.")

# Pregunta 10: Importe Medio por Estado

# Crear un mapa coroplético basado en el importe medio por compra por estado
location_avg_sales = data.groupby('Location')['Purchase Amount (USD)'].mean().reset_index()
location_avg_sales['Location'] = location_avg_sales['Location'].apply(lambda x: state_abbreviations.get(x.title(), x))

fig10_map1 = px.choropleth(
    location_avg_sales,
    locations='Location',
    locationmode="USA-states",
    color='Purchase Amount (USD)',
    hover_name='Location',
    title="Mapa de Importe Medio por Estado",
    color_continuous_scale=px.colors.sequential.Blues,
    labels={'Purchase Amount (USD)': 'Importe Medio (USD)'}
)

fig10_map1.update_layout(
    geo=dict(scope='usa'),
    coloraxis_colorbar=dict(title="Importe Medio (USD)")
)

st.plotly_chart(fig10_map1)

# Localizaciones con Mayor Importe Medio por Compra
location_avg_sales = (data_filtered.groupby('Location')['Purchase Amount (USD)'].mean().sort_values(ascending=False).head(10))

fig10 = px.bar(location_avg_sales, orientation='v',
              title=f"Top 10 Estados con Mayor Importe Medio por Compra {' - ' + selected_category if selected_category != 'Todas' else ''}",
              labels={'value': 'Importe Medio por Compra (USD)', 'index': 'Estado'})
fig10.update_traces(marker_color='#4682B4')
fig10.update_layout(showlegend=False, yaxis_title="Importe Medio por Compra (USD)", xaxis_title="Estados", xaxis_tickangle=-45)
st.plotly_chart(fig10)

# Transformar la columna 'Location' a abreviaturas de los estados para el mapa de ventas medias
location_avg_sales_df = location_avg_sales.reset_index()
location_avg_sales_df['Location'] = location_avg_sales_df['Location'].apply(lambda x: state_abbreviations.get(x.title(), x))

# Crear un mapa de choropleth para resaltar los estados con mayor importe medio por compra
fig10_map2 = px.choropleth(location_avg_sales_df, locations='Location', locationmode="USA-states", hover_name='Location',
                         color_discrete_sequence=['#4682B4'], scope="usa", title="Mapa de Top 10 Estados con Mayor Importe Medio por Compra") 

fig10_map2.update_traces(marker_line_color='black',marker_line_width=0.5,showscale=False )
fig10_map2.update_layout(geo=dict(scope='usa') )
st.plotly_chart(fig10_map2)
