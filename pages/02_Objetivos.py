import streamlit as st

# Configurar la página
st.set_page_config(
    page_title="Top Aeropuertos por pasajeros",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título principal
st.title("✈️ Análisis exploratorio de tráfico aéreo en EE.UU 2022-2023")
st.markdown("---")

# Tab 1: Datos Completos
st.subheader("Objetivo General")
st.write("""Estudiar el comportamineto de la cantidad de psajeros nacionales e internacionales en los aeropuertos de estados unidos en los años 2022-2023.
""")
st.markdown("---")


st.subheader("Objetivos específicos")
objetivos = """
- Estudiar el comportamiento de la cantidad de pasajeros nacionales e internacionales en los aeropuertos de Estados Unidos en los años 2022-2023
- Calcular las estadísticas descriptivas del número de pasajeros por aeropuerto en los años 2022-2023
- Analizar la proporción de vuelos nacionales vs internacionales por aeropuerto
- Identificar aeropuertos con mayor y menor cantidad de pasajeros en cada categoría
- Determinar los 10 aeropuertos que tuvieron el mayor porcentaje de crecimiento en los años 2022-2023
- Comparar el ranking de aeropuertos con mayor cantidad de pasajeros entre 2022 y 2023
"""

st.markdown(objetivos)
