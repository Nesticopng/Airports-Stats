import streamlit as st
import pandas as pd
from utils.database import obtener_datos

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

# ========== OPCIÓN 2: CONSULTAS SQL REALES ==========
elif menu == "🔍 Consultas SQL":
    st.subheader("🔍 Consultas SQL - EJECUCIÓN REAL")
    
    # Crear pestañas para los diferentes tipos de consultas
    tab_queries, tab_custom = st.tabs(["🚀 Queries Predefinidos", "📝 SQL Personalizado"])
    
    # ========== PESTAÑA 1: QUERIES PREDEFINIDOS ==========
    with tab_queries:
        st.write("**Selecciona una consulta predefinida para ejecutar:**")
        
        # Selector de queries predefinidos
        query_seleccionado = st.selectbox(
            "Consultas disponibles:",
            [
                "🏆 Top 10 - Mayor Crecimiento Doméstico 2022-2023",
                "📈 Aeropuertos con Crecimiento >20% Doméstico",
                "🌎 Participación de Pasajeros Internacionales por Aeropuerto",
                "🗺️ Top 5 Estados con Más Pasajeros Totales", 
                "⬆️ Aeropuertos que Mejoraron su Ranking Total"
            ]
        )
        
        # Botón para ejecutar el query seleccionado
        if st.button("🚀 Ejecutar Query Seleccionado", type="primary"):
            
            # QUERY 1: Top 18 crecimiento doméstico
            if query_seleccionado == "🏆 Top 10 - Mayor Crecimiento Doméstico 2022-2023":
                st.info("**Ejecutando:** Top 10 aeropuertos con mayor crecimiento porcentual")
                
                with st.spinner("Cargando datos..."):
                    try:
                        # Usamos la función obtener_datos que ya funciona
                        df = obtener_datos("domestic")
                        if not df.empty:
                            # Seleccionar solo las columnas que necesitamos y ordenar
                            df_resultado = df[['airport', 'percentage_change_2022_2023_dom']]
                            df_resultado = df_resultado.sort_values('percentage_change_2022_2023_dom', ascending=False).head(10)
                            st.dataframe(df_resultado, width='stretch')
                            st.success(f"✅ Se encontraron {len(df_resultado)} registros")
                        else:
                            st.error("❌ No se encontraron datos")
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
            
            # QUERY 2: Crecimiento >20% doméstico
            elif query_seleccionado == "📈 Aeropuertos con Crecimiento >20% Doméstico":
                st.info("**Ejecutando:** Aeropuertos con crecimiento mayor al 20%")
                
                with st.spinner("Cargando datos..."):
                    try:
                        # Usamos la función obtener_datos que ya funciona
                        df = obtener_datos("domestic")
                        if not df.empty:
                            # Filtrar y ordenar
                            df_resultado = df[['airport', 'percentage_change_2022_2023_dom']]
                            df_resultado = df_resultado[df_resultado['percentage_change_2022_2023_dom'] >= 20]
                            df_resultado = df_resultado.sort_values('percentage_change_2022_2023_dom', ascending=False)
                            st.dataframe(df_resultado, width='stretch')
                            st.success(f"✅ Se encontraron {len(df_resultado)} registros")
                        else:
                            st.error("❌ No se encontraron datos")
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
            
            # QUERY 3: Participación internacional por aeropuerto
            elif query_seleccionado == "🌎 Participación de Pasajeros Internacionales por Aeropuerto":
                st.info("**Ejecutando:** Proporción de pasajeros internacionales por aeropuerto")
                
                with st.spinner("Calculando proporciones..."):
                    try:
                        # Obtener datos de internacional
                        df_international = obtener_datos("international")
                        if not df_international.empty:
                            # Calcular total de pasajeros internacionales
                            total_pasajeros_inter = df_international['2023_enplaned_passengers_inter'].sum()
                            
                            # Calcular proporción para cada aeropuerto
                            df_resultado = df_international[['airport', '2023_enplaned_passengers_inter']].copy()
                            df_resultado['proportion'] = df_resultado['2023_enplaned_passengers_inter'] / total_pasajeros_inter
                            df_resultado['proportion'] = df_resultado['proportion'].round(3)
                            
                            # Agregar fila de TOTAL
                            total_row = pd.DataFrame({
                                'airport': ['TOTAL'],
                                '2023_enplaned_passengers_inter': [total_pasajeros_inter],
                                'proportion': [1.000]
                            })
                            
                            df_resultado = pd.concat([df_resultado, total_row], ignore_index=True)
                            df_resultado = df_resultado.rename(columns={'airport': 'airport_name'})
                            
                            # Ordenar por proporción (descendente), con TOTAL al final
                            df_resultado = df_resultado.sort_values('proportion', ascending=False)
                            
                            st.dataframe(df_resultado[['airport_name', 'proportion']], width='stretch')
                            st.success(f"✅ Se calcularon proporciones para {len(df_resultado)-1} aeropuertos")
                        else:
                            st.error("❌ No se encontraron datos internacionales")
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
            
            # QUERY 4: Top 5 estados con más pasajeros totales
            elif query_seleccionado == "🗺️ Top 5 Estados con Más Pasajeros Totales":
                st.info("**Ejecutando:** Top 5 estados con mayor número total de pasajeros")
                
                with st.spinner("Calculando totales por estado..."):
                    try:
                        # Obtener datos de aeropuertos para tener la relación estado-aeropuerto
                        df_airports = obtener_datos("airports")
                        df_domestic = obtener_datos("domestic")
                        df_international = obtener_datos("international")
                        
                        if not df_airports.empty and not df_domestic.empty and not df_international.empty:
                            # Combinar datos
                            df_combined = df_airports[['id', 'state']].merge(
                                df_domestic[['id', '2023_enplaned_passengers_dom']], 
                                on='id', 
                                how='left'
                            ).merge(
                                df_international[['id', '2023_enplaned_passengers_inter']], 
                                on='id', 
                                how='left'
                            )
                            
                            # Calcular totales por estado
                            df_combined['total_passengers'] = (
                                df_combined['2023_enplaned_passengers_dom'].fillna(0) + 
                                df_combined['2023_enplaned_passengers_inter'].fillna(0)
                            )
                            
                            df_resultado = df_combined.groupby('state')['total_passengers'].sum().reset_index()
                            df_resultado = df_resultado.sort_values('total_passengers', ascending=False).head(5)
                            df_resultado = df_resultado.rename(columns={'state': 'states'})
                            
                            st.dataframe(df_resultado, width='stretch')
                            
                            # Mostrar gráfico de barras
                            st.bar_chart(df_resultado.set_index('states')['total_passengers'])
                            
                            st.success(f"✅ Se encontraron los top 5 estados")
                        else:
                            st.error("❌ No se pudieron cargar todos los datos necesarios")
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
            
            # QUERY 5: Aeropuertos que mejoraron ranking
            elif query_seleccionado == "⬆️ Aeropuertos que Mejoraron su Ranking Total":
                st.info("**Ejecutando:** Aeropuertos que mejoraron su ranking total del 2022 al 2023")
                
                with st.spinner("Analizando mejoras de ranking..."):
                    try:
                        # Obtener datos de total
                        df_total = obtener_datos("total")
                        if not df_total.empty:
                            # Filtrar aeropuertos que mejoraron su ranking
                            df_resultado = df_total[
                                (df_total['2023_rank_total'] < df_total['2022_rank_total']) & 
                                (df_total['2023_rank_total'].notna()) & 
                                (df_total['2022_rank_total'].notna())
                            ]
                            
                            # Seleccionar columnas relevantes y ordenar
                            df_resultado = df_resultado[['airport', '2022_rank_total', '2023_rank_total']]
                            df_resultado = df_resultado.sort_values('2023_rank_total', ascending=True)
                            df_resultado = df_resultado.rename(columns={'airport': 'name'})
                            
                            st.dataframe(df_resultado, width='stretch')
                            st.success(f"✅ {len(df_resultado)} aeropuertos mejoraron su ranking")
                        else:
                            st.error("❌ No se encontraron datos de rankings")
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
    
    # ========== PESTAÑA 2: SQL PERSONALIZADO ==========
    with tab_custom:
        st.warning("🚧 Función en desarrollo - Próximamente")
        st.info("Por ahora usa los queries predefinidos arriba ↑")

# Footer
st.markdown("---")
st.markdown("📊 **✈️ Análisis exploratorio de tráfico aéreo en EE.UU 2022-2023** - Grupo 5 (Computación 2) - Universidad Central de Venezuela")