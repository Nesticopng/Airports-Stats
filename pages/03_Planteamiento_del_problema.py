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
st.subheader("Planteamiento del problema")
st.write("""Los aeropuertos constituyen una red de flujo de personas constante ya sea que provengan de el extranjero a viajes a nivel nacional, esta red de transporte masivo ayuda a las personas de todos los países a trasladarse de manera más rápida y recorrer distancias muy largas, cada país tiene su red de aeropuertos que manejan y estructuran todos esos viajes para la población, siendo uno de los medios de transportes más eficientes .
""")
st.write("""En el año 2020 se declaro una pandemia mundial del virus covid-19 lo cual hizo que el flujo de personas en todo el mundo bajara drásticamente, los aeropuertos tuvieran una baja masiva de pasajeros debido a las medidas sanitarias de cada país en donde para ese mismo año muchos países cerraron completamente las aduanas reduciendo drásticamente el flujo de personas a nivel nacional e internacional.
""")
st.write("""Para los periodos 2022-2023 aunque todavía existían medidas sanitarias los vuelos y transporte esta nuevamente activándose y volviendo a prestar los servicios como era antes de la pandemia.
""")
st.write("""El sistema aeroportuario de los Estados Unidos de América constituye la red de transporte aéreo más grande y compleja del mundo, siendo un motor crucial de su economía y un reflejo directo de las dinámicas sociales, políticas y económicas globales. El volumen y el tipo de tráfico de pasajeros no solo determinan la planificación operativa y de infraestructura, sino que también actúan como indicadores sensibles de la salud económica y la política exterior del país. Tras periodos de gran incertidumbre global como la pandemia del covid-19, el comportamiento de los flujos de pasajeros se ha vuelto especialmente errático, haciendo obsoletos muchos modelos de predicción preexistentes. Esta situación exige un análisis riguroso para la toma de decisiones estratégicas.
""")
st.write("""La situación problemática se centra en la marcada incertidumbre generada por el período posterior a la pandemia de COVID-19. Si bien el tráfico aéreo experimentó una recuperación significativa a partir de 2022, el comportamiento de los flujos de pasajeros no necesariamente ha retomado los patrones históricos previos, además de que para esas fechas todavía se seguían manteniendo bastantes medidas de sanidad respecto a la misma pandemia.
""")
st.write("""En el año 2023 las medidas de seguridad fueron bajando y el flujo de personas en todas partes del mundo fue volviendo a los números antes de la pandemia, este periodo constituye una un periodo de reincorporación a las antiguas medidas previas a la pandemia, lo cual genera preguntas respecto a como fue variando el volumen de personas en los aeropuertos  en una época de cambios en el país con la red de transporte aéreo mas y compleja del mundo, en la cual hay un flujo de personas masivo de forma constante.
""")
st.markdown("---")

