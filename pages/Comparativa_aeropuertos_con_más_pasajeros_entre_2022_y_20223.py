import streamlit as st
from utils.database import obtener_datos
import pandas as pd
import plotly.express as px
import numpy as np

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
    
    df_top_20 = df[df['Ranking 2023'] <= 20].sort_values(by='Ranking 2023')[cols_finales]

    return df_top_20, df 

df_top_20, df_completo = load_and_process_data()

# --- 2. Funciones para Estadísticas Descriptivas  ---

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
    # Usaremos solo 2 columnas para estas 2 métricas.
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
    con el mayor cambio porcentual de pasajeros del año 2022 al 2023 y otra métrica extrema resaltante son las de los aeropuertos Miami, FL: Miami International y Phoenix, AZ: Phoenix Sky Harbor International que bajaron dos (2) puestos en el ranking de aeropuertos con más pasajeros """)
    st.markdown("---")

    # 3.2. Estadísticas Descriptivas Avanzadas (TABLA ÚNICA Y COMPLETA)
    st.header("📊 Estadísticas Descriptivas Avanzadas 2022 vs 2023")
    st.markdown("Análisis de distribución para Pasajeros Totales (2022 y 2023), Diferencia Absoluta y Crecimiento Porcentual para **todos** los aeropuertos.")

    stats_df_completa = generar_tabla_estadisticas(df_completo)
    st.dataframe(stats_df_completa, use_container_width=True)
    st.write(""" .
""")
    st.markdown("---")
    
    # 3.3. Histogramas de Frecuencia
    st.header("📈 Distribución de Frecuencia de Pasajeros y Crecimiento")
    st.write(""" .
""")
    st.markdown("Los histogramas muestran cómo se agrupan los datos en diferentes rangos para **todos** los aeropuertos.")
    
    # Histograma 1: Pasajeros 2023
    fig_hist_2023 = px.histogram(
        df_completo, 
        x='Pasajeros 2023', 
        nbins=50, 
        title='Frecuencia de Pasajeros Totales (2023)',
        labels={'Pasajeros 2023': 'Pasajeros Totales (2023)'}
    )
    fig_hist_2023.update_layout(bargap=0.1)
    st.plotly_chart(fig_hist_2023, use_container_width=True)
    st.write(""" .
""")

    # Histograma 2: Pasajeros 2022
    fig_hist_2022 = px.histogram(
        df_completo, 
        x='Pasajeros 2022', 
        nbins=50, 
        title='Frecuencia de Pasajeros Totales (2022)',
        labels={'Pasajeros 2022': 'Pasajeros Totales (2022)'}
    )
    fig_hist_2022.update_layout(bargap=0.1)
    st.plotly_chart(fig_hist_2022, use_container_width=True)
    st.write(""" .
""")

    # Histograma 3: Crecimiento Porcentual
    fig_hist_crecimiento = px.histogram(
        df_completo, 
        x='Crecimiento (%)', 
        nbins=50, 
        title='Frecuencia del Cambio Porcentual de Pasajeros (2022-2023)',
        labels={'Crecimiento (%)': 'Crecimiento Porcentual (%)'},
        color_discrete_sequence=['#00CC96']
    )
    fig_hist_crecimiento.update_layout(bargap=0.1)
    st.plotly_chart(fig_hist_crecimiento, use_container_width=True)

    st.write(""" .
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
    st.write(""" .
""")
    st.markdown("---")
    

else:
    st.error("No se encontraron datos para generar la comparativa o la carga de datos falló.")