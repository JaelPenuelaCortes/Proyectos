import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

def show_visualization_tab():
    st.header("📈 Visualizaciones de Población")

    if 'df_fact' not in st.session_state or 'resumen' not in st.session_state:
        st.warning("Primero debes construir la tabla de hechos en la pestaña 'Transformación y Métricas'.")
        return

    df_fact = st.session_state['df_fact']
    dim_geo = st.session_state['dim_geo']
    dim_tiempo = st.session_state['dim_tiempo']
    resumen = st.session_state['resumen']

    df = df_fact.merge(dim_geo, on='id_geo').merge(dim_tiempo, on='id_tiempo')

    # ================================
    # GRÁFICO 1: Serie de tiempo por departamento
    # ================================
    st.subheader("📊 Evolución de la Población por Departamento")

    deptos = sorted(df['departamento'].unique())
    selected_depto_1 = st.selectbox("Selecciona un departamento", deptos)

    df_1 = df[df['departamento'] == selected_depto_1]
    df_1 = df_1.groupby('anio')['poblacion'].sum().reset_index()

    fig1 = go.Figure()

    fig1.add_trace(go.Scatter(
        x=df_1['anio'],
        y=df_1['poblacion'],
        mode='lines+markers',
        name='Población',
        line=dict(color='blue')
    ))

    fig1.update_layout(
        title=f"Población Total en {selected_depto_1} por Año",
        xaxis_title="Año",
        yaxis_title="Población",
        height=450
    )

    st.plotly_chart(fig1, use_container_width=True)

    # ================================
    # GRÁFICO 2: Comparación por área geográfica
    # ================================

    st.subheader("Gráfico de población por año (municipio y departamento)")

    # Cargar df_fact2 desde el estado
    df = st.session_state.get('df_fact2', None)

    if df is None:
        st.error("❌ No se encontró df_fact2 en session_state.")
        return

    # Validar columnas
    required_cols = {'departamento', 'municipio', 'anio', 'poblacion'}
    if not required_cols.issubset(df.columns):
        st.error("❌ El DataFrame no contiene las columnas necesarias.")
        st.dataframe(df.head())
        return

    # Selector de departamento
    deptos = df['departamento'].dropna().unique()
    selected_depto = st.selectbox("Selecciona un departamento", sorted(deptos), key="select_depto_bar")

    # Filtrar municipios según departamento
    municipios = df[df['departamento'] == selected_depto]['municipio'].dropna().unique()
    selected_muni = st.selectbox("Selecciona un municipio", sorted(municipios), key="select_muni_bar")

    # Filtrar datos para gráfica
    df_filtrado = df[(df['departamento'] == selected_depto) & (df['municipio'] == selected_muni)]

    # Validar datos
    if df_filtrado.empty:
        st.warning(f"No hay datos para {selected_muni} ({selected_depto})")
        return

    # Gráfico de barras por año
    fig = px.bar(
        df_filtrado,
        x='anio',
        y='poblacion',
        labels={'anio': 'Año', 'poblacion': 'Población'},
        title=f"Población por año en {selected_muni} ({selected_depto})",
        text='poblacion'
    )

    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(
        xaxis_title="Año",
        yaxis_title="Población",
        template="plotly_white",
        uniformtext_minsize=8,
        uniformtext_mode='hide'
    )

    st.plotly_chart(fig, use_container_width=True)

    ## Grafico 3

    st.subheader("Municipios con mayor población por año")

    # Cargar DataFrame desde session_state
    df = st.session_state.get('df_fact2', None)

    if df is None:
        st.error("❌ No se encontró df_fact2 en session_state.")
        return

    # Validar columnas necesarias
    required_cols = {'anio', 'municipio', 'poblacion'}
    if not required_cols.issubset(df.columns):
        st.error("❌ El DataFrame no contiene las columnas necesarias.")
        st.dataframe(df.head())
        return

    # Selector de año
    anios = df['anio'].dropna().unique()
    selected_anio = st.selectbox("Selecciona un año", sorted(anios), key="select_anio_top")

    # Filtrar DataFrame por año
    df_anio = df[df['anio'] == selected_anio]

    # Agrupar (en caso de que haya duplicados por municipio)
    df_top = (
        df_anio
        .groupby(['municipio'], as_index=False)['poblacion']
        .sum()
        .sort_values(by='poblacion', ascending=False)
        .head(10)  # Top 10 municipios
    )

    # Validar que haya datos
    if df_top.empty:
        st.warning(f"No hay datos disponibles para el año {selected_anio}")
        return

    # Gráfico de barras horizontal
    fig = px.bar(
        df_top,
        x='poblacion',
        y='municipio',
        orientation='h',
        title=f"Top 10 municipios con mayor población en {selected_anio}",
        text='poblacion',
        labels={'poblacion': 'Población', 'municipio': 'Municipio'}
    )

    fig.update_layout(
        template="plotly_white",
        yaxis={'categoryorder': 'total ascending'},
        xaxis_title="Población",
        yaxis_title="Municipio"
    )

    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')

    st.plotly_chart(fig, use_container_width=True)