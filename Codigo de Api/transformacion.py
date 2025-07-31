import streamlit as st
import pandas as pd
import plotly.express as px
import io

# Color institucional
UST_BLUE = "#002855"

def show_transform_tab():
    st.title("📊 Dashboard Educativo: Modelo Estrella")

    if 'df_raw' not in st.session_state:
        st.warning("🔺 Primero debes cargar los datos desde la pestaña correspondiente.")
        return

    df = st.session_state['df_raw'].copy()

    # Renombrar columnas para estandarizar
    df = df.rename(columns={
        'DP': 'codigo_departamento',
        'DPNOM': 'departamento',
        'DPMP': 'municipio',
        'MPIO': 'codigo_municipio',
        'AÑO': 'anio',
        'ÁREA GEOGRÁFICA': 'area_geografica',
        'Población': 'poblacion'
    })

    # ========================
    # 1️⃣ Limpieza de Datos
    # ========================
    st.markdown("### 🛠️ Etapas del Flujo de Trabajo")
    st.markdown("""
    1. **Limpieza de datos**  
    2. **Construcción de dimensiones**  
    3. **Modelo estrella y tabla de hechos**  
    4. **Visualización y métricas clave**  
    5. **Descarga y resumen detallado**
    """)

    st.divider()
    st.subheader("1️⃣ Limpieza y Validación de Datos")

    columnas_requeridas = [
        'codigo_departamento', 'departamento', 'municipio', 'codigo_municipio',
        'anio', 'area_geografica', 'poblacion'
    ]

    if not all(col in df.columns for col in columnas_requeridas):
        faltantes = [col for col in columnas_requeridas if col not in df.columns]
        st.error(f"Faltan las siguientes columnas requeridas: {', '.join(faltantes)}")
        return

    df = df[df['departamento'] != 'NACIONAL']
    df = df[columnas_requeridas]
    df.columns = df.columns.str.lower()

    for col in df.columns:
        if col not in ['departamento', 'municipio', 'area_geografica']:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    df_clean = df.dropna()

    col1, col2 = st.columns(2)
    col1.metric("Registros originales", len(st.session_state['df_raw']))
    col2.metric("Registros válidos", len(df_clean))

    # ========================
    # 2️⃣ Dimensiones
    # ========================
    st.divider()
    st.subheader("2️⃣ Dimensiones del Modelo Estrella")

    dim_tiempo = (
        df_clean[['anio']].drop_duplicates().sort_values(by='anio').reset_index(drop=True)
        .assign(id_tiempo=lambda d: d.index + 1)
    )

    dim_geo = (
        df_clean[['codigo_departamento', 'departamento', 'municipio']]
        .drop_duplicates(subset=['codigo_departamento', 'municipio'])
        .sort_values(by=['codigo_departamento', 'municipio'])
        .reset_index(drop=True)
        .assign(id_geo=lambda d: d.index + 1)
    )

    col3, col4 = st.columns(2)
    col3.metric("Dimensión Tiempo", len(dim_tiempo))
    col4.metric("Dimensión Geográfica", len(dim_geo))

    # ========================
    # 3️⃣ Tabla de Hechos
    # ========================
    st.divider()
    st.subheader("3️⃣ Tabla de Hechos")

    df_fact = (
        df_clean
        .merge(dim_tiempo, on='anio')
        .merge(dim_geo, on=['codigo_departamento', 'departamento', 'municipio'], how='inner')
        [['id_tiempo', 'id_geo', 'poblacion']]
    )

    df_fact2 = (
    df_clean
    .groupby(['departamento', 'municipio', 'anio'], as_index=False)[['poblacion']]
    .sum()
    )

    ## unir df_fact2
    st.session_state['df_fact2'] = df_fact2


    st.success(f"✅ Tabla de hechos construida con {len(df_fact):,} registros.")
    st.session_state.update({
        'df_fact': df_fact,
        'dim_tiempo': dim_tiempo,
        'dim_geo': dim_geo
    })

    # ========================
    # 4️⃣ Visualizaciones
    # ========================
    st.divider()
    st.subheader("4️⃣ Indicadores y Visualizaciones")

    poblacion_top = (
        df_fact
        .merge(dim_geo, on='id_geo')
        .groupby('municipio')['poblacion']
        .mean()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.bar(
        poblacion_top,
        x='municipio',
        y='poblacion',
        title='Top 10 Municipios por Población Promedio',
        labels={'poblacion': 'Población'},
        color_discrete_sequence=[UST_BLUE]
    )
    st.plotly_chart(fig, use_container_width=True)


    # ========================
    # 5️⃣ Exportación y Resumen
    # ========================
    st.divider()
    st.subheader("5️⃣ Vista y Descarga de la Tabla de Hechos")

    st.dataframe(df_fact2.head(50))

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df_fact.to_excel(writer, index=False, sheet_name='TablaHechos')
    output.seek(0)

    st.download_button(
        label="📥 Descargar Tabla de Hechos",
        data=output,
        file_name='tabla_hechos_educacion.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    st.divider()
    st.subheader("📈 Resumen por Departamento y Año")

    df_fact_ext = (
        df_fact
        .merge(dim_geo, on='id_geo')
        .merge(dim_tiempo, on='id_tiempo')
    )

    resumen = (
        df_fact_ext
        .groupby(['departamento', 'anio'])[['poblacion']]
        .sum()
        .reset_index()
    )

    # Guardar en session_state
    st.session_state['resumen'] = resumen

    st.dataframe(resumen)

    output_resumen = io.BytesIO()
    with pd.ExcelWriter(output_resumen, engine='openpyxl') as writer:
        resumen.to_excel(writer, index=False, sheet_name='Resumen')
    output_resumen.seek(0)

    st.download_button(
        label="📥 Descargar de Estadisticas por Departamento y Año",
        data=output_resumen,
        file_name='Estadisticas_Departamento_Año.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
