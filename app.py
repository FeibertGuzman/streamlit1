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
    path = kagglehub.dataset_download("shree0910/ai-and-data-science-job-market-dataset-20202026")
    files = [f for f in os.listdir(path) if f.endswith('.csv')]
    if not files:
        return None
    
    full_path = os.path.join(path, files[0])
    df = pd.read_csv(full_path)
    
    # OPTIMIZACIÓN DEFINITIVA: 
    # Forzamos a que todas las columnas sigan el formato esperado: minúsculas y sin espacios
    df.columns = df.columns.str.strip().str.replace(' ', '_').str.lower()
    
    return df

df = load_data()

# Mapeo de columnas para que el código no se rompa si el CSV cambia
# Buscamos nombres que contengan palabras clave
def find_col(df, keyword):
    for col in df.columns:
        if keyword in col:
            return col
    return df.columns[0] # Fallback a la primera columna

# --- NAVEGACIÓN ---
st.sidebar.title("Navegación")
page = st.sidebar.radio("Ir a:", ["Inicio (Landing Page)", "Dashboard de Análisis"])

if page == "Inicio (Landing Page)":
    st.title("🚀 Análisis del Mercado Laboral en AI & Data Science (2020–2026)")
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("""
        ### Sobre el Proyecto
        Desarrollado para el curso de **Talento Tech**.
        **Autor:** Feibert Guzmán
        """)
        st.info("Usa el menú lateral para navegar.")
    with col2:
        try:
            st.image("image1.png", use_container_width=True)
        except:
            st.warning("Imagen image1.png no encontrada.")

elif page == "Dashboard de Análisis":
    st.title("📊 Panel de Control e Insights")
    
    if df is not None:
        # Identificación automática de columnas críticas
        c_job = find_col(df, 'job')      # Busca algo como 'job_title'
        c_sal = find_col(df, 'salary')   # Busca algo como 'salary_usd'
        c_loc = find_col(df, 'locat')    # Busca algo como 'location'
        c_emp = find_col(df, 'employ')   # Busca algo como 'employment_type'
        c_year = find_col(df, 'year')    # Busca algo como 'year'

        # --- FILTROS ---
        st.sidebar.header("Filtros Globales")
        unique_jobs = df[c_job].unique()
        job_role = st.sidebar.multiselect("Selecciona el Rol:", options=unique_jobs, default=unique_jobs[:3])
        
        df_filtered = df[df[c_job].isin(job_role)]

        # --- MÉTRICAS ---
        m1, m2, m3 = st.columns(3)
        m1.metric("Total de Registros", f"{len(df_filtered):,}")
        m2.metric("Salario Promedio", f"${df_filtered[c_sal].mean():,.2f}")
        m3.metric("Países", df_filtered[c_loc].nunique())

        st.divider()

        # --- GRÁFICOS ---
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            st.subheader("Distribución Salarial")
            fig1 = px.box(df_filtered, x=c_job, y=c_sal, color=c_job, template="plotly_dark")
            st.plotly_chart(fig1, use_container_width=True)
        with col_g2:
            st.subheader("Tipo de Empleo")
            fig2 = px.pie(df_filtered, names=c_emp, hole=0.4)
            st.plotly_chart(fig2, use_container_width=True)

        st.subheader("Evolución de Salarios")
        fig3 = px.line(df_filtered, x=c_year, y=c_sal, color=c_job, markers=True)
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.error("Error al cargar el dataset.")
