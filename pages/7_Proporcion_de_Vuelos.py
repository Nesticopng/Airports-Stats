import streamlit as st
import pandas as pd
import numpy as np
from utils.database import obtener_datos
import plotly.express as px # type: ignore
import plotly.graph_objects as go # type: ignore

# Configurar la página
st.set_page_config(
    page_title="Proporción de Vuelos por Aeropuerto",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título principal
st.title("✈️ Análisis de Proporción de Vuelos por Aeropuerto")
st.markdown("---")
st.markdown("Análisis detallado de la distribución de vuelos domésticos e internacionales por aeropuerto")

# Obtener datos
with st.spinner("Cargando datos..."):
    df_domestic = obtener_datos('domestic')
    df_international = obtener_datos('international')
    df_airports = obtener_datos('airports')

# Verificar que los datos se cargaron correctamente
if df_domestic.empty or df_international.empty or df_airports.empty:
    st.error("❌ No se pudieron cargar los datos. Verifica la conexión a la base de datos.")
    st.stop()

# Convertir columnas a string para evitar errores
df_domestic['airport'] = df_domestic['airport'].astype(str)
df_international['airport'] = df_international['airport'].astype(str)
df_airports['airport'] = df_airports['airport'].astype(str)

# Sidebar para configuración
st.sidebar.header("🔧 Configuración del Análisis")

# Selector de año
año_seleccionado = st.sidebar.selectbox(
    "Selecciona el año:",
    options=['2023', '2022'],
    help="Selecciona el año para el análisis de proporciones"
)

# Función para calcular proporciones por aeropuerto
def calcular_proporciones_por_aeropuerto(df_domestic, df_international, año):
    """
    Calcula las proporciones de vuelos domésticos e internacionales por aeropuerto
    """
    # Determinar columnas según el año
    if año == '2023':
        col_dom = '2023_enplaned_passengers_dom'
        col_inter = '2023_enplaned_passengers_inter'
    else:  # 2022
        col_dom = '2022_enplaned_passengers_dom'
        col_inter = '2022_enplaned_passengers_inter'
    
    # Crear DataFrame con todos los aeropuertos
    df_proporciones = pd.DataFrame()
    df_proporciones['airport'] = df_domestic['airport']
    
    # Limpiar y convertir valores a enteros, manejando None, NaN, y strings
    df_proporciones['vuelos_domesticos'] = pd.to_numeric(df_domestic[col_dom], errors='coerce').fillna(0).astype(int)
    df_proporciones['vuelos_internacionales'] = pd.to_numeric(df_international[col_inter], errors='coerce').fillna(0).astype(int)
    
    # Calcular totales
    df_proporciones['total_vuelos'] = df_proporciones['vuelos_domesticos'] + df_proporciones['vuelos_internacionales']
    
    # Calcular porcentajes
    # Manejar casos especiales cuando total_vuelos es 0
    df_proporciones['pct_domesticos'] = np.where(
        df_proporciones['total_vuelos'] > 0,
        (df_proporciones['vuelos_domesticos'] / df_proporciones['total_vuelos']) * 100,
        np.where(
            df_proporciones['vuelos_domesticos'] > 0,
            100.0,  # Si solo hay vuelos domésticos, 100%
            0.0     # Si no hay vuelos de ningún tipo, 0%
        )
    )
    df_proporciones['pct_internacionales'] = np.where(
        df_proporciones['total_vuelos'] > 0,
        (df_proporciones['vuelos_internacionales'] / df_proporciones['total_vuelos']) * 100,
        np.where(
            df_proporciones['vuelos_internacionales'] > 0,
            100.0,  # Si solo hay vuelos internacionales, 100%
            0.0     # Si no hay vuelos de ningún tipo, 0%
        )
    )
    
    # Asegurar que los porcentajes sean números enteros o decimales, no NaN
    df_proporciones['pct_domesticos'] = df_proporciones['pct_domesticos'].fillna(0).round(2)
    df_proporciones['pct_internacionales'] = df_proporciones['pct_internacionales'].fillna(0).round(2)
    
    # Clasificar aeropuertos por tipo de tráfico
    def clasificar_aeropuerto(pct_dom, pct_inter):
        if pct_dom >= 90:
            return "Predominantemente Doméstico"
        elif pct_inter >= 90:
            return "Predominantemente Internacional"
        elif pct_dom >= 70:
            return "Mayormente Doméstico"
        elif pct_inter >= 70:
            return "Mayormente Internacional"
        elif pct_dom >= 60:
            return "Balanceado-Doméstico"
        elif pct_inter >= 60:
            return "Balanceado-Internacional"
        else:
            return "Balanceado"
    
    df_proporciones['clasificacion'] = df_proporciones.apply(
        lambda row: clasificar_aeropuerto(row['pct_domesticos'], row['pct_internacionales']), 
        axis=1
    )
    
    # Ordenar por total de vuelos descendente
    df_proporciones = df_proporciones.sort_values('total_vuelos', ascending=False).reset_index(drop=True)
    
    return df_proporciones

# Calcular proporciones
df_proporciones = calcular_proporciones_por_aeropuerto(df_domestic, df_international, año_seleccionado)

# Mostrar resumen general
st.subheader("📊 Resumen General")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "Total Aeropuertos",
        len(df_proporciones),
        help="Número total de aeropuertos en el análisis"
    )

with col2:
    total_domestic = df_proporciones['vuelos_domesticos'].sum()
    st.metric(
        "Total Vuelos Domésticos",
        f"{total_domestic:,.0f}",
        help="Suma total de vuelos domésticos"
    )

with col3:
    total_international = df_proporciones['vuelos_internacionales'].sum()
    st.metric(
        "Total Vuelos Internacionales",
        f"{total_international:,.0f}",
        help="Suma total de vuelos internacionales"
    )

with col4:
    pct_domestic_global = (total_domestic / (total_domestic + total_international)) * 100
    st.metric(
        "Porcentaje de vuelos domésticos",
        f"{pct_domestic_global:.1f}%",
        help="Porcentaje global de vuelos domésticos"
    )

with col5:
    pct_international_global = (total_international / (total_domestic + total_international)) * 100
    st.metric(
        "Porcentaje de vuelos internacionales",
        f"{pct_international_global:.1f}%",
        help="Porcentaje global de vuelos internacionales"
    )

st.markdown("---")

# Búsqueda y filtrado de aeropuertos
st.subheader("🔍 Búsqueda de Aeropuertos")

col1, col2 = st.columns([2, 1])

with col1:
    # Búsqueda por nombre de aeropuerto
    aeropuerto_buscar = st.text_input(
        "Buscar aeropuerto:",
        placeholder="Escribe el nombre del aeropuerto...",
        help="Busca un aeropuerto específico por nombre"
    )

with col2:
    # Filtro por clasificación
    clasificaciones = ['Todas'] + list(df_proporciones['clasificacion'].unique())
    clasificacion_filtro = st.selectbox(
        "Filtrar por clasificación:",
        options=clasificaciones,
        help="Filtra aeropuertos por tipo de tráfico"
    )

# Aplicar filtros
df_filtrado = df_proporciones.copy()

if aeropuerto_buscar:
    df_filtrado = df_filtrado[df_filtrado['airport'].str.contains(aeropuerto_buscar, case=False, na=False)]

if clasificacion_filtro != 'Todas':
    df_filtrado = df_filtrado[df_filtrado['clasificacion'] == clasificacion_filtro]

st.markdown("---")

# Visualización de aeropuertos
st.subheader("📈 Análisis Detallado por Aeropuerto")

# Selector de vista usando tabs
tab1, tab2, tab3 = st.tabs(["📊 Tabla Completa", "📈 Gráfico de Barras", "🥧 Gráfico de Pie"])

with tab1:
    # Mostrar tabla completa
    st.markdown(f"### Tabla Completa - {año_seleccionado}")
    
    # Preparar datos para la tabla
    df_tabla = df_filtrado.copy()
    
    # Asegurar que todas las columnas numéricas estén limpias
    df_tabla['vuelos_domesticos'] = pd.to_numeric(df_tabla['vuelos_domesticos'], errors='coerce').fillna(0).astype(int)
    df_tabla['vuelos_internacionales'] = pd.to_numeric(df_tabla['vuelos_internacionales'], errors='coerce').fillna(0).astype(int)
    df_tabla['total_vuelos'] = pd.to_numeric(df_tabla['total_vuelos'], errors='coerce').fillna(0).astype(int)
    df_tabla['pct_domesticos'] = pd.to_numeric(df_tabla['pct_domesticos'], errors='coerce').fillna(0).round(2)
    df_tabla['pct_internacionales'] = pd.to_numeric(df_tabla['pct_internacionales'], errors='coerce').fillna(0).round(2)
    
    # Seleccionar columnas para mostrar
    columnas_mostrar = ['airport', 'vuelos_domesticos', 'vuelos_internacionales', 'total_vuelos', 
                       'pct_domesticos', 'pct_internacionales', 'clasificacion']
    
    st.dataframe(
        df_tabla[columnas_mostrar],
        use_container_width=True,
        column_config={
            "airport": "Aeropuerto",
            "vuelos_domesticos": st.column_config.NumberColumn(
                "Vuelos Domésticos",
                help="Número de vuelos domésticos",
                format="%d"
            ),
            "vuelos_internacionales": st.column_config.NumberColumn(
                "Vuelos Internacionales",
                help="Número de vuelos internacionales", 
                format="%d"
            ),
            "total_vuelos": st.column_config.NumberColumn(
                "Total Vuelos",
                help="Total de vuelos (domésticos + internacionales)",
                format="%d"
            ),
            "pct_domesticos": st.column_config.NumberColumn(
                "% Domésticos",
                help="Porcentaje de vuelos domésticos",
                format="%.2f%%"
            ),
            "pct_internacionales": st.column_config.NumberColumn(
                "% Internacionales",
                help="Porcentaje de vuelos internacionales",
                format="%.2f%%"
            ),
            "clasificacion": "Clasificación"
        }
    )

with tab2:
    # Gráfico de barras horizontales
    st.markdown(f"### Gráfico de Barras - {año_seleccionado}")
    
    # Crear gráfico de barras apiladas
    fig = go.Figure()
    
    # Agregar barras para vuelos domésticos
    fig.add_trace(go.Bar(
        y=df_filtrado['airport'],
        x=df_filtrado['vuelos_domesticos'],
        name='Vuelos Domésticos',
        orientation='h',
        marker_color='#1f77b4'
    ))
    
    # Agregar barras para vuelos internacionales
    fig.add_trace(go.Bar(
        y=df_filtrado['airport'],
        x=df_filtrado['vuelos_internacionales'],
        name='Vuelos Internacionales',
        orientation='h',
        marker_color='#ff7f0e'
    ))
    
    fig.update_layout(
        title=f'Distribución de Vuelos por Aeropuerto - {año_seleccionado}',
        xaxis_title='Número de Vuelos',
        yaxis_title='Aeropuerto',
        barmode='stack',
        height=max(400, len(df_filtrado) * 30),
            xaxis=dict(
                tickmode='linear',
                tick0=0,
                dtick=5000000,
                tickformat='~s',  # Abrevia: 5M, 10M, 15M
                ticksuffix=''     # No agrega nada más al final
            )
    )
    
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    # Gráfico de torta para distribución global
    st.markdown(f"### Distribución Global - {año_seleccionado}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de torta para vuelos totales
        fig_torta_vuelos = px.pie(
            values=[total_domestic, total_international],
            names=['Domésticos', 'Internacionales'],
            title=f'Distribución Global de Vuelos - {año_seleccionado}',
            color_discrete_sequence=['#1f77b4', '#ff7f0e']
        )
        st.plotly_chart(fig_torta_vuelos, use_container_width=True)
 

# Análisis de aeropuertos específicos
if len(df_filtrado) > 0:
    st.markdown("---")
    st.subheader("🎯 Análisis de Aeropuertos Específicos")
    
    # Selector de aeropuerto específico
    aeropuerto_especifico = st.selectbox(
        "Selecciona un aeropuerto para análisis detallado:",
        options=df_filtrado['airport'].tolist(),
        help="Selecciona un aeropuerto para ver su análisis detallado"
    )
    
    if aeropuerto_especifico:
        # Obtener datos del aeropuerto seleccionado
        aeropuerto_data = df_filtrado[df_filtrado['airport'] == aeropuerto_especifico].iloc[0]
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Vuelos Domésticos",
                f"{aeropuerto_data['vuelos_domesticos']:,.0f}",
                f"{aeropuerto_data['pct_domesticos']:.1f}%"
            )
        
        with col2:
            st.metric(
                "Vuelos Internacionales",
                f"{aeropuerto_data['vuelos_internacionales']:,.0f}",
                f"{aeropuerto_data['pct_internacionales']:.1f}%"
            )
        
        with col3:
            st.metric(
                "Total Vuelos",
                f"{aeropuerto_data['total_vuelos']:,.0f}",
                aeropuerto_data['clasificacion']
            )
        
        # Gráfico de barras individual
        fig_individual = go.Figure()
        
        fig_individual.add_trace(go.Bar(
            x=['Domésticos', 'Internacionales'],
            y=[aeropuerto_data['vuelos_domesticos'], aeropuerto_data['vuelos_internacionales']],
            marker_color=['#1f77b4', '#ff7f0e'],
            text=[f"{aeropuerto_data['vuelos_domesticos']:,.0f}", f"{aeropuerto_data['vuelos_internacionales']:,.0f}"],
            textposition='auto'
        ))
        
        fig_individual.update_layout(
            title=f'Distribución de Vuelos - {aeropuerto_especifico} ({año_seleccionado})',
            yaxis_title='Número de Vuelos',
            showlegend=False
        )
        
        st.plotly_chart(fig_individual, use_container_width=True)

# Información adicional
st.markdown("---")
st.markdown("### ℹ️ Información sobre las Clasificaciones")

with st.expander("Explicación de las clasificaciones de aeropuertos"):
    st.markdown("""
    **Clasificaciones por Tipo de Tráfico:**
    
    - **Predominantemente Doméstico** (≥90% doméstico): Aeropuertos que manejan principalmente vuelos nacionales
    - **Predominantemente Internacional** (≥90% internacional): Aeropuertos con enfoque en vuelos internacionales
    - **Mayormente Doméstico** (70-89% doméstico): Aeropuertos con mayoría doméstica pero con presencia internacional
    - **Mayormente Internacional** (70-89% internacional): Aeropuertos con mayoría internacional pero con tráfico doméstico
    - **Balanceado-Doméstico** (60-69% doméstico): Aeropuertos con distribución relativamente equilibrada, tendiendo a doméstico
    - **Balanceado-Internacional** (60-69% internacional): Aeropuertos con distribución relativamente equilibrada, tendiendo a internacional
    - **Balanceado** (40-59% cada uno): Aeropuertos con distribución muy equilibrada entre doméstico e internacional
    
    **Nota:** Los porcentajes se calculan basándose en el número de pasajeros en vuelos domésticos vs internacionales.
    """)