import streamlit as st
import pandas as pd
import plotly.express as px
import kagglehub
import os

# Configuración de la página
st.set_page_config(
    page_title="AI & Data Science Job Market Analysis",
    page_icon="📊",
    layout="wide"
)

# --- FUNCIÓN PARA CARGAR DATOS ---
@st.cache_data
def load_data():
    # Descarga desde Kaggle usando la librería kagglehub
    path = kagglehub.dataset_download("shree0910/ai-and-data-science-job-market-dataset-20202026")
    
    # Buscamos el archivo CSV en la ruta descargada
    files = [f for f in os.listdir(path) if f.endswith('.csv')]
    if not files:
        return None
    
    full_path = os.path.join(path, files[0])
    df = pd.read_csv(full_path)
    return df

# Carga inicial
df = load_data()

# --- NAVEGACIÓN LATERAL ---
st.sidebar.title("Navegación")
page = st.sidebar.radio("Ir a:", ["Inicio (Landing Page)", "Dashboard de Análisis"])

# --- PÁGINA DE INICIO (LANDING PAGE) ---
if page == "Inicio (Landing Page)":
    st.title("🚀 Análisis del Mercado Laboral en AI & Data Science (2020–2026)")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        ### Sobre el Proyecto
        Este proyecto ha sido desarrollado para el curso de **Talento Tech**, enfocado en el análisis de tendencias 
        del mercado laboral en áreas de Inteligencia Artificial y Ciencia de Datos.
        
        **Objetivos del Proyecto:**
        * Identificar los roles más demandados.
        * Analizar la evolución de los salarios.
        * Comprender las habilidades técnicas clave para el futuro.
        
        **Desarrollado por:** Feiber Guzmán
        """)
        st.info("Utiliza el menú lateral para explorar el Dashboard interactivo.")

    with col2:
        # Aquí se inserta la imagen que mencionaste
        st.image("image1.png", caption="Visualización del Ecosistema de Datos", use_container_width=True)

    st.divider()
    st.subheader("Ficha Técnica del Dataset")
    st.write("""
    El dataset contiene datos sintéticos que simulan patrones reales de contratación, incluyendo:
    - Roles laborales y características de empresas.
    - Habilidades técnicas requeridas y niveles educativos.
    - Rangos salariales y ubicaciones geográficas.
    """)

# --- PÁGINA DEL DASHBOARD ---
elif page == "Dashboard de Análisis":
    st.title("📊 Panel de Control e Insights")
    
    if df is not None:
        # --- FILTROS ---
        st.sidebar.header("Filtros Globales")
        job_role = st.sidebar.multiselect("Selecciona el Rol:", options=df['Job_Title'].unique(), default=df['Job_Title'].unique()[:3])
        
        df_filtered = df[df['Job_Title'].isin(job_role)]

        # --- MÉTRICAS CLAVE ---
        m1, m2, m3 = st.columns(3)
        m1.metric("Total de Registros", f"{len(df_filtered):,}")
        m2.metric("Salario Promedio", f"${df_filtered['Salary_USD'].mean():,.2f}")
        m3.metric("Países Representados", df_filtered['Location'].nunique())

        st.divider()

        # --- GRÁFICOS ---
        col_g1, col_g2 = st.columns(2)

        with col_g1:
            st.subheader("Distribución Salarial por Rol")
            fig1 = px.box(df_filtered, x='Job_Title', y='Salary_USD', color='Job_Title', template="plotly_dark")
            st.plotly_chart(fig1, use_container_width=True)

        with col_g2:
            st.subheader("Demanda por Tipo de Empleo")
            fig2 = px.pie(df_filtered, names='Employment_Type', hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig2, use_container_width=True)

        st.subheader("Evolución de Salarios (2020-2026)")
        fig3 = px.line(df, x='Year', y='Salary_USD', color='Job_Title', markers=True)
        st.plotly_chart(fig3, use_container_width=True)
        
        # Tabla de datos
        with st.expander("Ver Datos Crutos"):
            st.dataframe(df_filtered)
    else:
        st.error("No se pudo cargar el dataset. Verifica la conexión con Kaggle.")
