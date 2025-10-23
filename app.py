import streamlit as st
<<<<<<< Updated upstream
from utils.database import obtener_datos
=======
from utils.database import obtener_datos, ejecutar_query_sql
>>>>>>> Stashed changes
import pandas as pd

# Configurar la página
st.set_page_config(
    page_title="Estadísticas de Aeropuertos",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título principal
st.title("✈️ Análisis exploratorio de tráfico aéreo en EE.UU 2022-2023")
st.markdown("---")

# ========== OPCIÓN 1: PESTAÑAS SIMPLES QUE SÍ FUNCIONAN ==========
menu = st.radio(
    "¿Qué quieres ver?",
    ["📊 Datos Predefinidos", "🔍 Consultas SQL"],
    horizontal=True
)

# ========== OPCIÓN 1: TUS DATOS ORIGINALES ==========
if menu == "📊 Datos Predefinidos":
    st.subheader("📋 Base de Datos")

    # Selector de tabla
    tabla_seleccionada = st.selectbox(
        "Tabla a consultar:",
        ["city", "state", "airports", "domestic", "international", "total"],
        index=2  # Por defecto mostrar airports
    )

    # Obtener datos basado en la tabla seleccionada
    with st.spinner(f"Cargando datos de la tabla {tabla_seleccionada}..."):
        df = obtener_datos(tabla_seleccionada)

    if not df.empty:    
        # Mostrar información básica
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total de Registros", len(df))
        
        with col2:
            st.metric("Total de Columnas", len(df.columns))

        if tabla_seleccionada == "domestic":
            with col3:
                total_pasajeros = df['2023_enplaned_passengers_dom'].sum()
                st.metric("Total Pasajeros 2023", f"{total_pasajeros:,.0f}")

            with col4:
                total_pasajeros = df['2022_enplaned_passengers_dom'].sum()
                st.metric("Total Pasajeros 2022", f"{total_pasajeros:,.0f}")
        elif tabla_seleccionada == "international":
            with col3:
                total_pasajeros = df['2023_enplaned_passengers_inter'].sum()
                st.metric("Total Pasajeros 2023", f"{total_pasajeros:,.0f}")

            with col4:
                total_pasajeros = df['2022_enplaned_passengers_inter'].sum()
                st.metric("Total Pasajeros 2022", f"{total_pasajeros:,.0f}")
        else:
            with col3:
                st.metric("Tabla", tabla_seleccionada.title())
        
        st.markdown("---")
        
        # Mostrar todos los datos
        st.dataframe(df, width='stretch')
        
        # Botón para descargar
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Descargar CSV",
            data=csv,
            file_name=f"{tabla_seleccionada}_data.csv",
            mime="text/csv"
        )

    else:
        st.error(f"❌ No se pudieron cargar los datos de la tabla '{tabla_seleccionada}'")

<<<<<<< Updated upstream
# ========== OPCIÓN 2: CONSULTAS SQL MÁGICAS ==========
elif menu == "🔍 Consultas SQL":
    st.subheader("🔍 Consultas SQL Personalizadas")
=======
# ========== OPCIÓN 2: CONSULTAS SQL REALES ==========
elif menu == "🔍 Consultas SQL":
    st.subheader("🔍 Consultas SQL - EJECUCIÓN REAL")
>>>>>>> Stashed changes
    
    # Crear pestañas para los diferentes tipos de consultas
    tab_queries, tab_custom = st.tabs(["🚀 Queries Predefinidos", "📝 SQL Personalizado"])
    
    # ========== PESTAÑA 1: QUERIES PREDEFINIDOS ==========
    with tab_queries:
        st.write("**Selecciona una consulta predefinida para ejecutar:**")
        
        # Selector de queries predefinidos
        query_seleccionado = st.selectbox(
            "Consultas disponibles:",
            [
                "🏆 Top 18 - Mayor Crecimiento Doméstico 2022-2023",
                "📈 Aeropuertos con Crecimiento >20% Doméstico", 
                "🌎 Participación de Pasajeros Internacionales por Aeropuerto",
                "🗺️ Top 5 Estados con Más Pasajeros Totales",
                "⬆️ Aeropuertos que Mejoraron su Ranking Total"
            ]
        )
        
<<<<<<< Updated upstream
        # QUERY 1: Top 18 crecimiento doméstico
        if query_seleccionado == "🏆 Top 18 - Mayor Crecimiento Doméstico 2022-2023":
            st.info("**Consulta:** Top 18 aeropuertos con mayor crecimiento porcentual en pasajeros domésticos (2022-2023)")
            
            # Simulación de resultados (reemplazar con conexión real a BD)
            datos_ejemplo = {
                'name': [
                    'Provo Municipal', 'Tweed New Haven', 'Brownsville South Padre Island International',
                    'Akron-Canton Regional', 'Westchester County', 'Great Falls International',
                    'Daytona Beach International', 'Jackson Hole', 'Meadows Field', 'Huntsville International',
                    'Rafael Hernandez', 'Asheville Regional', 'Wilmington International', 
                    'Raleigh-Durham International', 'Cherry Capital', 'Portland International Jetport',
                    'Myrtle Beach International', 'Boise Air Terminal'
                ],
                'percentage_change_2022_2023_dom': [
                    96.7, 39.3, 35.6, 29.3, 25.9, 25.5, 24.2, 23.8, 23.8, 23.2,
                    23.1, 22.1, 21.3, 20.8, 20.5, 20.3, 20.1, 19.8
                ]
            }
            
            df_resultado = pd.DataFrame(datos_ejemplo)
            st.dataframe(df_resultado, width='stretch')
            
            # Mostrar el query SQL
            with st.expander("🔍 Ver Query SQL"):
                st.code("""
SELECT 
    a.name,
    d.percentage_change_2022_2023_dom
FROM domestic as d
INNER JOIN airports as a ON d.airport_id = a.id
ORDER BY percentage_change_2022_2023_dom DESC
LIMIT 18;
                """, language='sql')
        
        # QUERY 2: Crecimiento >20% doméstico
        elif query_seleccionado == "📈 Aeropuertos con Crecimiento >20% Doméstico":
            st.info("**Consulta:** Aeropuertos con crecimiento mayor al 20% en pasajeros domésticos")
            
            datos_ejemplo = {
                'name': [
                    'Jackson Hole', 'Meadows Field', 'Huntsville International-Carl T Jones Field',
                    'Rafael Hernandez', 'Asheville Regional', 'Wilmington International',
                    'Raleigh-Durham International', 'Cherry Capital', 'Portland International Jetport',
                    'Myrtle Beach International', 'Boise Air Terminal', 'Dane County Regional',
                    'Portland International', 'San Antonio International', 'Palm Beach International'
                ],
                'percentage_change_2022_2023_dom': [
                    23.8, 23.8, 23.2, 23.1, 22.1, 21.3, 20.8, 20.5, 20.3, 20.1,
                    19.8, 19.6, 19.4, 19.2, 19.0
                ]
            }
            
            df_resultado = pd.DataFrame(datos_ejemplo)
            st.dataframe(df_resultado, width='stretch')
            
            with st.expander("🔍 Ver Query SQL"):
                st.code("""
SELECT 
    a.name,
    d.percentage_change_2022_2023_dom
FROM domestic as d
INNER JOIN airports as a ON d.airport_id = a.id
WHERE percentage_change_2022_2023_dom >= 20
ORDER BY percentage_change_2022_2023_dom DESC;
                """, language='sql')
        
        # QUERY 3: Participación internacional
        elif query_seleccionado == "🌎 Participación de Pasajeros Internacionales por Aeropuerto":
            st.info("**Consulta:** Proporción de pasajeros internacionales por aeropuerto")
            
            datos_ejemplo = {
                'airport_name': [
                    'John Wayne Airport-Orange County', 'Southwest Florida International',
                    'Louis Armstrong New Orleans International', 'Francisco C. Ada Saipan International',
                    'Kahului Airport', 'Fresno Yosemite International', 'Cleveland-Hopkins International',
                    'TOTAL'
                ],
                'proportion': [0.002, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 1.000]
            }
            
            df_resultado = pd.DataFrame(datos_ejemplo)
            st.dataframe(df_resultado, width='stretch')
            
            with st.expander("🔍 Ver Query SQL"):
                st.code("""
WITH total AS (
    SELECT sum("2023_enplaned_passengers_inter") as total_passengers
    FROM international
)
SELECT
    COALESCE(a.name, 'TOTAL') as airport_name,
    ROUND(sum(i."2023_enplaned_passengers_inter") / (SELECT total_passengers FROM total), 3) AS proportion
FROM international as i
INNER JOIN airports as a ON a.id = i.airport_id
GROUP BY ROLLUP(a.name)
ORDER BY CASE WHEN a.name IS NULL THEN 1 ELSE 0 END, proportion DESC;
                """, language='sql')
        
        # QUERY 4: Top 5 estados
        elif query_seleccionado == "🗺️ Top 5 Estados con Más Pasajeros Totales":
            st.info("**Consulta:** Top 5 estados con mayor número total de pasajeros")
            
            datos_ejemplo = {
                'states': ['CA', 'FL', 'TX', 'GA', 'NY'],
                'total_passengers': [102368701, 86210614, 84310827, 50925180, 46683417]
            }
            
            df_resultado = pd.DataFrame(datos_ejemplo)
            st.dataframe(df_resultado, width='stretch')
            
            # Gráfico de barras
            st.bar_chart(df_resultado.set_index('states')['total_passengers'])
            
            with st.expander("🔍 Ver Query SQL"):
                st.code("""
WITH total AS (
    SELECT
        sum(i."2023_enplaned_passengers_inter" + d."2023_enplaned_passengers_dom") as total_passengers,
        s.name as states
    FROM international as i
    INNER JOIN domestic as d on d.airport_id = i.airport_id
    INNER JOIN airports as a on a.id = i.airport_id
    INNER JOIN state as s on s.id = a.state_id
    GROUP BY s.name
)
SELECT
    DISTINCT states,
    total_passengers
FROM total
ORDER BY total_passengers DESC
LIMIT 5;
                """, language='sql')
        
        # QUERY 5: Mejora de ranking
        elif query_seleccionado == "⬆️ Aeropuertos que Mejoraron su Ranking Total":
            st.info("**Consulta:** Aeropuertos que mejoraron su ranking total del 2022 al 2023")
            
            datos_ejemplo = {
                'name': [
                    'Los Angeles International', 'Orlando International', 'Charlotte Douglas International',
                    'Seattle/Tacoma International', 'Newark Liberty International', 'San Francisco International',
                    'Baltimore/Washington International Thurgood Marshall', 'Washington Dulles International'
                ],
                '2022_rank_total': [5, 8, 10, 11, 13, 14, 25, 28],
                '2023_rank_total': [4, 7, 9, 10, 12, 13, 23, 26]
            }
            
            df_resultado = pd.DataFrame(datos_ejemplo)
            st.dataframe(df_resultado, width='stretch')
            
            with st.expander("🔍 Ver Query SQL"):
                st.code("""
SELECT  
    a.name,  
    "2022_rank_total",  
    "2023_rank_total"  
FROM total as t  
INNER JOIN airports as a on a.id = t.airport_id  
WHERE "2023_rank_total" < "2022_rank_total"  
ORDER BY "2023_rank_total" ASC;
                """, language='sql')
=======
        # Botón para ejecutar el query seleccionado
        if st.button("🚀 Ejecutar Query Seleccionado", type="primary"):
            
            # QUERY 1: Top 18 crecimiento doméstico
            if query_seleccionado == "🏆 Top 18 - Mayor Crecimiento Doméstico 2022-2023":
                st.info("**Ejecutando:** Top 18 aeropuertos con mayor crecimiento porcentual en pasajeros domésticos")
                
                query_sql = """
                SELECT 
                    a.name,
                    d.percentage_change_2022_2023_dom
                FROM domestic as d
                INNER JOIN airports as a ON d.airport_id = a.id
                ORDER BY percentage_change_2022_2023_dom DESC
                LIMIT 18;
                """
                
                with st.spinner("Ejecutando consulta en la base de datos REAL..."):
                    try:
                        # ¡ESTA ES LA PARTE IMPORTANTE! Ejecuta el query REAL
                        df_resultado = ejecutar_query_sql(query_sql)
                        st.dataframe(df_resultado, width='stretch')
                        st.success(f"✅ Se encontraron {len(df_resultado)} registros REALES")
                    except Exception as e:
                        st.error(f"❌ Error ejecutando query: {e}")
                
                with st.expander("🔍 Ver Query SQL"):
                    st.code(query_sql, language='sql')
            
            # Los demás queries siguen igual...
            # ... (el resto del código que te pasé antes)
>>>>>>> Stashed changes
    
    # ========== PESTAÑA 2: SQL PERSONALIZADO ==========
    with tab_custom:
        st.write("Escribe tus propias consultas SQL para explorar los datos")
        
<<<<<<< Updated upstream
        # Ejemplos de consultas para ayudar
        with st.expander("💡 Ejemplos de consultas"):
            st.code("""
-- Aeropuertos con más pasajeros en 2023
SELECT airport_name, "2023_enplaned_passengers_total" 
FROM total 
ORDER BY "2023_enplaned_passengers_total" DESC 
LIMIT 10;

-- Aeropuertos internacionales más importantes
SELECT airport_name, "2023_enplaned_passengers_inter" 
FROM international 
WHERE "2023_enplaned_passengers_inter" > 0 
ORDER BY "2023_enplaned_passengers_inter" DESC;

-- Aeropuertos de un estado específico
SELECT * FROM airports WHERE state = 'CA';
            """)
        
=======
>>>>>>> Stashed changes
        # Cuadro grande para escribir SQL
        query_sql = st.text_area(
            "Escribe tu consulta SQL aquí:",
            height=150,
            placeholder="SELECT * FROM airports WHERE state = 'CA';"
        )
        
        # Botón mágico para ejecutar
        if st.button("🚀 Ejecutar Query Personalizado", type="primary"):
            if query_sql.strip():
<<<<<<< Updated upstream
                # Guardar el query en la memoria mágica
                st.session_state['query_actual'] = query_sql
            else:
                st.warning("📝 Escribe una consulta SQL primero")
        
        # Mostrar resultados si hay un query guardado
        if 'query_actual' in st.session_state and st.session_state['query_actual']:
            st.write("**Tu consulta:**")
            st.code(st.session_state['query_actual'], language='sql')
            
            st.write("**Resultados:**")
            
            # Simulación de resultados (por ahora)
            with st.spinner("Ejecutando consulta..."):
                try:
                    # Por ahora mostramos datos de ejemplo
                    st.info("🔧 Esta función estará disponible pronto")
                    st.info("Mientras tanto, puedes usar los queries predefinidos arriba ↑")
                    
                    # Mostramos un ejemplo de cómo se verán los datos
                    df_ejemplo = obtener_datos("airports").head(5)
                    st.write("**Ejemplo de cómo se verán tus resultados:**")
                    st.dataframe(df_ejemplo)
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
=======
                with st.spinner("Ejecutando consulta en la base de datos REAL..."):
                    try:
                        # ¡ESTA ES LA PARTE IMPORTANTE! Ejecuta el query REAL
                        df_resultado = ejecutar_query_sql(query_sql)
                        st.write("**Tu consulta:**")
                        st.code(query_sql, language='sql')
                        st.write("**Resultados REALES:**")
                        st.dataframe(df_resultado, width='stretch')
                        st.success(f"✅ Se encontraron {len(df_resultado)} registros REALES")
                    except Exception as e:
                        st.error(f"❌ Error en la consulta: {e}")
            else:
                st.warning("📝 Escribe una consulta SQL primero")
>>>>>>> Stashed changes

# Footer
st.markdown("---")
st.markdown("📊 **✈️ Análisis exploratorio de tráfico aéreo en EE.UU 2022-2023** - Grupo 5 (Computación 2) - Universidad Central de Venezuela")