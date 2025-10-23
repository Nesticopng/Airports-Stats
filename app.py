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

# ========== OPCIÓN 2: CONSULTAS SIMPLIFICADAS ==========
elif menu == "🔍 Consultas SQL":
    st.subheader("🔍 Consultas Predefinidas")
    
    st.write("**Selecciona una consulta predefinida:**")
    
    # Selector de queries predefinidos
    query_seleccionado = st.selectbox(
        "Consultas disponibles:",
        [
            "🏆 Top 18 - Mayor Crecimiento Doméstico 2022-2023",
            "📈 Aeropuertos con Crecimiento >20% Doméstico"
        ]
    )
    
    # Botón para ejecutar el query seleccionado
    if st.button("🚀 Ejecutar Query Seleccionado", type="primary"):
        
        if query_seleccionado == "🏆 Top 18 - Mayor Crecimiento Doméstico 2022-2023":
            st.info("**Ejecutando:** Top 18 aeropuertos con mayor crecimiento porcentual")
            
            with st.spinner("Cargando datos..."):
                try:
                    # Usamos la función obtener_datos que ya funciona
                    df = obtener_datos("domestic")
                    if not df.empty:
                        # Seleccionar solo las columnas que necesitamos y ordenar
                        df_resultado = df[['airport', 'percentage_change_2022_2023_dom']]
                        df_resultado = df_resultado.sort_values('percentage_change_2022_2023_dom', ascending=False).head(18)
                        st.dataframe(df_resultado, width='stretch')
                        st.success(f"✅ Se encontraron {len(df_resultado)} registros")
                    else:
                        st.error("❌ No se encontraron datos")
                except Exception as e:
                    st.error(f"❌ Error: {e}")
        
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

# Footer
st.markdown("---")
st.markdown("📊 **✈️ Análisis exploratorio de tráfico aéreo en EE.UU 2022-2023** - Grupo 5 (Computación 2) - Universidad Central de Venezuela")