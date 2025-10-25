import streamlit as st
import pandas as pd
from utils.database import supabase

# Configurar la página
st.set_page_config(
    page_title="Consultas SQL - Aeropuertos",
    page_icon="🔍",
    layout="wide"
)

# Título de la página
st.title("🔍 Querys SQL")
st.markdown("---")

# ========== QUERIES PREDEFINIDOS ==========
# Selector de queries predefinidos
query_seleccionado = st.selectbox(
        "**Selecciona una consulta:**",
        [
            "🏆 Top 10 - Mayor Crecimiento Doméstico 2022-2023",
            "📈 Aeropuertos con Crecimiento mayor a 20% Doméstico", 
            "🌎 Proporción de Pasajeros Internacionales",
            "🗺️ Top 5 Estados con Más Pasajeros Totales",
            "⬆️ Aeropuertos que Mejoraron su Ranking Total"
        ]
    )
    
    # QUERY 1: Top 10 crecimiento doméstico
if query_seleccionado == "🏆 Top 10 - Mayor Crecimiento Doméstico 2022-2023":
    st.subheader("**Top 10 aeropuertos con mayor aumento en pasajeros domésticos entre 2022 y 2023**")

    tab2, tab1 = st.tabs(["🔢 Incremento Absoluto de Pasajeros", "📈 Porcentaje de Crecimiento"])

    # ===== TAB 1: PORCENTAJE =====
    with tab1:
        st.subheader("**Top 10 aeropuertos con mayor incremento porcentual de pasajeros domésticos (2023 vs 2022)**")

        with st.expander("🔍 Ver Query SQL", expanded=True):
            st.code("""
SELECT 
    a.name,
    d."2022_enplaned_passengers_dom" as 2022_passengers,
    d."2023_enplaned_passengers_dom" as 2023_passengers,
    d.percentage_change_2022_2023_dom as percentage_change
FROM domestic as d
INNER JOIN airports as a ON d.airport_id = a.id
ORDER BY percentage_change_2022_2023_dom DESC
LIMIT 10;
            """, language='sql')
        
        if st.button("🚀 Ejecutar Query (Porcentaje)", key="query1_percentage"):
            with st.spinner("Ejecutando consulta a Supabase..."):
                try:
                    response = supabase.table('domestic').select("*, airports(name)").execute()
                    if response.data:
                        df = pd.DataFrame(response.data)
                        df['airport_name'] = df['airports'].apply(lambda x: x['name'] if x else None)
                        df_resultado = df[['airport_name', '2022_enplaned_passengers_dom', '2023_enplaned_passengers_dom', 'percentage_change_2022_2023_dom']].copy()
                        df_resultado = df_resultado.rename(columns={
                            'airport_name': 'name',
                            '2022_enplaned_passengers_dom': '2022_passengers',
                            '2023_enplaned_passengers_dom': '2023_passengers',
                            'percentage_change_2022_2023_dom': 'percentage_change'
                        })
                        df_resultado = df_resultado.sort_values('percentage_change', ascending=False).head(10).reset_index(drop=True)

                        st.success(f"✅ Consulta ejecutada exitosamente. {len(df_resultado)} registros encontrados.")
                        st.dataframe(df_resultado, width='stretch')

                        csv_real = df_resultado.to_csv(index=False)
                        st.download_button(
                            label="📥 Descargar Resultados (Porcentaje)",
                            data=csv_real,
                            file_name="top_10_porcentaje_crecimiento_domestico_real.csv",
                            mime="text/csv"
                        )
                    else:
                        st.warning("⚠️ No se encontraron datos para esta consulta")
                except Exception as e:
                    st.error(f"❌ Error al ejecutar consulta: {str(e)}")
                    st.info("💡 **Nota:** Asegúrate de que las tablas 'domestic' y 'airports' existan en Supabase")

    # ===== TAB 2: INCREMENTO ABSOLUTO =====
    with tab2:
        st.subheader("**Top 10 aeropuertos con mayor incremento absoluto de pasajeros domésticos (2023 vs 2022)**")

        with st.expander("🔍 Ver Query SQL", expanded=True):
            st.code("""
SELECT 
    a.name,
    d."2022_enplaned_passengers_dom" as "2022_passengers",
    d."2023_enplaned_passengers_dom" as "2023_passengers",
    (d."2023_enplaned_passengers_dom" - d."2022_enplaned_passengers_dom") as increase
FROM domestic as d
INNER JOIN airports as a ON d.airport_id = a.id
ORDER BY increase DESC
LIMIT 10;
            """, language='sql')

        if st.button("🚀 Ejecutar Query (Incremento Absoluto)", key="query1_absolute"):
            with st.spinner("Ejecutando consulta a Supabase..."):
                try:
                    response = supabase.table('domestic').select("*, airports(name)").execute()
                    if response.data:
                        df = pd.DataFrame(response.data)
                        df['airport_name'] = df['airports'].apply(lambda x: x['name'] if x else None)

                        # Calcular el incremento absoluto
                        df['increase'] = df['2023_enplaned_passengers_dom'] - df['2022_enplaned_passengers_dom']

                        df_resultado = df[['airport_name', '2022_enplaned_passengers_dom', '2023_enplaned_passengers_dom', 'increase']].copy()
                        df_resultado = df_resultado.rename(columns={
                            'airport_name': 'name',
                            '2022_enplaned_passengers_dom': '2022_passengers',
                            '2023_enplaned_passengers_dom': '2023_passengers'
                        })
                        df_resultado = df_resultado.sort_values('increase', ascending=False).head(10).reset_index(drop=True)

                        st.success(f"✅ Consulta ejecutada exitosamente. {len(df_resultado)} registros encontrados.")
                        st.dataframe(df_resultado, width='stretch')

                        csv_real = df_resultado.to_csv(index=False)
                        st.download_button(
                            label="📥 Descargar Resultados (Incremento Absoluto)",
                            data=csv_real,
                            file_name="top_10_incremento_absoluto_domestico_real.csv",
                            mime="text/csv"
                        )
                    else:
                        st.warning("⚠️ No se encontraron datos para esta consulta")
                except Exception as e:
                    st.error(f"❌ Error al ejecutar consulta: {str(e)}")
                    st.info("💡 **Nota:** Asegúrate de que las tablas 'domestic' y 'airports' existan en Supabase")
# QUERY 2: Crecimiento >20% doméstico
elif query_seleccionado == "📈 Aeropuertos con Crecimiento mayor a 20% Doméstico":
    st.subheader("**Aeropuertos donde el tráfico doméstico creció más de un 20% en 2023 respecto a 2022**")
    
    with st.expander("🔍 Ver Query SQL", expanded=True):
        st.code("""
SELECT 
    a.name,
    d."2022_enplaned_passengers_dom" as 2022_passengers,
    d."2023_enplaned_passengers_dom" as 2023_passengers,
    d.percentage_change_2022_2023_dom
FROM domestic as d
INNER JOIN airports as a ON d.airport_id = a.id
WHERE percentage_change_2022_2023_dom > 20
ORDER BY percentage_change_2022_2023_dom DESC;
        """, language='sql')

    if st.button("🚀 Ejecutar Query", key="query2"):
        with st.spinner("Ejecutando consulta a Supabase..."):
            try:
                # Obtener datos de domestic con JOIN a airports
                response = supabase.table('domestic').select("*, airports(name)").execute()
                
                if response.data:
                    df = pd.DataFrame(response.data)
                    
                    # Expandir la columna airports para obtener el campo name
                    df['airport_name'] = df['airports'].apply(lambda x: x['name'] if x else None)
                    
                    # Filtrar por crecimiento > 20% (más de 20%, no >= 20%)
                    df_filtrado = df[df['percentage_change_2022_2023_dom'] > 20]
                    
                    if len(df_filtrado) > 0:
                        # Si PF existen aeropuertos con crecimiento > 20%
                        df_resultado = df_filtrado[['airport_name', '2022_enplaned_passengers_dom', '2023_enplaned_passengers_dom', 'percentage_change_2022_2023_dom']].copy()
                        df_resultado = df_resultado.rename(columns={
                            'airport_name': 'name',
                            '2022_enplaned_passengers_dom': '2022_passengers',
                            '2023_enplaned_passengers_dom': '2023_passengers'
                        })
                        df_resultado = df_resultado.sort_values('percentage_change_2022_2023_dom', ascending=False)
                        df_resultado = df_resultado.reset_index(drop=True)
                        
                        st.success(f"✅ Consulta ejecutada exitosamente. {len(df_resultado)} registros encontrados.")
                        st.dataframe(df_resultado, width='stretch')
                        
                        # Botón para descargar resultados reales
                        csv_real = df_resultado.to_csv(index=False)
                        st.download_button(
                            label="📥 Descargar Resultados Reales",
                            data=csv_real,
                            file_name="crecimiento_mayor_20_porciento_real.csv",
                            mime="text/csv"
                        )                            
                        
                    else:
                        st.warning("⚠️ No se encontraron datos para esta consulta")
                else:
                    st.warning("⚠️ No se encontraron datos para esta consulta")
                    
            except Exception as e:
                st.error(f"❌ Error al ejecutar consulta: {str(e)}")
                st.info("💡 **Nota:** Asegúrate de que las tablas 'domestic' y 'airports' existan en Supabase")
    
# QUERY 3: Participación internacional
elif query_seleccionado == "🌎 Proporción de Pasajeros Internacionales":
    st.subheader("**Proporción de Pasajeros Internacionales**")
    
    with st.expander("🔍 Ver Query SQL", expanded=True):
        st.code("""
WITH total AS (
    SELECT sum("2023_enplaned_passengers_inter") as total_passengers
    FROM international
)
SELECT
    COALESCE(a.name, 'TOTAL') as airport_name,
    ROUND(sum(i."2023_enplaned_passengers_inter") / (SELECT total_passengers FROM total), 3) AS proportion
FROM international as i
INNER JOIN airports as a ON a.id = i.airport_id
GROUP BY ROLLUP(a.name)
ORDER BY CASE WHEN a.name IS NULL THEN 1 ELSE 0 END, proportion DESC;
        """, language='sql')

    if st.button("🚀 Ejecutar Query", key="query3"):
        with st.spinner("Ejecutando consulta a Supabase..."):
            try:
                # Obtener datos de international con JOIN a airports
                response = supabase.table('international').select("*, airports(name)").execute()
                
                if response.data:
                    df = pd.DataFrame(response.data)
                    
                    # Expandir la columna airports para obtener el campo name
                    df['airport_name'] = df['airports'].apply(lambda x: x['name'] if x else None)
                    
                    # Calcular total de pasajeros internacionales
                    total_passengers = df['2023_enplaned_passengers_inter'].sum()
                    
                    # Calcular proporción por aeropuerto
                    df['proportion'] = (df['2023_enplaned_passengers_inter'] / total_passengers).round(3)
                    
                    # Seleccionar columnas necesarias y ordenar
                    df_resultado = df[['airport_name', 'proportion']].copy()
                    df_resultado = df_resultado.rename(columns={'airport_name': 'airport_name'})
                    df_resultado = df_resultado.sort_values('proportion', ascending=False)
                    
                    # Agregar fila de total
                    total_row = pd.DataFrame({
                        'airport_name': ['TOTAL'],
                        'proportion': [1.000]
                    })
                    df_resultado = pd.concat([df_resultado, total_row], ignore_index=True)
                    df_resultado = df_resultado.reset_index(drop=True)
                    
                    st.success(f"✅ Consulta ejecutada exitosamente. {len(df_resultado)} registros encontrados.")
                    st.dataframe(df_resultado, width='stretch')
                    
                    # Botón para descargar resultados reales
                    csv_real = df_resultado.to_csv(index=False)
                    st.download_button(
                        label="📥 Descargar Resultados Reales",
                        data=csv_real,
                        file_name="participacion_internacional_real.csv",
                        mime="text/csv"
                    )
                else:
                    st.warning("⚠️ No se encontraron datos para esta consulta")
                    
            except Exception as e:
                st.error(f"❌ Error al ejecutar consulta: {str(e)}")
                st.info("💡 **Nota:** Asegúrate de que las tablas 'international' y 'airports' existan en Supabase")
            

# QUERY 4: Top 5 estados
elif query_seleccionado == "🗺️ Top 5 Estados con Más Pasajeros Totales":
    st.subheader("**Top 5 estados con mayor número total de pasajeros**")

    with st.expander("🔍 Ver Query SQL", expanded=True):
        st.code("""
WITH total AS (
    SELECT
        sum(i."2023_enplaned_passengers_inter" + d."2023_enplaned_passengers_dom") as total_passengers,
        s.name as states
    FROM international as i
    INNER JOIN domestic as d on d.airport_id = i.airport_id
    INNER JOIN airports as a on a.id = i.airport_id
    INNER JOIN state as s on s.id = a.state_id
    GROUP BY s.name
)
SELECT
    DISTINCT states,
    total_passengers
FROM total
ORDER BY total_passengers DESC
LIMIT 5;
        """, language='sql')
    
    
    if st.button("🚀 Ejecutar Query", key="query4"):
        with st.spinner("Ejecutando consulta a Supabase..."):
            try:
                # Obtener datos de airports con JOIN a state
                response = supabase.table('airports').select("*, state(name)").execute()
                
                if response.data:
                    df_airports = pd.DataFrame(response.data)
                    
                    # Expandir la columna state para obtener el campo name
                    df_airports['state_name'] = df_airports['state'].apply(lambda x: x['name'] if x else None)
                    
                    # Obtener datos de domestic e international
                    response_dom = supabase.table('domestic').select("*").execute()
                    response_int = supabase.table('international').select("*").execute()
                    
                    if response_dom.data and response_int.data:
                        df_domestic = pd.DataFrame(response_dom.data)
                        df_international = pd.DataFrame(response_int.data)
                        
                        # Combinar datos de domestic e international
                        df_combined = df_domestic.merge(df_international, on='airport_id', suffixes=('_dom', '_inter'))
                        
                        # Combinar con airports para obtener state_name
                        df_final = df_combined.merge(df_airports[['id', 'state_name']], left_on='airport_id', right_on='id')
                        
                        # Calcular total de pasajeros por estado
                        df_final['total_passengers'] = df_final['2023_enplaned_passengers_dom'] + df_final['2023_enplaned_passengers_inter']
                        
                        # Agrupar por estado y sumar pasajeros
                        df_resultado = df_final.groupby('state_name')['total_passengers'].sum().reset_index()
                        df_resultado = df_resultado.rename(columns={'state_name': 'states'})
                        df_resultado = df_resultado.sort_values('total_passengers', ascending=False).head(5)
                        df_resultado = df_resultado.reset_index(drop=True)
                        
                        st.success(f"✅ Consulta ejecutada exitosamente. {len(df_resultado)} registros encontrados.")
                        st.dataframe(df_resultado, width='stretch')
                        
                        # Gráfico de barras con datos reales
                        if not df_resultado.empty:
                            st.bar_chart(df_resultado.set_index('states')['total_passengers'])
                        
                        # Botón para descargar resultados reales
                        csv_real = df_resultado.to_csv(index=False)
                        st.download_button(
                            label="📥 Descargar Resultados Reales",
                            data=csv_real,
                            file_name="top_5_estados_real.csv",
                            mime="text/csv"
                        )
                    else:
                        st.warning("⚠️ No se pudieron obtener datos de domestic o international")
                else:
                    st.warning("⚠️ No se encontraron datos para esta consulta")
                    
            except Exception as e:
                st.error(f"❌ Error al ejecutar consulta: {str(e)}")
                st.info("💡 **Nota:** Asegúrate de que las tablas 'airports', 'domestic', 'international' y 'state' existan en Supabase")
        
# QUERY 5: Mejora de ranking
elif query_seleccionado == "⬆️ Aeropuertos que Mejoraron su Ranking Total":
    st.subheader("**Aeropuertos que mejoraron su ranking total del 2022 al 2023**")
    
    with st.expander("🔍 Ver Query SQL", expanded=True):
        st.code("""
SELECT  
    a.name,  
    "2022_rank_total",  
    "2023_rank_total"  
FROM total as t  
INNER JOIN airports as a on a.id = t.airport_id  
WHERE "2023_rank_total" < "2022_rank_total"  
ORDER BY "2023_rank_total" ASC;
        """, language='sql')

    if st.button("🚀 Ejecutar Query", key="query5"):
        with st.spinner("Ejecutando consulta a Supabase..."):
            try:
                # Obtener datos de total con JOIN a airports
                response = supabase.table('total').select("*, airports(name)").execute()
                
                if response.data:
                    df = pd.DataFrame(response.data)
                    
                    # Expandir la columna airports para obtener el campo name
                    df['airport_name'] = df['airports'].apply(lambda x: x['name'] if x else None)
                    
                    # Filtrar aeropuertos que mejoraron su ranking (2023 < 2022)
                    df_filtrado = df[df['2023_rank_total'] < df['2022_rank_total']]
                    
                    # Seleccionar columnas necesarias y ordenar
                    df_resultado = df_filtrado[['airport_name', '2022_rank_total', '2023_rank_total']].copy()
                    df_resultado = df_resultado.rename(columns={'airport_name': 'name'})
                    df_resultado = df_resultado.sort_values('2023_rank_total')
                    df_resultado = df_resultado.reset_index(drop=True)
                    
                    st.success(f"✅ Consulta ejecutada exitosamente. {len(df_resultado)} registros encontrados.")
                    st.dataframe(df_resultado, width='stretch')
                    
                    # Botón para descargar resultados reales
                    csv_real = df_resultado.to_csv(index=False)
                    st.download_button(
                        label="📥 Descargar Resultados Reales",
                        data=csv_real,
                        file_name="mejora_ranking_total_real.csv",
                        mime="text/csv"
                    )
                else:
                    st.warning("⚠️ No se encontraron datos para esta consulta")
                    
            except Exception as e:
                st.error(f"❌ Error al ejecutar consulta: {str(e)}")
                st.info("💡 **Nota:** Asegúrate de que las tablas 'total' y 'airports' existan en Supabase")
            


# Footer
st.markdown("---")
st.markdown("📊 **✈️ Análisis exploratorio de tráfico aéreo en EE.UU 2022-2023** - Grupo 5 (Computación 2) - Universidad Central de Venezuela")
