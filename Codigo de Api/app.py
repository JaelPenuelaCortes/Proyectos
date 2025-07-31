import streamlit as st

# Aplica el CSS inmediatamente después del import
UST_BLUE = "#002855"
UST_YELLOW = "#FFD100"
UST_GRAY = "#0e1117"
UST_WHITE = "#FFFFFF"

st.markdown(f"""
    <style>
    /* Fondo general de la app */
    .stAppViewContainer {{
        background-color: {UST_GRAY};
    }}

    /* Contenedor principal */
    .appview-container {{
        background-color: {UST_GRAY};
    }}

    /* Cuerpo general */
    .stApp {{
        background-color: {UST_WHITE};
        color: #000000;
        font-family: 'Segoe UI', sans-serif;
    }}

    /* Botones normales */
    .stButton > button {{
        background-color: {UST_YELLOW};
        color: black;
        font-weight: bold;
        border-radius: 10px;
        padding: 0.5em 1em;
    }}

    /* Botones de descarga */
    .stDownloadButton > button {{
        background-color: {UST_BLUE};
        color: white;
        font-weight: bold;
        border-radius: 10px;
        padding: 0.5em 1em;
    }}

    /* Tabs */
    .stTabs [data-baseweb="tab"] {{
        font-weight: bold;
        background-color: {UST_WHITE};
        color: {UST_BLUE};
        border-radius: 6px 6px 0 0;
        border: 1px solid #CCC;
    }}

     /* 🔽 ESTILO PARA LOS TEXTOS 🔽 */
    h1, h2, h3, h4, h5, h6 {{
        color: white !important;
    }}
    p {{
        color: white !important;
    }}

    li {{
        color: white !important;
    }}

    /* Cambiar a blanco el nombre y peso del archivo subido */
    .stFileUploaderFileName {{
        color: white !important;
    }}
    .stFileUploaderFileData small {{
        color: white !important;
    }}

    </style>
""", unsafe_allow_html=True)


from cargar_datos import show_data_tab
from transformacion import show_transform_tab
from visualizaciones import show_visualization_tab
from mapa import show_map_tab


# Menú lateral en la izquierda
st.sidebar.title("Menú de opciones")
seccion = st.sidebar.radio(
    "Ir a:",
    ["📥 Carga de Datos", "🔧 Transformación y Métricas", "📊 Visualizaciones", "🗺️ Mapa"]
)

# Mostrar contenido según selección
if seccion == "📥 Carga de Datos":
    show_data_tab()

elif seccion == "🔧 Transformación y Métricas":
    show_transform_tab()
elif seccion == "📊 Visualizaciones":
    show_visualization_tab()
elif seccion == "🗺️ Mapa":
    show_map_tab()




