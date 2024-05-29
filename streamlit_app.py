import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Cargar datos
@st.cache
def load_data():
    data = pd.read_csv('IMDB-Movie-Data.csv')
    # Crear una nueva columna con el primer género listado
    data['Primary Genre'] = data['Genre'].apply(lambda x: x.split(',')[0])
    return data

data = load_data()

# Sidebar para filtros
st.sidebar.header('Filtros')
year_min, year_max = int(data['Year'].min()), int(data['Year'].max())
year_start, year_end = st.sidebar.slider('Selecciona el rango de años', year_min, year_max, (year_min, year_max))

# Filtrar datos
filtered_data = data[(data['Year'] >= year_start) & (data['Year'] <= year_end)]

# Gráfico de sectores para géneros primarios
st.header('Número de películas por género primario')
primary_genre_counts = filtered_data['Primary Genre'].value_counts()
fig1, ax1 = plt.subplots()
ax1.pie(primary_genre_counts, labels=primary_genre_counts.index, autopct='%1.1f%%', startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
st.pyplot(fig1)

# Gráfico de barras para ingresos por año
st.header('Ingresos por año')
revenue_per_year = filtered_data.groupby('Year')['Revenue (Millions)'].sum()
fig2, ax2 = plt.subplots()
ax2.bar(revenue_per_year.index, revenue_per_year.values)
ax2.set_xlabel('Año')
ax2.set_ylabel('Ingresos (Millones de dólares)')
ax2.set_title('Ingresos por año')
st.pyplot(fig2)

# Mostrar las 5 películas con mayor facturación
st.header('Top 5 películas con mayor facturación')
top_movies = filtered_data.nlargest(5, 'Revenue (Millions)')
st.write(top_movies[['Title', 'Year', 'Revenue (Millions)']])

