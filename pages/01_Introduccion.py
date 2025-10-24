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
st.subheader("Introducción")
st.write("""El transporte aéreo es, indiscutiblemente, un pilar neurálgico para la economía global y, particularmente, para la infraestructura de los Estados Unidos. Los aeropuertos de la nación no son meros puntos de tránsito, sino complejos centros de actividad económica y conectividad que sustentan el comercio, el turismo y las relaciones internacionales. En este sentido, la gestión, planificación y expansión de la capacidad aeroportuaria dependen directamente de un conocimiento granular y preciso de las dinámicas de flujo de pasajeros. Sin este conocimiento, las inversiones en infraestructura y las decisiones operativas se basan en conjeturas, introduciendo una incertidumbre significativa en un sector de altísimo costo y vital importancia estratégica.
""")
st.write("""El período comprendido entre los años 2022 y 2023 reviste una importancia histórica y económica singular. Tras los profundos trastornos generados por la pandemia global, estos años marcan una fase crucial de recuperación y reajuste en la movilidad aérea. El comportamiento del tráfico durante este lapso no solo refleja la resiliencia del sector, sino también la efectividad de las políticas de reapertura y los cambios en los hábitos de viaje. Sin embargo, no todos los segmentos de pasajeros se han recuperado o evolucionado de manera uniforme.
""")
st.write("""Este estudio se centra en una distinción fundamental para la planificación: el comportamiento de la cantidad de pasajeros nacionales y la cantidad de pasajeros internacionales en los Estados Unidos. Esta distinción es esencial, ya que cada flujo está determinado por factores macroeconómicos y regulatorios diferentes. El flujo nacional es un barómetro de la economía doméstica y la confianza del consumidor interno, mientras que el flujo internacional es sensible a políticas de visado, geopolítica y tasas de cambio. Comprender las diferencias en la estacionalidad, el crecimiento y la contribución relativa de estos dos segmentos es imperativo para optimizar recursos como el personal de seguridad, cuyo dimensionamiento es vitalmente distinto para cada tipo de vuelo.
""")
st.write("""El propósito de este trabajo es llenar la brecha de un análisis estadístico descriptivo y sistemático que compare el comportamiento de estos flujos por aeropuerto. En lugar de ofrecer datos agregados que ocultan las realidades operacionales individuales, esta investigación se enfoca en la identificación precisa de los patrones a nivel de terminal..
""")
st.write("""Mediante este enfoque riguroso, el estudio busca no solo describir la realidad de los años 2022-2023, sino también proporcionar una base empírica sólida para la toma de decisiones, reduciendo la incertidumbre y sentando las bases para proyecciones futuras más precisas en la compleja y dinámica industria aérea de los Estados Unidos.
""")

st.markdown("---")

