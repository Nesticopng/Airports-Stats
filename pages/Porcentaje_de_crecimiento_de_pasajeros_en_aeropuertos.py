import streamlit as st
from utils.database import obtener_datos

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