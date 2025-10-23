import streamlit as st
from utils.database import obtener_datos
import plotly.express as px
import pandas as pd

# Configurar la página
st.set_page_config(
    page_title="Aeropuertos con mayor y menor porcentaje de crecimiento entre los años 2022 - 2023",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título principal
st.title("✈️ Análisis exploratorio de tráfico aéreo en EE.UU 2022-2023")
st.markdown("---")

# Tab 1: Datos Completos
st.subheader("Porcentaje de crecimiento de pasajeros entre los años 2022 - 2023")
st.markdown("---")

# 1. Define la tabla que quieres (por ejemplo, 'total', 'domestic', 'airports')
Tabla_Total = 'total' 
Tabla_Domestic = 'domestic'
Tabla_airports = 'airports'
Tabla_international = 'international'

# 2. Llama a la función para obtener la tabla completa como un DataFrame
# La función está decorada con @st.cache_data, por lo que solo se ejecuta una vez.
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

# Definición de las nuevas columnas de cambio porcentual
TIPOS_DE_FLUJO = ['total', 'domestic', 'international']

for flujo in TIPOS_DE_FLUJO:
    col_2022 = f'2022_{flujo}'
    col_2023 = f'2023_{flujo}'
    
    # Nombre de la nueva columna de cambio porcentual
    col_cambio = f'cambio_{flujo}_pct'
    
    # Calcular el cambio porcentual
    # Nota: Usamos .div(..., fill_value=0) para manejar posibles divisiones por cero 
    # (si 2022 es 0 o NaN)
    df_final[col_cambio] = (
        (df_final[col_2023] - df_final[col_2022]) / df_final[col_2022].replace(0, pd.NA)
    ) * 100

# Llenar cualquier valor NaN resultante con 0 (si no hay datos o la división era por cero)
df_final = df_final.fillna(0)

def crear_grafico_cambio(df, flujo, orden, n_aeropuertos):
    """
    Genera un gráfico de barras de cambio porcentual dinámico.
    """
    # 1. CONSTRUIR NOMBRE DE LA COLUMNA DE CAMBIO
    nombre_columna_cambio = f'cambio_{flujo}_pct' 
    titulo_flujo = flujo.capitalize()
    
    if nombre_columna_cambio not in df.columns:
        st.error(f"Error: La columna '{nombre_columna_cambio}' no se encontró.")
        return None
    
    # --- NUEVO PASO CLAVE: FILTRAR LOS DATOS DE CAMBIO 0% ---
    
    # 1. Crear una copia del DataFrame para trabajar sobre él
    df_filtrado = df.copy()
    
    # 2. Aplicar el filtro: solo incluir filas donde el cambio NO es 0
    # Esto elimina los aeropuertos que pasaron de 0 a 0 o que realmente no tienen datos.
    # Usamos np.isclose() para manejar errores de punto flotante, aunque pd.Series.abs() > 0.0 también funciona.
    df_filtrado = df_filtrado[df_filtrado[nombre_columna_cambio].abs() > 0.001].copy()

    # Si después de filtrar no quedan datos
    if df_filtrado.empty:
        st.warning(f"No hay aeropuertos con cambio porcentual distinto de 0% para el flujo {titulo_flujo}.")
        return None

    # 2. ORDENAR Y SELECCIONAR DATOS
    
    if orden == 'Mayor Crecimiento (Top N)':
        # Orden descendente (los cambios positivos más altos)
        df_ordenado = df_filtrado.sort_values(by=nombre_columna_cambio, ascending=False)
    else: # Menor Crecimiento (Bottom N)
        # Orden ascendente (los cambios negativos más bajos)
        df_ordenado = df_filtrado.sort_values(by=nombre_columna_cambio, ascending=True)

    # Seleccionar los Top/Bottom N
    df_top_n = df_ordenado.head(n_aeropuertos).copy()
    
    # 3. GENERAR EL GRÁFICO CON PLOTLY
    
    fig = px.bar(
        df_top_n, 
        x=nombre_columna_cambio, 
        y='airport', 
        orientation='h', 
        title=f'{orden} de {n_aeropuertos} Aeropuertos: Cambio % de Pasajeros {titulo_flujo} (2022 vs 2023)',
        labels={nombre_columna_cambio: 'Cambio Porcentual (%)', 'airport': 'Aeropuerto'},
        # Usamos una escala de color divergente para mostrar crecimiento (positivo) vs. caída (negativo)
        color=nombre_columna_cambio,
        color_continuous_scale='RdYlGn' 
    )
    
    # Mejorar la visualización: Mover la barra de color a una posición más neutral (cerca del 0%)
    fig.update_layout(
        yaxis={'categoryorder':'total ascending'}
    )
    fig.update_coloraxes(colorbar_title='Cambio %', cmid=0) # Centra el color en 0
    
    return fig

# --- Lógica de la página ---

# --- Selectores ---
st.sidebar.header("Opciones de Cambio %")

# Selector de Flujo (Nacional, Internacional, Total)
flujo_seleccionado = st.sidebar.selectbox(
    "Selecciona el Flujo de Pasajeros:",
    options=['total', 'domestic', 'international'],
    format_func=lambda x: x.capitalize() 
)

# Selector de Top/Bottom
orden_seleccionado = st.sidebar.radio(
    "Mostrar:",
    options=['Mayor Crecimiento (Top N)', 'Menor Crecimiento (Bottom N)']
)

# Selector de Cantidad de Aeropuertos
n_seleccionado = st.sidebar.slider(
    "Número de Aeropuertos a Mostrar (N):",
    min_value=5,
    max_value=20,
    value=10
)

# --- Generar Gráfico ---
if 'df_final' in locals():
    figura = crear_grafico_cambio(
        df=df_final, 
        flujo=flujo_seleccionado, 
        orden=orden_seleccionado,
        n_aeropuertos=n_seleccionado
    )

    if figura:
        st.plotly_chart(figura, use_container_width=True)
    
if flujo_seleccionado == 'total':
                
        st.markdown(f"""
                    **Total** 
                    """)
        
elif flujo_seleccionado == 'international':
                
        st.markdown(f"""
                    **Internacional**
                    """)
    
elif flujo_seleccionado == 'domestic':
                
        st.markdown(f"""
                    **Doméstica**
                    """)
            

    # Opcional: Mostrar los datos para debug
    # st.subheader("Datos de Cambio Porcentual")
    # st.dataframe(df_final[['airport', '2022_' + flujo_seleccionado, '2023_' + flujo_seleccionado, 'cambio_' + flujo_seleccionado + '_pct']].head(20))
else:
    st.warning("El DataFrame 'df_final' no está cargado. Asegúrate de que la conexión a Supabase se ejecuta primero.")


