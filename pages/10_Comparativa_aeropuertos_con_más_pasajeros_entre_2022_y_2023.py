import streamlit as st
from utils.database import obtener_datos
import pandas as pd
import plotly.express as px # type: ignore

# Configurar la página
st.set_page_config(
    page_title="Comparativa del ranking de aeropuertos con mayor cantidad de pasajeron entre 2022 y 2023",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título principal
st.title("✈️ Análisis Exploratorio de Tráfico Aéreo Global 2022-2023")
st.markdown("---")

@st.cache_data
def load_and_process_data():
    """Carga los datos de la tabla 'total', renombra las columnas y prepara los datos."""
    
    df = obtener_datos('total')

    if df.empty:
        st.warning("No se pudieron cargar los datos de la tabla 'total'. Asegúrate de que Supabase está configurado correctamente.")
        return pd.DataFrame(), pd.DataFrame()

    # Nombres de las columnas según tu base de datos
    COL_PASAJEROS_2023 = '2023_enplaned_passengers_total'
    COL_PASAJEROS_2022 = '2022_enplaned_passengers_total'
    COL_CRECIMIENTO = 'percentage_change_2022_2023_total'
    
    # 1. Asegurar que las columnas sean numéricas
    df[COL_PASAJEROS_2023] = pd.to_numeric(df[COL_PASAJEROS_2023], errors='coerce')
    df[COL_PASAJEROS_2022] = pd.to_numeric(df[COL_PASAJEROS_2022], errors='coerce')
    df[COL_CRECIMIENTO] = pd.to_numeric(df[COL_CRECIMIENTO], errors='coerce')

    # 2. Renombrar columnas
    df = df.rename(columns={
        '2023_rank_total': 'Ranking 2023',
        '2022_rank_total': 'Ranking 2022',
        COL_PASAJEROS_2023: 'Pasajeros 2023',
        COL_PASAJEROS_2022: 'Pasajeros 2022',
        COL_CRECIMIENTO: 'Crecimiento (%)',
        'airport': 'Aeropuerto',
    })
    
    # 3. Eliminar filas con valores nulos para los cálculos clave
    df.dropna(subset=['Pasajeros 2023', 'Pasajeros 2022', 'Crecimiento (%)', 'Ranking 2023', 'Ranking 2022'], inplace=True)

    # 4. Cálculos Adicionales
    df['Diferencia Pasajeros'] = df['Pasajeros 2023'] - df['Pasajeros 2022']
    df['Cambio Ranking'] = df['Ranking 2022'] - df['Ranking 2023'] 
    
    # Seleccionar y reordenar columnas finales (mostrando solo el Top 20)
    cols_finales = ['Aeropuerto', 'Ranking 2023', 'Pasajeros 2023', 'Pasajeros 2022', 
                    'Cambio Ranking', 'Diferencia Pasajeros', 'Crecimiento (%)']
    
    # df_top_20 es el DataFrame filtrado para el Top 20.
    df_top_20 = df[df['Ranking 2023'] <= 20].sort_values(by='Ranking 2023')[cols_finales]

    # df_completo es el DataFrame completo, aunque ya no lo usaremos para estadísticas.
    return df_top_20, df 

df_top_20, df_completo = load_and_process_data() 

# --- 2. Funciones para Estadísticas Descriptivas ---

def calcular_estadisticas_avanzadas(series):
    """Calcula la asimetría, curtosis y coeficiente de variación."""
    mean = series.mean()
    std = series.std()
    
    stats = {
        'Asimetría': series.skew(),
        'Curtosis': series.kurtosis(),
        'Coeficiente de Variación': (std / mean) * 100 if mean != 0 else 0
    }
    return pd.Series(stats)

def generar_tabla_estadisticas(df):
    """Genera una tabla de estadísticas descriptivas unificada con formato."""
    
    cols_calc = ['Pasajeros 2023', 'Pasajeros 2022', 'Diferencia Pasajeros', 'Crecimiento (%)']

    stats_std = df[cols_calc].describe().T.drop(columns=['count'])
    stats_adv = df[cols_calc].apply(calcular_estadisticas_avanzadas).T
    stats_df = pd.concat([stats_std, stats_adv], axis=1)

    idx_rename = {
        'Pasajeros 2023': 'Pasajeros Totales (2023)',
        'Pasajeros 2022': 'Pasajeros Totales (2022)',
        'Diferencia Pasajeros': 'Diferencia Pasajeros (2022-2023)',
        'Crecimiento (%)': 'Crecimiento Porcentual (%)'
    }
    stats_df.rename(index=idx_rename, inplace=True)
    
    stats_df.columns = ['Media', 'Desviación Estándar', 'Mínimo', 'Cuartil 25%', 'Mediana (Cuartil 50%)', 'Cuartil 75%', 'Máximo', 
                        'Asimetría', 'Curtosis', 'Coeficiente de Variación']
    
    for col in ['Media', 'Desviación Estándar', 'Mínimo', 'Cuartil 25%', 'Mediana (Cuartil 50%)', 'Cuartil 75%', 'Máximo']:
        mask_miles = stats_df.index.str.contains('Pasajeros') | stats_df.index.str.contains('Diferencia')
        stats_df.loc[mask_miles, col] = stats_df.loc[mask_miles, col].map('{:,.0f}'.format)
        
        mask_percent = stats_df.index.str.contains('Crecimiento')
        stats_df.loc[mask_percent, col] = stats_df.loc[mask_percent, col].map('{:.2f}%'.format)
    
    stats_df['Asimetría'] = stats_df['Asimetría'].map('{:.3f}'.format)
    stats_df['Curtosis'] = stats_df['Curtosis'].map('{:.3f}'.format)
    stats_df['Coeficiente de Variación'] = stats_df['Coeficiente de Variación'].map('{:.2f}%'.format)
    
    return stats_df


# --- 3. Streamlit ---

if not df_top_20.empty:
    
    # 3.1. Métricas Clave 
    col1, col_vacio, col2 = st.columns([1, 0.5, 1])
    
    # Métrica 1: Mayor Crecimiento Porcentual
    mayor_crecimiento = df_top_20.loc[df_top_20['Crecimiento (%)'].idxmax()]
    col1.metric(
        label="Aeropuerto con Mayor Crecimiento (%)", 
        value=f"{mayor_crecimiento['Aeropuerto']}", 
        delta=f"+{mayor_crecimiento['Crecimiento (%)']:.2f}%"
    )

    # Métrica 2: Mayor Caída de Ranking
    mayor_caida = df_top_20.loc[df_top_20['Cambio Ranking'].idxmin()]
    col2.metric(
        label="Aeropuerto con Mayor Caída de Ranking",
        value=f"{mayor_caida['Aeropuerto']}",
        # El cambio de ranking será negativo, se muestra así directamente.
        delta=f"{int(mayor_caida['Cambio Ranking'])} puestos" 
    )
    st.write("""Es muy importante resaltar en presente ranking aquellas métricas extremas que se han presentado en los aeropuertos como en el caso del San Francisco, CA: San Francisco International
    con el mayor cambio porcentual de pasajeros del año 2022 al 2023 y otra métrica extrema resaltante son las de los aeropuertos Miami, FL: Miami International y Phoenix, AZ: Phoenix Sky Harbor International que bajaron dos (2) puestos en el ranking de aeropuertos con más pasajeros.""")
    
    st.markdown("---")

    # 3.2. Estadísticas Descriptivas Avanzadas (SOLO TOP 20)
    st.header("📊 Estadísticas Descriptivas Avanzadas (Top 20) 2022 vs 2023")
    st.markdown("Análisis de distribución para Pasajeros Totales (2022 y 2023), Diferencia Absoluta y Crecimiento Porcentual, **restringido al Top 20 de aeropuertos por pasajeros de 2023**.")

    stats_df_top_20 = generar_tabla_estadisticas(df_top_20)
    st.dataframe(stats_df_top_20, use_container_width=True)
    st.write("""Para el ranking de los 20 aeropuertos con mayor cantidad de pasajeros, la media de pasajeros subió de 24,260,899 pasajeros por aeropuerto a 27,087,306 pasajeros por aeropuerto con una diferencia media de 2,826,408 con un crecimiento porcentual promedio de 11,74%,todas las estadísticas descriptivas del año 2023 en comparación al año 2022 presentaron un aumento, en cuanto a la distribución de los datos para ambos años se ven inclinados hacia los valores mas pequeños con picos pronunciados cercanos a la media, en cuantos a la dispersión los coeficientes de variación para ambos años indican que los datos son heterogéneos y la media no es representativa.
""")
    st.write("""En cuanto al cambio porcentual de los pasajeros hay los datos se vena cumulados hacia los valores más altos con alta concentración de datos entorno a la media, con una baja variación lo cual hace la media representaba de los datos y bastantes homogéneos.
""")

    
    
    st.markdown("---")
    
    # 3.3. Histogramas de Frecuencia (SOLO TOP 20)
    st.header("📈 Distribución de Frecuencia de Pasajeros y Crecimiento (Top 20)")
    st.markdown("Los histogramas muestran cómo se agrupan y se distribuyen la cantidad de pasajeros en los años 2022 y 2023 y del cambio porcentual de los pasajeros **pertenecientes al Top 20 de aeropuertos con mayor cantidad de pasajeros**.")


    # Histograma 2: Pasajeros 2022
    fig_hist_2022 = px.histogram(
        df_top_20, 
        x='Pasajeros 2022', 
        nbins=10, 
        title='Frecuencia de Pasajeros Totales (2022) - Top 20',
        labels={'Pasajeros 2022': 'Pasajeros Totales (2022)'}
    )
    fig_hist_2022.update_layout(bargap=0.1)
    st.plotly_chart(fig_hist_2022, use_container_width=True)
    st.write("""Respaldando lo mostrado en las estadísticas descriptivas es fácilmente visible la distribución de los datos además de observar que 7 de los 20 aeropuertos en el ranking tienen de entre 20 y 25 millones de pasajeros en el año 2022 y con un solo aeropuerto entre los 45 y 50 millones de aeropuertos como un valor muy alejado y atípico.
""")

# Histograma 1: Pasajeros 2023
    fig_hist_2023 = px.histogram(
        df_top_20, 
        x='Pasajeros 2023', 
        nbins=10, 
        title='Frecuencia de Pasajeros Totales (2023)  - Top 20',
        labels={'Pasajeros 2023': 'Pasajeros Totales (2023)'}
    )
    fig_hist_2023.update_layout(bargap=0.1)
    st.plotly_chart(fig_hist_2023, use_container_width=True)
    st.write("""En el presente histograma de frecuencia se respalda los valores de las estadísticas descriptivas en donde se puede apreciar fácilmente la distribución de los datos en donde hay mayor frecuencia de aeropuertos  con cantidades de personas entre 20 y 25 millones de pasajeros y solo un aeropuerto cuenta con una cantidad de pasajeros de entre 50 y 55 millones.
""")

    # Histograma 3: Crecimiento Porcentual
    fig_hist_crecimiento = px.histogram(
        df_top_20, 
        x='Crecimiento (%)', 
        nbins=50, 
        title='Frecuencia del Cambio Porcentual de Pasajeros (2022-2023) - Top 20',
        labels={'Crecimiento (%)': 'Crecimiento Porcentual (%)'},
        color_discrete_sequence=['#00CC96']
    )
    fig_hist_crecimiento.update_layout(bargap=0.1)
    st.plotly_chart(fig_hist_crecimiento, use_container_width=True)
    st.write("""Nuevamente se es fácilmente evidenciable lo visto en las estadísticas descriptivas y se puede apreciar visualmente que dentro el cambio porcentual de la cantidad de pasajeros hay una alta concentración de frecuencias entorno a la media de 11,74% además se pueden ver dos valores atípicos ambos en extremos opuestos de la distribución siendo los aeropuertos que más y menos crecieron respecto al año 2022.
""")

    st.markdown("---")

    # 3.4. Tabla de Datos Detallada (Top 20)
    st.markdown("### Tabla de Comparación Detallada (Top 20)")
    
    df_mostrar = df_top_20.copy()
    df_mostrar['Pasajeros 2023'] = df_mostrar['Pasajeros 2023'].map('{:,.0f}'.format)
    df_mostrar['Pasajeros 2022'] = df_mostrar['Pasajeros 2022'].map('{:,.0f}'.format)
    df_mostrar['Diferencia Pasajeros'] = df_mostrar['Diferencia Pasajeros'].map('{:,.0f}'.format)
    df_mostrar['Crecimiento (%)'] = df_mostrar['Crecimiento (%)'].map('{:.2f}%'.format)

    st.dataframe(df_mostrar, use_container_width=True)
    st.write("""En la siguiente tabla detallada del ranking de los 20 aeropuertos con más pasajeros se observa los detalles de cada aeropuerto incluido el cambio que tuvo en el ranking en comparación al año anterior en donde se presenciaron cambios tan notorios solo dos aeropuertos bajaron dos puestos en el ranking, y agregando que los primeros tres y los últimos 6 aeropuertos mantuvieron sus puestos en el ranking en el año 2023 respecto al año 2022.
""")
    
    st.markdown("---")
    
    # 3.5. Visualización: Gráfico de Dispersión
    st.markdown("### Visualización: Crecimiento Porcentual vs. Pasajeros Totales (2023)")
    
    fig_scatter = px.scatter(
        df_top_20,
        x='Pasajeros 2023',
        y='Crecimiento (%)',
        size='Pasajeros 2023',
        color='Aeropuerto',
        hover_name='Aeropuerto',
        title='Pasajeros y Crecimiento de los Top 20 Aeropuertos',
        labels={'Pasajeros 2023': 'Pasajeros Totales 2023', 'Crecimiento (%)': 'Crecimiento Porcentual (%)'},
    )
    
    st.plotly_chart(fig_scatter, use_container_width=True)
    st.write("""Y como último se tiene un grafico que resume todo lo investigado respecto al ranking de aeropuertos con mayor cantidad de pasajeros en el eje x se ve la cantidad de pasajeros en el año 2023 en el eje y el cambio porcentual respecto al año 2022, y el tamaño de el circulo indica también la cantidad de pasajeros en el año 2022.
A la derecha del grafico se tiene la leyenda con el ranking de aeropuertos ordenados respectivamente con el color que lo representa en el grafico.
""")

else:
    st.error("No se encontraron datos para generar la comparativa o la carga de datos falló.")
