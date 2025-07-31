import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import st_folium

def show_map_tab():
    st.header("🗺️ Mapa Interactivo de Población por Departamento")

    if 'df_fact' not in st.session_state:
        st.warning("Primero debes construir la tabla de hechos en la pestaña 'Transformación y Métricas'.")
        return

    df_fact = st.session_state['df_fact']
    dim_geo = st.session_state['dim_geo']
    dim_tiempo = st.session_state['dim_tiempo']

    # Merge con dimensiones
    df = df_fact.merge(dim_geo, on='id_geo').merge(dim_tiempo, on='id_tiempo')

    # Años disponibles
    años = sorted(df['anio'].unique())
    año_sel = st.selectbox("Selecciona el año", años, index=len(años)-1)

    # Filtrar y agregar población
    df_filtrado = df[df['anio'] == año_sel]
    resumen = (
        df_filtrado
        .groupby(['codigo_departamento'])[['poblacion']]
        .sum()
        .reset_index()
    )
    resumen['codigo_departamento'] = resumen['codigo_departamento'].astype(str)

    # Leer shapefile
    try:
        gdf = gpd.read_file("data/shapes/MGN_ANM_DPTOS.shp")
    except Exception as e:
        st.error(f"❌ Error al leer el archivo .shp: {e}")
        return

    gdf['DPTO_CCDGO'] = gdf['DPTO_CCDGO'].astype(str)
    resumen['DPTO_CCDGO'] = resumen['codigo_departamento']

    # Unir datos espaciales con la población
    gdf_merged = gdf.merge(resumen, on='DPTO_CCDGO', how='left')

    # Crear mapa
    m = folium.Map(location=[4.6, -74.1], zoom_start=5, tiles="CartoDB positron")

    folium.Choropleth(
        geo_data=gdf_merged,
        name="choropleth",
        data=gdf_merged,
        columns=['DPTO_CCDGO', 'poblacion'],
        key_on='feature.properties.DPTO_CCDGO',
        fill_color='YlOrRd',
        fill_opacity=0.7,
        line_opacity=0.2,
        nan_fill_color='gray',
        legend_name=f"Población Total - {año_sel}",
        highlight=True
    ).add_to(m)

    folium.LayerControl().add_to(m)

    st.subheader(f"👥 Población Total por Departamento - {año_sel}")
    st_folium(m, width=750, height=550)
