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
st.subheader("Marco Teórico")
st.markdown("---")

texto_concepto = """
**Aeropuerto**

Podemos definir un **aeropuerto** como todo aquel terreno en el
que podemos encontrar instalaciones y pistas destinadas al despegue, aterrizaje
y tráfico de aeronaves, así como al mantenimiento, carga de combustible de los
mismos, embarque y desembarque de pasajeros, etc.

Cabe decir que un aeropuerto tiene infinidad de diferentes
instalaciones, servicios, edificios en toda su extensión, pero lo podemos
dividir en dos partes:
Lado aire (air-side), que incluyen las pistas, tanto para
despegar como para aterrizar, las calles de rodaje y la zona de estacionamiento
de los aviones.
Lado tierra (land-side), que está dedicado al pasajero, es
decir, incluye el edificio terminal (con las zonas de comercio también), las
aduanas, los estacionamientos de coches, etc.

**Los servicios aeroportuarios** 

son aquellos servicios prestados por los operadores de servicios aeropuertos, el gestor aeroportuario o las empresas colaboradores que
operan en la infraestructura aeroportuaria. Podemos distinguir entre servicios
dirigidos a las aeronaves y servicios dirigidos a los pasajeros, que podríamos
dividir entre servicios aeroportuarios y servicios para el
pasajero/comerciales.

Los servicios aeroportuarios incluyen servicios de:
Rampa (asistencia en tierra a las aeronaves en relación a
embarque, desembarque de carga, pasajeros, mercancía y mensajería), suministro
de combustible, suministro de alimentos (catering), terminales de
almacenamiento de carga, servicios de limpieza de aeronaves, despacho de
aeronaves, mantenimiento en línea, control de operaciones, servicio de
seguridad, etc.

También encontramos otros servicios de asistencia de vital
importancia: control de fauna, servicios de meteorología, asignación de slots,
salvamento y extinción de incendios, etc.

En cuanto a los servicios para el pasajero/comerciales:
Servicios de facturación de vuelos, control de seguridad,
control de pasaportes, zonas de espera con asientos, servicios de asistencia a
personas con movilidad reducida (PMR), indicaciones y señalización adecuadas y
puntos de información, ofertas de restauración, salas VIP, oferta de compras
indispensables (farmacias, accesorios de viaje, etc.).

**Tipos de aeropuertos**

Los tipos de aeropuertos según su actividad principal son
aeropuertos civiles, de aviación general y de carga aérea. Veremos las
características de cada uno:

Aeropuertos civiles: aquellos aeropuertos que destinados a
atender a los pasajeros que utilizan las aeronaves como medio de transporte.

Aeropuertos de aviación general: son todos los aeropuertos
acogen vuelos de aviación general, lo que viene a ser todo vuelo civil que no
sea de aerolíneas regulares ni tipo chárter.

Aeropuertos de carga aérea: son todos los aeropuertos
ubicados en zonas estratégicas dentro del ámbito económico o industrial
destinados a ser el punto de salida o llegada de una carga o mercancía que va a
ser transportada por vía aérea.

**Importancia de los aeropuertos**

Los aeropuertos son esenciales para el desarrollo económico
de cualquier lugar. Mejoran las comunicaciones, conllevan la creación de
puestos de trabajo, generan actividad económica y revalorizan el entorno. La
globalización del mundo actual hace que sea imprescindible para la sociedad
poder usar el transporte aéreo tanto por razones de negocio domo de ocio. Los
aeropuertos ocupan el primer lugar de importancia en las actividades turísticas
y de negocios de cada país.

La globalización del mundo actual hace que sea imprescindible
para la sociedad poder usar el transporte aéreo tanto por razones de negocio
domo de ocio. Los aeropuertos ocupan el primer lugar de importancia en las
actividades turísticas y de negocios de cada país.

**Movimiento de Aeronaves (Aircraft Movements)**

El Movimiento de Aeronaves es un indicador operativo
fundamental que contabiliza el total de veces que una aeronave ha utilizado el
aeródromo (pista).

Distinción: Se distingue entre aterrizajes y despegues. Un
único vuelo que llega y luego parte del aeropuerto genera dos movimientos de
aeronaves (un aterrizaje y un despegue). Es un indicador crucial de la
capacidad y actividad de la infraestructura aeroportuaria, incluso si el
enfoque principal es el tráfico de pasajeros.

**Tráfico de Pasajeros**

El Tráfico de Pasajeros en el contexto aeroportuario se
refiere al movimiento de personas transportadas en aeronaves entre aeropuertos,
que engloba tanto las llegadas como las salidas. Es uno de los principales
indicadores de la actividad aérea y la demanda de transporte.

Pasajeros Nacionales (Domésticos): Son aquellos cuyo viaje
(vuelo) tiene su origen y destino dentro de las fronteras territoriales del
mismo país. Es decir, no implican un cruce de frontera internacional.

Pasajeros Internacionales: Son aquellos cuyo viaje cruza al
menos una frontera de un país a otro. Los aeropuertos internacionales están
equipados y regulados para prestar servicios a aerolíneas y pasajeros de todo
el mundo y servir como centros de conexión para estos vuelos, regidos por
acuerdos internacionales de seguridad y operación.

**IATA**

La IATA, o International Air Transport Association (IATA –
Sitio Oficial), es una organización comercial que agrupa a la mayoría de las
aerolíneas del mundo. Fundada en 1945, la IATA nació con el objetivo de
promover la cooperación entre las compañías aéreas, facilitar el desarrollo de
normativas y procedimientos que garanticen la seguridad, eficiencia y
sostenibilidad del transporte aéreo. Para una visión histórica y de contexto,
puedes consultar también el artículo de Wikipedia: Asociación Internacional de
Transporte Aéreo.

**Breve historia y fundación en 1945**

La historia de la IATA se remonta a la posguerra, un periodo
en el que la necesidad de reconstruir las redes de transporte aéreo era
imperativa. En 1945, representantes de 57 aerolíneas de diferentes países se
reunieron para establecer una organización que pudiera regular y estandarizar
las operaciones aéreas en un contexto global. Entre los objetivos iniciales se
encontraban:

Establecer tarifas y políticas comunes: Con el fin de evitar
la competencia desleal y asegurar una mayor estabilidad en los precios.

Fomentar la cooperación técnica: A través del intercambio de
información y el establecimiento de normas de seguridad.

Facilitar el crecimiento del comercio internacional: Creando
procedimientos unificados que agilizaran el transporte de pasajeros y
mercancías.

Con el paso del tiempo, la IATA amplió su ámbito de acción y
hoy cuenta con más de 290 aerolíneas miembro, representando aproximadamente el
82% del tráfico aéreo mundial.
 
**Membresía actual y alcance global**

Actualmente, la IATA no solo se encarga de coordinar y
unificar estándares en la aviación comercial, sino que también actúa como una
plataforma de colaboración entre gobiernos, reguladores y empresas del sector.
Su alcance global le permite influir en decisiones políticas y en la
implementación de normativas que afectan a toda la industria, promoviendo el
desarrollo de nuevas tecnologías y prácticas que favorecen la seguridad y la
eficiencia en el transporte aéreo.
 
**Objetivos y Funciones de la IATA**

La IATA tiene una serie de objetivos y funciones que la
posicionan como un pilar fundamental en la industria aeronáutica y logística.
Entre sus principales tareas se encuentran:
 
**Promoción de la cooperación entre aerolíneas**

Uno de los pilares de la IATA es la cooperación entre
aerolíneas. A través de foros, reuniones y comités, la organización facilita el
intercambio de información y la coordinación de esfuerzos para resolver
problemas comunes. Esta colaboración permite a las aerolíneas:

Compartir mejores prácticas: Lo que se traduce en una mayor
seguridad y eficiencia operativa.

Optimizar rutas y conexiones: Mejorando la experiencia del
pasajero y la conectividad global.

Negociar tarifas y políticas comunes: Beneficiando tanto a
las aerolíneas como a los consumidores.
Establecimiento de estándares de seguridad y eficiencia
La seguridad es una prioridad indiscutible en la aviación.
La IATA desempeña un papel crucial en el desarrollo y la implementación de
estándares internacionales que aseguran que:
 
Los procedimientos de vuelo sean uniformes: Garantizando que
todas las operaciones cumplan con normas estrictas de seguridad.

Se minimicen los riesgos operativos: A través de la
capacitación continua y la certificación de procesos.

La infraestructura aeroportuaria se mantenga actualizada:
Incorporando tecnologías modernas y protocolos de emergencia.
Estos estándares no solo mejoran la seguridad, sino que
también contribuyen a la eficiencia operativa, permitiendo a las aerolíneas
reducir costos y optimizar recursos.
 
**Desarrollo de normativas medioambientales**

Con la creciente preocupación por el medio ambiente, la IATA
ha incorporado normativas y programas de sostenibilidad en su agenda. La
organización trabaja en iniciativas que buscan:
 
Reducir las emisiones de carbono: Promoviendo prácticas de
vuelo más eficientes y el uso de combustibles alternativos.

Fomentar la innovación tecnológica: En el diseño de
aeronaves y en la gestión del tráfico aéreo.

Promover la responsabilidad social corporativa: Incentivando
a las aerolíneas a adoptar medidas que minimicen su impacto ambiental.
Estas acciones son vitales para garantizar un desarrollo
sostenible del transporte aéreo y para cumplir con los objetivos globales de
protección ambiental.

**Tipología de Aeropuertos en EE. UU. (Clasificación de la FAA)**

La Federal Aviation Administration (FAA) clasifica los
aeropuertos según su función y nivel de actividad, siendo una categorización
clave para la distribución de fondos e infraestructura. Una clasificación
importante es por el volumen de pasajeros, donde los Grandes Hubs (Major Hubs)
son aeropuertos que manejan un volumen significativo de tráfico y sirven como
centros primarios para el transporte aéreo nacional e internacional.

Importancia de los Grandes Hubs: Aeropuertos como
Hartsfield-Jackson Atlanta International Airport (ATL) y Dallas-Fort Worth International
Airport (DFW) son ejemplos de Major Hubs que actúan como puntos focales,
concentrando la actividad de las aerolíneas, y tienen un impacto masivo en el
tráfico al canalizar a millones de pasajeros hacia una vasta red de destinos.

**"Hub" Aeroportuario**

El concepto de Hub aeroportuario se centra en un modelo de
red conocido como Hub-and-Spoke (centro y radio).

Rol en la conectividad: Un Hub es el punto neurálgico donde
se reúnen y se dispersan los vuelos. Las aerolíneas lo utilizan para optimizar
su eficiencia operativa, ya que permite a los pasajeros viajar entre dos
ciudades con poca demanda directa a través de una conexión en el hub, lo que
aumenta la oferta de servicios globales y la conectividad nacional e
internacional sin requerir múltiples rutas punto a punto.

**FAA (Federal Aviation Administration)**

La FAA es la agencia del gobierno de los Estados Unidos
responsable de la regulación de todos los aspectos de la aviación civil.

Su rol incluye la regulación del espacio aéreo (control de
tráfico aéreo), la certificación de aeronaves y pilotos, y el desarrollo y la
supervisión de la infraestructura aeroportuaria (por ejemplo, a través de
directrices como las de ruido en la Parte 150) para garantizar la seguridad y
la eficiencia de la aviación.

**DOT (Department of Transportation) y BTS (Bureau of Transportation Statistics)**

El DOT (Departamento de Transporte) es el departamento
ejecutivo federal encargado de la política de transporte de la nación, y el BTS
(Oficina de Estadísticas de Transporte) es una agencia de estadísticas dentro
del DOT.

**ACI (Airports Council International)**

El ACI es el organismo comercial mundial de los aeropuertos
del mundo.

Es la fuente de informes y clasificaciones a nivel mundial,
incluyendo rankings anuales por volumen de tráfico de pasajeros (total,
internacional), carga y movimientos de aeronaves. Estos informes son cruciales
para el análisis de la industria global y clasifican a los principales
aeropuertos de EE. UU. dentro del contexto internacional.
"""

st.markdown(texto_concepto, unsafe_allow_html=False)

