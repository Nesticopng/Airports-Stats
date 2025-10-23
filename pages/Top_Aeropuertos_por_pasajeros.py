import streamlit as st
from utils.database import obtener_datos
import pandas as pd
import plotly.express as px

# Configurar la página
st.set_page_config(
    page_title="Top Aeropuertos por pasajeros",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título principal
st.title("✈️ Análisis exploratorio de tráfico aéreo en EE.UU 2022-2023")
st.markdown("---")

# Tab 1: Datos Completos
st.subheader("Aeropuertos con mayor y menor cantidad de pasajeros")
st.markdown("---")

#Crear tabla final 

# 1. Extrael tablas de la base de datos
Tabla_Total = 'total' 
Tabla_Domestic = 'domestic'
Tabla_airports = 'airports'
Tabla_international = 'international'

# 2. Llama a la función para obtener la tabla completa como un DataFrame

df_total = obtener_datos(Tabla_Total)
df_domestic = obtener_datos(Tabla_Domestic)
df_airports = obtener_datos(Tabla_airports)
df_international = obtener_datos(Tabla_international)

# Convertir la columna 'airport' a string (texto) en df_total
df_total['airport'] = df_total['airport'].astype(str)

# Convertir la columna 'airport' a string (texto) en df_domestic
df_domestic['airport'] = df_domestic['airport'].astype(str)

# Convertir la columna 'airport' a string (texto) en df_international
df_international['airport'] = df_international['airport'].astype(str)

df_airports['iata_code'] = df_airports['iata_code'].astype(str)

# --- Paso 2: Ejecutar el Join/Merge de forma segura ---

KEY_COL = 'airport' 

# 1. Seleccionar las últimas 2 columnas de df_domestic y df_international
df2_extra = df_domestic.iloc[:, -2:]
df3_extra = df_international.iloc[:, -2:]
df4_extra = df_airports[['iata_code']]

# 2. Establecer la columna clave como índice en los DataFrames que se van a unir
# Esto es necesario para usar .join()
df2_extra = df2_extra.set_index(df_domestic[KEY_COL])
df3_extra = df3_extra.set_index(df_international[KEY_COL])
df4_extra = df4_extra.set_index(df_airports[KEY_COL])


# 3. Unir (Join) usando la columna clave ya unificada
df_final = df_total.join(
    df2_extra, 
    on=KEY_COL, 
    how='left'
).join(
    df3_extra, 
    on=KEY_COL, 
    how='left'
).join(
    df4_extra,
    on=KEY_COL,
    how='left'
)

df_final.rename(columns={'2023_enplaned_passengers_total': '2023_total','2022_enplaned_passengers_total': '2022_total','2023_enplaned_passengers_dom': '2023_domestic','2022_enplaned_passengers_dom': '2022_domestic','2023_enplaned_passengers_inter': '2023_international','2022_enplaned_passengers_inter': '2022_international'}, inplace=True)

def crear_grafico_dinamico(df, anio, flujo, orden, n_aeropuertos):
    """
    Genera un gráfico de barras dinámico basado en las selecciones del usuario.
    """
    # 1. CONSTRUIR NOMBRE DE LA COLUMNA
    # Convierte 'total' a 'total_passengers', etc., si es necesario, basado en el nombre de tu columna.
    # Si tus columnas son exactamente '2023_total', '2022_domestic', puedes usar la sintaxis directa:
    nombre_columna_datos = f'{anio}_{flujo}' 
    
    # Verificar si la columna existe
    if nombre_columna_datos not in df.columns:
        st.error(f"Error: La columna '{nombre_columna_datos}' no se encontró en el DataFrame.")
        return None

    # 2. ORDENAR Y SELECCIONAR DATOS
    # Ordenar los datos
    if orden == 'Mayor Flujo (Top N)':
        # Orden descendente para el TOP N
        df_ordenado = df.sort_values(by=nombre_columna_datos, ascending=False)
    else: # Menor Flujo (Bottom N)
        # Orden ascendente para el BOTTOM N
        df_ordenado = df.sort_values(by=nombre_columna_datos, ascending=True)

    # Seleccionar los Top/Bottom N
    df_top_n = df_ordenado.head(n_aeropuertos).copy()
    
    # 3. GENERAR EL GRÁFICO CON PLOTLY
    
    # Asegurar que el aeropuerto sea la categoría (eje Y) y los datos la barra (eje X)
    fig = px.bar(
        df_top_n, 
        x=nombre_columna_datos, 
        y='airport', 
        orientation='h', # Barras horizontales
        title=f'{orden} de {n_aeropuertos} Aeropuertos por Pasajeros ({flujo.capitalize()}, {anio})',
        labels={nombre_columna_datos: f'Pasajeros {flujo.capitalize()}', 'airport': 'Aeropuerto'},
        color=nombre_columna_datos, # Colorear por el valor
        color_continuous_scale=px.colors.sequential.Plasma
    )
    
    # Mejorar la visualización: Ordenar las barras para que la más grande quede arriba
    fig.update_layout(
        yaxis={'categoryorder':'total ascending'}
    )
    
    return fig

# Continúa en tu archivo Streamlit principal (ej: app.py)

if 'df_final' in locals(): # Verifica que el DataFrame esté cargado
    
    # --- 1. Definir los Selectores en el Sidebar ---
    st.sidebar.header("Opciones de Visualización")
    
    # Selector de Año
    anio_seleccionado = st.sidebar.selectbox(
        "Selecciona el Año:",
        options=['2023', '2022']
    )
    
    # Selector de Flujo (Nacional, Internacional, Total)
    flujo_seleccionado = st.sidebar.selectbox(
        "Selecciona el Flujo de Pasajeros:",
        options=['total', 'domestic', 'international'],
        format_func=lambda x: x.capitalize() # Muestra Total/Domestic/International
    )
    
    # Selector de Top/Bottom
    orden_seleccionado = st.sidebar.radio(
        "Mostrar:",
        options=['Mayor Flujo (Top N)', 'Menor Flujo (Bottom N)']
    )
    
    # Selector de Cantidad de Aeropuertos
    n_seleccionado = st.sidebar.slider(
        "Número de Aeropuertos a Mostrar (N):",
        min_value=5,
        max_value=20,
        value=10
    )

    # --- 2. Generar y Mostrar el Gráfico ---
    
    # Llamar a la función con los valores seleccionados
    figura = crear_grafico_dinamico(
        df=df_final, 
        anio=anio_seleccionado, 
        flujo=flujo_seleccionado, 
        orden=orden_seleccionado,
        n_aeropuertos=n_seleccionado
    )

    # Mostrar el gráfico si se generó correctamente
    if figura:
        st.plotly_chart(figura, use_container_width=True)
else:
    st.warning("El DataFrame 'df_final' no está disponible. Asegúrate de cargarlo correctamente.")

# --- BLOQUE PRINCIPAL 1: Condición de AÑO ---
if anio_seleccionado == '2023':
            
            # --- BLOQUE ANIDADO 1.1: Condición de FLUJO ---
    if flujo_seleccionado == 'total':
                
        st.markdown(f"""
                    **Análisis total 2023**
                    """)
            
    elif flujo_seleccionado == 'international':
                
        st.markdown(f"""
                    **Análisis internacional 2023**
                    """)
    
    elif flujo_seleccionado == 'domestic':
                
        st.markdown(f"""
                    **Análisis doméstico 2023**
                    """)
            
elif anio_seleccionado == '2022':
            
            # --- BLOQUE PRINCIPAL 2: Condición de AÑO 2022 ---
    if flujo_seleccionado == 'total':
        
        st.markdown(f"""
                    **Análisis total 2022**
                    """)
    
    if flujo_seleccionado == 'internacional':
        
        st.markdown(f"""
                    **Análisis internacional 2022**
                    """)
        
    if flujo_seleccionado == 'domestic':
        
        st.markdown(f"""
                    **Análisis doméstico 2023**
                    """)