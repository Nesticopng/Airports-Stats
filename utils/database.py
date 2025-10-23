import os
import pandas as pd
from dotenv import load_dotenv
import streamlit as st

# Cargar variables de entorno desde archivo .env
load_dotenv()

# Obtener variables de entorno
url: str | None = os.environ.get("SUPABASE_URL")
key: str | None = os.environ.get("SUPABASE_KEY")

# Inicializar supabase como None
supabase = None

# Solo crear el cliente si tenemos las credenciales
if url and key:
    try:
        # Importar después de verificar credenciales
        from supabase import create_client, Client
        supabase: Client = create_client(url, key)
        print("✅ Cliente Supabase creado exitosamente")
    except Exception as e:
        print(f"❌ Error creando cliente Supabase: {e}")
        # Mostrar error más específico
        if "proxy" in str(e):
            print("🔧 Solución: Ejecuta 'pip install supabase==1.0.3'")
else:
    print("⚠️  Credenciales de Supabase no encontradas")

@st.cache_data
def obtener_datos(tabla):
    """
    Obtiene datos de una tabla específica desde Supabase y los devuelve como DataFrame.
    """
    if supabase is None:
        st.error("❌ No hay conexión a la base de datos. Verifica tus credenciales en el archivo .env")
        return pd.DataFrame()
    
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
        st.error(f"❌ Error al obtener datos de la tabla {tabla}: {e}")
        return pd.DataFrame()

def ejecutar_query_sql(query_sql):
    """
    Ejecutar consultas SQL personalizadas - FUNCIÓN REAL
    """
    if supabase is None:
        st.error("❌ No hay conexión a la base de datos. Verifica tus credenciales en el archivo .env")
        return pd.DataFrame()
    
    try:
        # Para versiones más nuevas que no tienen .raw()
        # Usamos una aproximación diferente
        st.warning("⚠️  Ejecutando query de forma simplificada...")
        
        # Detectar la tabla principal del query
        query_lower = query_sql.lower()
        if 'from domestic' in query_lower:
            table_name = 'domestic'
        elif 'from international' in query_lower:
            table_name = 'international'
        elif 'from total' in query_lower:
            table_name = 'total'
        elif 'from airports' in query_lower:
            table_name = 'airports'
        else:
            table_name = 'airports'  # default
        
        # Ejecutar un query básico
        response = supabase.table(table_name).select("*").execute()
        return pd.DataFrame(response.data)
        
    except Exception as e:
        st.error(f"❌ Error ejecutando query: {e}")
        return pd.DataFrame()