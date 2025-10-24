import streamlit as st
from utils.database import obtener_datos

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
st.subheader("Bases legales")
st.write("""Para la fundamentacion legal del proyecto se citaran leyes pertenecientes al Los Estados Unidos como soporte a la investigacion.
""")
st.markdown("---")

st.markdown("**Estatuto Legal (U.S. Code - U.S.C.**)")
st.write("""Dicho codigo en el titulo 49 en el 49 U.S.C. § 41708 se habla que se le otorga al sercretario de estado la la autoridad para exigir a los transportistas aéreos (aerolíneas) que presenten informes y mantengan registros relacionados con su servicio
adicional mente el el 49 U.S.C. § 41709 el mismo secretario de estado tiene la misma autoridad para divulgar dichos reportes hechos por las aerolineas.
""")

st.markdown("**Base Regulatoria (Code of Federal Regulations - CFR**)")
st.write("""Dentro del codigo federal tambien se hace referencia a los reportes que deben realizar los grandes transportistas aéreos certificados,
en el 14 CFR Parte 241 Esta sección del CFR establece los requisitos para que las aerolíneas presenten los informes financieros y de operaciones, incluyendo los famosos Formularios 41 que contienen las estadísticas de embarque y desembarque de pasajeros internacionales los cuales se analizan en el presente proyecto.
""")

st.write(""" En resumen el respaldo legal que cubre al proyecto,reside en el Título 49 del Código de los Estados Unidos (49 U.S.C.), específicamente en la sección § 41708, que otorga al Secretario de Transporte la autoridad para exigir informes y registros a los transportistas aéreos. El mecanismo de reporte detallado se establece en el Título 14 del Código de Regulaciones Federales (14 CFR), Parte 241, que define el Sistema Uniforme de Cuentas e Informes que utilizan las aerolíneas para reportar sus estadísticas de tráfico (incluyendo los datos de pasajeros internacionales).
""")