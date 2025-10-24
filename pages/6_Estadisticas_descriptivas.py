import streamlit as st
from utils.database import obtener_datos
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats
import numpy as np

# Configurar la página
st.set_page_config(
    page_title="Estadísticas Descriptivas de Pasajeros por Aeropuerto",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título principal
st.title("📊 Estadísticas Descriptivas de Pasajeros por Aeropuerto")
st.markdown("---")
st.markdown("Análisis estadístico del número de pasajeros en aeropuertos de EE.UU. para los años 2022 y 2023")

# Obtener datos
with st.spinner("Cargando datos..."):
    df_total = obtener_datos('total')
    df_domestic = obtener_datos('domestic')
    df_international = obtener_datos('international')

# Verificar que los datos se cargaron correctamente
if df_total.empty or df_domestic.empty or df_international.empty:
    st.error("❌ No se pudieron cargar los datos. Verifica la conexión a la base de datos.")
    st.stop()

# Convertir columnas a string para evitar errores
df_total['airport'] = df_total['airport'].astype(str)
df_domestic['airport'] = df_domestic['airport'].astype(str)
df_international['airport'] = df_international['airport'].astype(str)

# Sidebar para selección de tipo de flujo
st.sidebar.header("🔧 Configuración del Análisis")

tipo_flujo = st.sidebar.selectbox(
    "Selecciona el tipo de flujo:",
    options=['total', 'domestic', 'international'],
    format_func=lambda x: x.capitalize(),
    help="Selecciona si quieres analizar el flujo total, doméstico o internacional"
)

# Función para calcular estadísticas descriptivas
def calcular_estadisticas_descriptivas(df, columnas_pasajeros, tipo_flujo):
    """
    Calcula estadísticas descriptivas para las columnas de pasajeros especificadas
    """
    estadisticas = {}
    
    for col in columnas_pasajeros:
        if col in df.columns:
            # Filtrar valores nulos y negativos
            datos_limpios = df[col].dropna()
            datos_limpios = datos_limpios[datos_limpios >= 0]
            
            if len(datos_limpios) > 0:
                estadisticas[col] = {
                    'count': len(datos_limpios),
                    'mean': datos_limpios.mean(),
                    'median': datos_limpios.median(),
                    'std': datos_limpios.std(),
                    'min': datos_limpios.min(),
                    'max': datos_limpios.max(),
                    'q25': datos_limpios.quantile(0.25),
                    'q75': datos_limpios.quantile(0.75),
                    'skewness': datos_limpios.skew(),
                    'kurtosis': datos_limpios.kurtosis()
                }
    
    return estadisticas

# Función para crear visualizaciones
def crear_visualizaciones(df, columnas_pasajeros, tipo_flujo):
    """
    Crea visualizaciones para las estadísticas descriptivas
    """
    visualizaciones = {}
    
    for col in columnas_pasajeros:
        if col in df.columns:
            # Filtrar datos
            datos_limpios = df[col].dropna()
            datos_limpios = datos_limpios[datos_limpios >= 0]
            
            if len(datos_limpios) > 0:
                # Histograma
                año = "2023" if "2023" in col else "2022"
                fig_hist = px.histogram(
                    x=datos_limpios,
                    nbins=50,
                    title=f'Distribución de Pasajeros Embarcados en {año}',
                    labels={'x': 'Pasajeros Embarcados', 'y': 'Frecuencia'},
                    color_discrete_sequence=['#1f77b4']
                )
                fig_hist.update_layout(
                    xaxis_title='Pasajeros Embarcados',
                    yaxis_title='Frecuencia',
                    showlegend=False
                )
                visualizaciones[f'hist_{col}'] = fig_hist
                
                # Box plot
                año = "2023" if "2023" in col else "2022"
                fig_box = px.box(
                    y=datos_limpios,
                    title=f'Box Plot de Pasajeros Embarcados en {año}',
                    labels={'y': 'Pasajeros Embarcados'},
                    color_discrete_sequence=['#ff7f0e']
                )
                fig_box.update_layout(
                    yaxis_title='Pasajeros Embarcados',
                    showlegend=False
                )
                visualizaciones[f'box_{col}'] = fig_box
                
                fig_qq = go.Figure()
                
                # Calcular percentiles teóricos y muestrales
                n = len(datos_limpios)
                percentiles_teoricos = np.linspace(0.01, 0.99, n)
                percentiles_muestrales = np.percentile(datos_limpios, percentiles_teoricos * 100)
                percentiles_normales = stats.norm.ppf(percentiles_teoricos, 
                                                    loc=np.mean(datos_limpios), 
                                                    scale=np.std(datos_limpios))
                
                # Agregar línea de referencia (distribución normal)
                fig_qq.add_trace(go.Scatter(
                    x=percentiles_normales,
                    y=percentiles_muestrales,
                    mode='markers',
                    name='Datos vs Normal',
                    marker=dict(color='#e74c3c', size=6)
                ))
                
                # Línea de referencia perfecta
                min_val = min(percentiles_normales.min(), percentiles_muestrales.min())
                max_val = max(percentiles_normales.max(), percentiles_muestrales.max())
                fig_qq.add_trace(go.Scatter(
                    x=[min_val, max_val],
                    y=[min_val, max_val],
                    mode='lines',
                    name='Línea de Referencia',
                    line=dict(color='#2c3e50', dash='dash')
                ))
                
                fig_qq.update_layout(
                    title=f'Análisis de Asimetría en {año}',
                    xaxis_title='Cuantiles Teóricos (Normal)',
                    yaxis_title='Cuantiles Muestrales',
                    showlegend=True
                )
                visualizaciones[f'qq_{col}'] = fig_qq
                
                # Gráfica de Curtosis (Histograma con curva normal superpuesta)
                fig_kurt = px.histogram(
                    x=datos_limpios,
                    nbins=50,
                    title=f'Análisis de Curtosis - Distribución vs Normal en {año}',
                    labels={'x': 'Pasajeros Embarcados', 'y': 'Densidad'},
                    color_discrete_sequence=['#9b59b6'],
                    histnorm='probability density'
                )
                
                # Agregar curva normal teórica
                x_range = np.linspace(datos_limpios.min(), datos_limpios.max(), 100)
                normal_curve = stats.norm.pdf(x_range, 
                                            loc=np.mean(datos_limpios), 
                                            scale=np.std(datos_limpios))
                
                fig_kurt.add_trace(go.Scatter(
                    x=x_range,
                    y=normal_curve,
                    mode='lines',
                    name='Distribución Normal Teórica',
                    line=dict(color='#e67e22', width=3)
                ))
                
                fig_kurt.update_layout(
                    xaxis_title='Pasajeros Embarcados',
                    yaxis_title='Densidad de Probabilidad',
                    showlegend=True
                )
                visualizaciones[f'kurt_{col}'] = fig_kurt
    
    return visualizaciones

# Determinar columnas según el tipo de flujo
if tipo_flujo == 'total':
    df_analisis = df_total
    columnas_pasajeros = ['2023_enplaned_passengers_total', '2022_enplaned_passengers_total']
    titulo_analisis = "Total de Pasajeros"
elif tipo_flujo == 'domestic':
    df_analisis = df_domestic
    columnas_pasajeros = ['2023_enplaned_passengers_dom', '2022_enplaned_passengers_dom']
    titulo_analisis = "Pasajeros Domésticos"
else:  # international
    df_analisis = df_international
    columnas_pasajeros = ['2023_enplaned_passengers_inter', '2022_enplaned_passengers_inter']
    titulo_analisis = "Pasajeros Internacionales"

# Calcular estadísticas descriptivas
estadisticas = calcular_estadisticas_descriptivas(df_analisis, columnas_pasajeros, tipo_flujo)

# Mostrar resumen general
st.subheader(f"📈 Resumen General - {titulo_analisis}")

col1, col2, col3, col4 = st.columns(4)

if '2023_enplaned_passengers_total' in estadisticas or '2023_enplaned_passengers_dom' in estadisticas or '2023_enplaned_passengers_inter' in estadisticas:
    col_2023 = [col for col in columnas_pasajeros if '2023' in col][0]
    col_2022 = [col for col in columnas_pasajeros if '2022' in col][0]
    
    with col1:
        st.metric(
            "Total Aeropuertos",
            len(df_analisis),
            help="Número total de aeropuertos en el análisis"
        )
    
    with col2:
        if col_2023 in estadisticas:
            total_2023 = df_analisis[col_2023].sum()
            st.metric(
                "Total Pasajeros 2023",
                f"{total_2023:,.0f}",
                help="Suma total de pasajeros en 2023"
            )
    
    with col3:
        if col_2022 in estadisticas:
            total_2022 = df_analisis[col_2022].sum()
            st.metric(
                "Total Pasajeros 2022",
                f"{total_2022:,.0f}",
                help="Suma total de pasajeros en 2022"
            )
    
    with col4:
        if col_2023 in estadisticas and col_2022 in estadisticas:
            crecimiento = ((total_2023 - total_2022) / total_2022) * 100
            st.metric(
                "Crecimiento %",
                f"{crecimiento:.2f}%",
                delta=f"{crecimiento:.2f}%",
                help="Porcentaje de crecimiento entre 2022 y 2023"
            )

st.markdown("---")

# Dashboard de estadísticas descriptivas
st.markdown("## 📊 Dashboard Estadístico")

# CSS personalizado para cards con bordes redondeados y sombra
st.markdown("""
<style>
.metric-card {
    background: #344168;
    border-radius: 12px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    padding: 20px;
    margin: 10px 0;
    border: 1px solid #050C24;
    transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}

.metric-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 15px rgba(0, 0, 0, 0.15);
}

.metric-title {
    font-size: 14px;
    font-weight: 600;
    color: #ffffff;
    margin-bottom: 8px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.metric-value {
    font-size: 28px;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 4px;
}

.metric-description {
    font-size: 12px;
    color: #ffffff;
    margin-top: 4px;
}
</style>
""", unsafe_allow_html=True)

# Función para crear cards personalizados
def crear_metric_card(titulo, valor, descripcion=""):
    return f"""
    <div class="metric-card">
        <div class="metric-title">{titulo}</div>
        <div class="metric-value">{valor}</div>
        <div class="metric-description">{descripcion}</div>
    </div>
    """

# Crear tabs para cada año
if len(columnas_pasajeros) == 2:
    tab_2023, tab_2022 = st.tabs(["📈 2023", "📈 2022"])
    
    col_2023 = columnas_pasajeros[0] if "2023" in columnas_pasajeros[0] else columnas_pasajeros[1]
    col_2022 = columnas_pasajeros[1] if "2023" in columnas_pasajeros[0] else columnas_pasajeros[0]
    
    with tab_2023:
        if col_2023 in estadisticas:
            st.markdown("### Estadísticas Descriptivas 2023")
            
            # Primera fila de métricas principales
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(crear_metric_card(
                    "Media",
                    f"{estadisticas[col_2023]['mean']:,.0f}",
                    "Promedio aritmético"
                ), unsafe_allow_html=True)
            
            with col2:
                st.markdown(crear_metric_card(
                    "Mediana",
                    f"{estadisticas[col_2023]['median']:,.0f}",
                    "Valor central"
                ), unsafe_allow_html=True)
            
            with col3:
                st.markdown(crear_metric_card(
                    "Desv. Estándar",
                    f"{estadisticas[col_2023]['std']:,.0f}",
                    "Dispersión de datos"
                ), unsafe_allow_html=True)
            
            with col4:
                st.markdown(crear_metric_card(
                    "Rango",
                    f"{estadisticas[col_2023]['max'] - estadisticas[col_2023]['min']:,.0f}",
                    "Diferencia min-max"
                ), unsafe_allow_html=True)
            
            # Segunda fila de métricas adicionales
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(crear_metric_card(
                    "Mínimo",
                    f"{estadisticas[col_2023]['min']:,.0f}",
                    "Valor más bajo"
                ), unsafe_allow_html=True)
            
            with col2:
                st.markdown(crear_metric_card(
                    "Máximo",
                    f"{estadisticas[col_2023]['max']:,.0f}",
                    "Valor más alto"
                ), unsafe_allow_html=True)
            
            with col3:
                st.markdown(crear_metric_card(
                    "Q1 (25%)",
                    f"{estadisticas[col_2023]['q25']:,.0f}",
                    "Primer cuartil"
                ), unsafe_allow_html=True)
            
            with col4:
                st.markdown(crear_metric_card(
                    "Q3 (75%)",
                    f"{estadisticas[col_2023]['q75']:,.0f}",
                    "Tercer cuartil"
                ), unsafe_allow_html=True)
            
            # Tercera fila para métricas de forma
            col1, col2 = st.columns(2)
            
            with col1:
                skew_val = estadisticas[col_2023]['skewness']
                skew_interpretation = "Sesgada a la derecha" if skew_val > 0.5 else "Sesgada a la izquierda" if skew_val < -0.5 else "Simétrica"
                st.markdown(crear_metric_card(
                    "Asimetría",
                    f"{skew_val:.3f}",
                    skew_interpretation
                ), unsafe_allow_html=True)
            
            with col2:
                kurt_val = estadisticas[col_2023]['kurtosis']
                kurt_interpretation = "Más puntiaguda que la normal" if kurt_val > 0 else "Más plana que la normal" if kurt_val < 0 else "Similar a la normal"
                st.markdown(crear_metric_card(
                    "Curtosis",
                    f"{kurt_val:.3f}",
                    kurt_interpretation
                ), unsafe_allow_html=True)
    
    with tab_2022:
        if col_2022 in estadisticas:
            st.markdown("### Estadísticas Descriptivas 2022")
            
            # Primera fila de métricas principales
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(crear_metric_card(
                    "Media",
                    f"{estadisticas[col_2022]['mean']:,.0f}",
                    "Promedio aritmético"
                ), unsafe_allow_html=True)
            
            with col2:
                st.markdown(crear_metric_card(
                    "Mediana",
                    f"{estadisticas[col_2022]['median']:,.0f}",
                    "Valor central"
                ), unsafe_allow_html=True)
            
            with col3:
                st.markdown(crear_metric_card(
                    "Desv. Estándar",
                    f"{estadisticas[col_2022]['std']:,.0f}",
                    "Dispersión de datos"
                ), unsafe_allow_html=True)
            
            with col4:
                st.markdown(crear_metric_card(
                    "Rango",
                    f"{estadisticas[col_2022]['max'] - estadisticas[col_2022]['min']:,.0f}",
                    "Diferencia min-max"
                ), unsafe_allow_html=True)
            
            # Segunda fila de métricas adicionales
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(crear_metric_card(
                    "Mínimo",
                    f"{estadisticas[col_2022]['min']:,.0f}",
                    "Valor más bajo"
                ), unsafe_allow_html=True)
            
            with col2:
                st.markdown(crear_metric_card(
                    "Máximo",
                    f"{estadisticas[col_2022]['max']:,.0f}",
                    "Valor más alto"
                ), unsafe_allow_html=True)
            
            with col3:
                st.markdown(crear_metric_card(
                    "Q1 (25%)",
                    f"{estadisticas[col_2022]['q25']:,.0f}",
                    "Primer cuartil"
                ), unsafe_allow_html=True)
            
            with col4:
                st.markdown(crear_metric_card(
                    "Q3 (75%)",
                    f"{estadisticas[col_2022]['q75']:,.0f}",
                    "Tercer cuartil"
                ), unsafe_allow_html=True)
            
            # Tercera fila para métricas de forma
            col1, col2 = st.columns(2)
            
            with col1:
                skew_val = estadisticas[col_2022]['skewness']
                skew_interpretation = "Sesgada a la derecha" if skew_val > 0.5 else "Sesgada a la izquierda" if skew_val < -0.5 else "Simétrica"
                st.markdown(crear_metric_card(
                    "Asimetría",
                    f"{skew_val:.3f}",
                    skew_interpretation
                ), unsafe_allow_html=True)
            
            with col2:
                kurt_val = estadisticas[col_2022]['kurtosis']
                kurt_interpretation = "Más puntiaguda que la normal" if kurt_val > 0 else "Más plana que la normal" if kurt_val < 0 else "Similar a la normal"
                st.markdown(crear_metric_card(
                    "Curtosis",
                    f"{kurt_val:.3f}",
                    kurt_interpretation
                ), unsafe_allow_html=True)

# Crear visualizaciones
st.subheader("📈 Visualizaciones")

visualizaciones = crear_visualizaciones(df_analisis, columnas_pasajeros, tipo_flujo)

# Mostrar histogramas
st.markdown("### Distribuciones de Frecuencia")
for col in columnas_pasajeros:
    if f'hist_{col}' in visualizaciones:
        año = "2023" if "2023" in col else "2022"
        st.plotly_chart(visualizaciones[f'hist_{col}'], use_container_width=True)

# Mostrar box plots
st.markdown("### Análisis de Cajas (Box Plots)")
for col in columnas_pasajeros:
    if f'box_{col}' in visualizaciones:
        año = "2023" if "2023" in col else "2022"
        st.plotly_chart(visualizaciones[f'box_{col}'], use_container_width=True)

# Mostrar gráficas de asimetría y curtosis
st.markdown("### Análisis de Forma de la Distribución")

# Crear tabs para asimetría y curtosis
tab_asimetria, tab_curtosis = st.tabs(["📐 Análisis de Asimetría", "📊 Análisis de Curtosis"])

with tab_asimetria:
    st.markdown("""
    **Análisis de Asimetría**
    
    Esta gráfica compara los cuantiles de los datos con los de una distribución normal teórica:
    - **Puntos cerca de la línea diagonal**: Los datos siguen una distribución normal
    - **Puntos por encima de la línea**: Valores más altos de lo esperado (cola derecha)
    - **Puntos por debajo de la línea**: Valores más bajos de lo esperado (cola izquierda)
    """)
    
    for col in columnas_pasajeros:
        if f'qq_{col}' in visualizaciones:
            año = "2023" if "2023" in col else "2022"
            st.plotly_chart(visualizaciones[f'qq_{col}'], use_container_width=True)

with tab_curtosis:
    st.markdown("""
    **Análisis de Curtosis**
    
    Esta gráfica compara la distribución real con una distribución normal teórica:
    - **Curtosis > 0**: Distribución más puntiaguda que la normal (leptocúrtica)
    - **Curtosis < 0**: Distribución más plana que la normal (platicúrtica)
    - **Curtosis ≈ 0**: Similar a la distribución normal (mesocúrtica)
    """)
    
    for col in columnas_pasajeros:
        if f'kurt_{col}' in visualizaciones:
            año = "2023" if "2023" in col else "2022"
            st.plotly_chart(visualizaciones[f'kurt_{col}'], use_container_width=True)

# Comparación entre años
if len(columnas_pasajeros) == 2:
    st.subheader("🔄 Comparación entre Años")
    
    col_2023 = columnas_pasajeros[0] if "2023" in columnas_pasajeros[0] else columnas_pasajeros[1]
    col_2022 = columnas_pasajeros[1] if "2023" in columnas_pasajeros[0] else columnas_pasajeros[0]
    
    if col_2023 in df_analisis.columns and col_2022 in df_analisis.columns:
        # Crear DataFrame para comparación
        df_comparacion = df_analisis[[col_2023, col_2022]].copy()
        df_comparacion = df_comparacion.dropna()
        df_comparacion = df_comparacion[(df_comparacion[col_2023] >= 0) & (df_comparacion[col_2022] >= 0)]
        
        if len(df_comparacion) > 0:
            # Scatter plot de comparación
            fig_scatter = px.scatter(
                df_comparacion,
                x=col_2022,
                y=col_2023,
                title=f'Comparación de Pasajeros: 2022 vs 2023 - {tipo_flujo.capitalize()}',
                labels={
                    col_2022: 'Pasajeros 2022',
                    col_2023: 'Pasajeros 2023'
                },
                color_discrete_sequence=['#2ca02c']
            )
            
            # Agregar línea de referencia (y = x)
            max_val = max(df_comparacion[col_2022].max(), df_comparacion[col_2023].max())
            fig_scatter.add_trace(
                go.Scatter(
                    x=[0, max_val],
                    y=[0, max_val],
                    mode='lines',
                    name='Línea de igualdad (y=x)',
                    line=dict(dash='dash', color='red')
                )
            )
            
            fig_scatter.update_layout(
                xaxis_title='Pasajeros 2022',
                yaxis_title='Pasajeros 2023',
                showlegend=True
            )
            
            st.plotly_chart(fig_scatter, use_container_width=True)
            
            # Calcular correlación
            correlacion = df_comparacion[col_2022].corr(df_comparacion[col_2023])
            st.metric(
                "Correlación entre 2022 y 2023",
                f"{correlacion:.4f}",
                help="Correlación de Pearson entre los datos de 2022 y 2023"
            )

# Información adicional
st.markdown("---")
st.markdown("### ℹ️ Información sobre las Métricas")

with st.expander("Explicación de las estadísticas descriptivas"):
    st.markdown("""
    **Estadísticas Descriptivas:**
    - **Conteo**: Número de aeropuertos con datos válidos
    - **Media**: Promedio aritmético de pasajeros
    - **Mediana**: Valor que divide los datos en dos mitades iguales
    - **Desviación Estándar**: Medida de dispersión de los datos
    - **Mínimo/Máximo**: Valores extremos
    - **Q1/Q3**: Primer y tercer cuartil (25% y 75% de los datos)
    - **Asimetría**: Medida de la simetría de la distribución
    - **Curtosis**: Medida de la "pesadez" de las colas de la distribución
    
    **Interpretación:**
    - **Asimetría > 0**: Distribución sesgada a la derecha (más valores altos)
    - **Asimetría < 0**: Distribución sesgada a la izquierda (más valores bajos)
    - **Curtosis > 0**: Distribución más "puntiaguda" que la normal
    - **Curtosis < 0**: Distribución más "plana" que la normal
    """)

st.markdown("---")
st.markdown("📊 **Análisis Estadístico de Tráfico Aéreo en EE.UU. 2022-2023** - Grupo 5 (Computación 2) - Universidad Central de Venezuela")
