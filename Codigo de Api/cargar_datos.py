import streamlit as st
import pandas as pd
#import requests

# ===================================================================
# Función: para cargar datos
# ===================================================================

def show_data_tab():
    """
    Muestra la interfaz para cargar datos desde un archivo Excel.
    El usuario puede subir el archivo y se mostrará una vista previa.
    """
    st.header("📥 Carga de Datos desde Archivo Excel")

    st.markdown("""
    Sube un archivo de Excel (.xlsx o .xls) con los datos que deseas analizar.
    """)

    # Verificar si ya hay un archivo cargado en sesión
    if 'df_raw' not in st.session_state:
        # Subida de archivo Excel
        archivo = st.file_uploader(
            label="Sube el archivo a analizar",
            type=["xlsx", "xls"],
            label_visibility='hidden'
        )

        if archivo is not None:
            try:
                # Leer el archivo Excel
                df_raw = pd.read_excel(archivo)

                # Guardar el DataFrame en sesión
                st.session_state['df_raw'] = df_raw

                st.success(f"¡Archivo cargado correctamente! ({len(df_raw)} filas)")
                st.dataframe(df_raw.head(50), height=1200)

            except Exception as e:
                st.error(f"Error al leer el archivo: {e}")
        else:
            st.info("Por favor, sube un archivo para comenzar.")
    else:
        df_raw = st.session_state['df_raw']
        st.success(f"¡Archivo cargado previamente! ({len(df_raw)} filas)")
        st.dataframe(df_raw.head(50), height=1200)


