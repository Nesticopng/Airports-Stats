import streamlit as st
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

# Footer
st.markdown("---")
st.markdown("📊 **✈️ Análisis exploratorio de tráfico aéreo en EE.UU 2022-2023** - Grupo 5 (Computación 2) - Universidad Central de Venezuela")