import os
import pandas as pd
from dotenv import load_dotenv
from supabase import create_client, Client
import streamlit as st

# Cargar variables de entorno desde archivo .env
load_dotenv()

# Obtener variables de entorno con valores por defecto
url: str | None = os.environ.get("SUPABASE_URL")
key: str | None = os.environ.get("SUPABASE_KEY")

if url is None or key is None:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables or .env file")

supabase: Client = create_client(url, key)

@st.cache_data
def obtener_datos(tabla):
    """
    Obtiene datos de una tabla específica desde Supabase y los devuelve como DataFrame.
    Para tablas 'domestic', 'international' y 'total':
    - Hace JOIN automático con la tabla 'airports' para obtener nombres de aeropuertos
    - Reemplaza 'airport_id' con 'airport_name' (nombre completo del aeropuerto)
    
    Automáticamente:
    - Reordena las columnas: 'id' primero, 'airport_name' segundo, 'airport_id' tercero (si existen)
    - Ordena las filas por rankings de 2023 (domestic, international, total) o por 'id' (otras tablas)
    
    Args:
        tabla (str): Nombre de la tabla a consultar
        
    Returns:
        pd.DataFrame: DataFrame con JOIN realizado y columnas reordenadas
    """
    try:
        # Para tablas que tienen airport_id, hacer JOIN con airports
        if tabla in ['domestic', 'international', 'total']:
            query = "*, airports(airport)"
        elif tabla == 'airports':
            query = "*, city(name), state(name)"
        else:
            query = "*"
        
        response = supabase.table(tabla).select(query).execute()

        if response.data:
            df = pd.DataFrame(response.data)
            
            # Si es una tabla con airport_id, expandir el campo airports
            if tabla in ['domestic', 'international', 'total']:
                # Expandir la columna airports para obtener el campo airport
                df['airport'] = df['airports'].apply(lambda x: x['airport'] if x else None)
                # Eliminar la columna airports original
                df = df.drop('airports', axis=1)
            
            if tabla == 'airports':
                df['city'] = df['city'].apply(lambda x: x['name'] if x else None)
                df['state'] = df['state'].apply(lambda x: x['name'] if x else None)
    
            # Reordenar columnas para que 'id' aparezca primero y 'airport_name' en segunda posición
            columnas_ordenadas = ['id']
                
            # Si existe 'airport_name', agregarlo en segunda posición
            if tabla == 'total' or tabla == 'domestic' or tabla == 'international' or tabla == 'airports':
                columnas_ordenadas.append('airport')

            # Agregar columnas de rankings en posición específica
            if tabla == 'total':
                if '2023_rank_total' in df.columns:
                    columnas_ordenadas.append('2023_rank_total')
                if '2022_rank_total' in df.columns:
                    columnas_ordenadas.append('2022_rank_total')

            # Agregar el resto de columnas (excluyendo las ya agregadas)
            columnas_ya_agregadas = ['id', 'airport', 'airport_id', '2023_rank_total', '2022_rank_total', 'city_id', 'state_id']
            columnas_ordenadas.extend([col for col in df.columns if col not in columnas_ya_agregadas])
            
            # Reordenar DataFrame con las columnas en el orden deseado
            df = df[columnas_ordenadas]
            
            # Ordenar por rankings de 2023
            if tabla == 'domestic':
                df = df.sort_values('2023_rank_dom').reset_index(drop=True)
            
            if tabla == 'international':
                df = df.sort_values('2023_rank_inter').reset_index(drop=True)
            
            if tabla == 'total':
                df = df.sort_values('2023_rank_total').reset_index(drop=True)
            
            return df
        else:
            return pd.DataFrame()
    except Exception as e:
        print(f"Error al obtener datos de la tabla {tabla}: {e}")
        return pd.DataFrame()

# ========== AQUÍ AGREGA LA NUEVA FUNCIÓN ==========
def ejecutar_query_sql(query_sql):
    """
    Ejecutar consultas SQL personalizadas - FUNCIÓN REAL
    Esta función ejecuta los queries SQL directamente en tu base de datos
    y devuelve los resultados REALES, no datos de ejemplo.
    
    Args:
        query_sql (str): Consulta SQL a ejecutar
        
    Returns:
        pd.DataFrame: DataFrame con los resultados REALES de la base de datos
    """
    try:
        # Esto ejecuta el query REAL en tu base de datos
        response = supabase.raw(query_sql).execute()
        return pd.DataFrame(response.data)
    except Exception as e:
        print(f"Error ejecutando query: {e}")
        raise Exception(f"Error en la consulta SQL: {str(e)}")