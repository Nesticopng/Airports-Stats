# ✈️ Análisis Exploratorio de Tráfico Aéreo en EE.UU. 2022-2023

## 📋 Descripción del Proyecto

Este proyecto presenta un análisis estadístico comprehensivo del comportamiento del tráfico aéreo en los Estados Unidos durante los años 2022-2023, un período crucial de recuperación post-pandémica. El estudio se enfoca en el análisis de la cantidad de pasajeros nacionales e internacionales en los aeropuertos estadounidenses, proporcionando insights valiosos sobre la evolución del sector aeroportuario tras los profundos trastornos generados por la pandemia de COVID-19.

### 🎯 Objetivo General

Estudiar el comportamiento de la cantidad de pasajeros nacionales e internacionales en los aeropuertos de Estados Unidos en los años 2022-2023, proporcionando un análisis estadístico descriptivo y sistemático que compare el comportamiento de estos flujos por aeropuerto.

### 🎯 Objetivos Específicos

- **Análisis Estadístico Descriptivo**: Calcular las estadísticas descriptivas del número de pasajeros por aeropuerto en los años 2022-2023
- **Análisis de Proporciones**: Analizar la proporción de vuelos nacionales vs internacionales por aeropuerto
- **Identificación de Patrones**: Identificar aeropuertos con mayor y menor cantidad de pasajeros en cada categoría
- **Análisis de Crecimiento**: Determinar los 10 aeropuertos que tuvieron el mayor porcentaje de crecimiento en los años 2022-2023
- **Comparación Temporal**: Comparar el ranking de aeropuertos con mayor cantidad de pasajeros entre 2022 y 2023

## 🔍 Marco Teórico

### Conceptos Clave

**Aeropuerto**: Terreno con instalaciones y pistas destinadas al despegue, aterrizaje y tráfico de aeronaves, incluyendo servicios de mantenimiento, carga de combustible, embarque y desembarque de pasajeros.

**Tipos de Aeropuertos**:
- **Aeropuertos Civiles**: Destinados a atender pasajeros que utilizan aeronaves como medio de transporte
- **Aeropuertos de Aviación General**: Acogen vuelos civiles no regulares ni chárter
- **Aeropuertos de Carga Aérea**: Ubicados en zonas estratégicas para transporte de mercancías

**Clasificación de Pasajeros**:
- **Pasajeros Nacionales (Domésticos)**: Viajes con origen y destino dentro de las fronteras territoriales del mismo país
- **Pasajeros Internacionales**: Viajes que cruzan al menos una frontera internacional

### Organizaciones Reguladoras

- **IATA (International Air Transport Association)**: Organización comercial que agrupa a la mayoría de aerolíneas del mundo, estableciendo estándares de seguridad y eficiencia
- **FAA (Federal Aviation Administration)**: Agencia gubernamental estadounidense responsable de la regulación de la aviación civil
- **ACI (Airports Council International)**: Organismo comercial mundial de aeropuertos, fuente de informes y clasificaciones globales

## 📊 Funcionalidades del Sistema

### 1. **Estadísticas Descriptivas Avanzadas**
- Análisis estadístico completo con métricas de tendencia central, dispersión y forma
- Visualizaciones interactivas incluyendo histogramas, box plots, Q-Q plots y análisis de curtosis
- Dashboard moderno con métricas en cards personalizados
- Comparación entre años 2022 y 2023

### 2. **Análisis de Proporciones de Vuelos**
- Análisis detallado de la distribución de vuelos domésticos vs internacionales
- Visualizaciones en tablas interactivas, gráficos de barras y gráficos de pie
- Métricas globales de porcentaje de vuelos por tipo
- Filtros por año y configuración personalizable

### 3. **Análisis de Crecimiento**
- Identificación de aeropuertos con mayor crecimiento porcentual
- Comparativas entre años con métricas de cambio
- Rankings dinámicos por diferentes criterios

### 4. **Top Aeropuertos**
- Rankings de aeropuertos por volumen de pasajeros
- Análisis comparativo entre años
- Visualizaciones de tendencias y patrones

### 5. **Consultas SQL Personalizadas**
- Interfaz para consultas SQL directas a la base de datos
- Exploración interactiva de datos
- Visualización de resultados en tiempo real

## 🛠️ Aspectos Técnicos

### Tecnologías Utilizadas

- **Frontend**: Streamlit - Framework de Python para aplicaciones web interactivas
- **Base de Datos**: Supabase - Plataforma de base de datos en la nube
- **Análisis de Datos**: Pandas, NumPy, SciPy
- **Visualizaciones**: Plotly - Librería para gráficos interactivos
- **Gestión de Variables**: python-dotenv
- **Procesamiento**: Matplotlib, Pillow

### Instalación y Configuración

> **💡 Opción Rápida**: Si solo quieres explorar el proyecto, puedes usar la [demo en vivo](https://airport-stats.streamlit.app/) sin necesidad de instalación.

#### Prerrequisitos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

#### Pasos de Instalación

1. **Clonar el repositorio**:
```bash
git clone https://github.com/Nesticopng/Airports-Stats.git
cd Airports-Stats
```

2. **Crear entorno virtual** (recomendado):
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias**:
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**:
Crear un archivo `.env` en la raíz del proyecto con:
```env
SUPABASE_URL=tu_url_de_supabase
SUPABASE_KEY=tu_clave_de_supabase
```

5. **Ejecutar la aplicación**:
```bash
streamlit run app.py
```

### Estructura del Proyecto

```
Airports-Stats/
├── app.py                          # Aplicación principal de Streamlit
├── requirements.txt                 # Dependencias del proyecto
├── .env                           # Variables de entorno (crear manualmente)
├── utils/
│   └── database.py                # Módulo de conexión a base de datos
└── pages/
    ├── 01_Introducción.py         # Página de introducción
    ├── 02_Objetivos.py            # Objetivos del proyecto
    ├── 03_Planteamiento_del_problema.py  # Planteamiento del problema
    ├── 04_Marco_Teórico.py        # Marco teórico
    ├── 05_Bases_legales.py        # Bases legales
    ├── 6_Estadísticas_descriptivas.py  # Análisis estadístico
    ├── 7_Proporción_de_Vuelos.py  # Análisis de proporciones
    ├── 08_Porcentaje_de_crecimiento...  # Análisis de crecimiento
    ├── 09_Top_Aeropuertos...      # Rankings de aeropuertos
    ├── 10_Comparativa_aeropuertos...  # Comparativas entre años
    ├── 11_Conclusion.py           # Conclusiones
    └── Querys.py                  # Consultas SQL personalizadas
```

### Dependencias Principales

```txt
supabase>=2.22.0          # Cliente de Supabase
python-dotenv>=0.19.0     # Gestión de variables de entorno
streamlit>=1.50.0         # Framework web
pandas>=2.3.0             # Manipulación de datos
numpy>=2.3.0              # Computación numérica
plotly>=6.3.1             # Visualizaciones interactivas
scipy>=1.16.2             # Análisis estadístico avanzado
matplotlib>=3.10.0        # Visualizaciones adicionales
```

## 🚀 Uso del Sistema

### Navegación Principal
El sistema está organizado en páginas temáticas accesibles desde la barra lateral de Streamlit:

1. **Introducción**: Contexto y objetivos del proyecto
2. **Objetivos**: Metas específicas del análisis
3. **Planteamiento del Problema**: Justificación y problemática
4. **Marco Teórico**: Fundamentos conceptuales
5. **Bases Legales**: Marco regulatorio
6. **Estadísticas Descriptivas**: Análisis estadístico avanzado
7. **Proporción de Vuelos**: Análisis de distribución de vuelos
8. **Análisis de Crecimiento**: Identificación de tendencias
9. **Top Aeropuertos**: Rankings y comparativas
10. **Comparativas**: Análisis comparativo entre años
11. **Conclusiones**: Hallazgos y resultados
12. **Consultas SQL**: Exploración personalizada de datos

### Características Interactivas

- **Filtros Dinámicos**: Selección de años, tipos de flujo, y parámetros de análisis
- **Visualizaciones Interactivas**: Gráficos que responden a interacciones del usuario
- **Dashboards Modernos**: Interfaces con diseño profesional y métricas visuales
- **Exportación de Datos**: Capacidad de descargar resultados y visualizaciones

## 📈 Resultados y Aplicaciones

Este sistema proporciona insights valiosos para:

- **Planificación Aeroportuaria**: Optimización de recursos y capacidad
- **Análisis de Mercado**: Identificación de tendencias y oportunidades
- **Toma de Decisiones**: Base empírica para políticas y estrategias
- **Investigación Académica**: Datos para estudios sobre transporte aéreo
- **Monitoreo de Recuperación**: Seguimiento del impacto post-pandémico

## 👥 Equipo de Desarrollo

Este proyecto fue desarrollado por:

- **Néstor Alirio**
- **Eros Bande**
- **Nathalia Bognanno**
- **Angel Velasquez**
- **Simon Lira**

## 📄 Licencia

Este proyecto está desarrollado con fines académicos y de investigación. 
---
## 🌐 Demo en Vivo

**🚀 [Ver Proyecto Desplegado](https://airport-stats.streamlit.app/)**

Puedes explorar todas las funcionalidades del sistema directamente en tu navegador sin necesidad de instalación.

---
*Desarrollado con ❤️*