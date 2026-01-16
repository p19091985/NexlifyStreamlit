import streamlit as st
import sys
import os
import pandas as pd
import logging
from typing import Optional

# Adicionar root ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from utils.st_utils import st_check_session, check_access
    # Importação do Engine - Camada de Serviço
    from services.iris_engine import IrisEngine
except ImportError as e:
    st.error(f"Erro de Importação Crítico: {e}")
    st.stop()

logger = logging.getLogger(__name__)

st.set_page_config(page_title="Explorador de Dados Iris", layout="wide")

st_check_session()                                     
check_access([])
logger.info("Acessando página: Explorador de Dados Iris (v2 - Engine Based)")

# --- State Management ---
def init_state() -> None:
    if 'page_number' not in st.session_state:
        st.session_state.page_number = 0
    if 'full_df' not in st.session_state:
        st.session_state.full_df = None

# --- Logic Controllers ---
def load_data_controller(source="local", uploaded_file=None):
    df = None
    
    try:
        if source == "web":
            with st.spinner("Conectando ao repositório remoto..."):
                df, err = IrisEngine.fetch_from_web()
                if err: 
                    st.sidebar.error(f"Erro: {err}")
                else: 
                    st.sidebar.success("Dados baixados com sucesso!")

        elif source == "upload" and uploaded_file:
             df = pd.read_csv(uploaded_file)
             st.sidebar.success(f"Arquivo '{uploaded_file.name}' processado.")

        elif source == "local":
            path = IrisEngine.get_default_csv_path()
            if path and os.path.exists(path):
                df = pd.read_csv(path)
        
        if df is not None:
            # Normalização Centralizada
            df = IrisEngine.normalize_columns(df)
            st.session_state.full_df = df
            st.session_state.page_number = 0
            
    except Exception as e:
        logger.error(f"Erro no controlador de dados: {e}")
        st.sidebar.error("Falha ao carregar dados.")

# --- UI Components ---
def render_sidebar():
    st.sidebar.header("🗂️ Configuração de Dados")
    data_source = st.sidebar.radio("Fonte", ["Local (Padrão)", "Upload CSV", "Web (GitHub)"])
    
    if data_source == "Local (Padrão)":
        if st.sidebar.button("🔄 Carregar/Resetar"):
            load_data_controller("local")
            st.rerun()
            
    elif data_source == "Upload CSV":
        uploaded = st.sidebar.file_uploader("Arquivo CSV", type="csv")
        if uploaded:
            load_data_controller("upload", uploaded_file=uploaded)
            
    elif data_source == "Web (GitHub)":
        if st.sidebar.button("☁️ Baixar Dataset"):
            load_data_controller("web")
            st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.subheader("🔎 Filtro Ativo")
    
    df = st.session_state.full_df
    filtered_df = df
    
    if df is not None:
        # --- Self-Healing: Garantir Normalização ---
        if 'species' not in df.columns:
            logger.warning("Detectado DataFrame não normalizado no Session State. Tentando corrigir...")
            try:
                df = IrisEngine.normalize_columns(df)
                st.session_state.full_df = df # Atualiza o state corrigido
            except Exception as e:
                logger.error(f"Falha na auto-correção: {e}")
                st.error("Erro nos dados. Por favor recarregue.")
                st.session_state.full_df = None
                st.rerun()

        species_list = list(df['species'].unique())
        selected = st.sidebar.multiselect("Espécies", species_list, default=species_list)
        if selected: filtered_df = df[df['species'].isin(selected)]
        st.sidebar.caption(f"Visualizando: {len(filtered_df)} registros")
    
    return filtered_df

def render_metrics(df):
    cols = st.columns(4)
    cols[0].metric("Amostras", len(df))
    cols[1].metric("Variáveis", df.shape[1])
    if 'species' in df.columns: cols[2].metric("Classes", df['species'].nunique())

def render_data_tab(df):
    # Paginação simples
    limit = 20
    total = len(df)
    pages = max(1, (total // limit) + (1 if total % limit > 0 else 0))
    
    # Simple pagination controls
    col1, _, col3 = st.columns([1, 4, 1])
    
    if col1.button("⬅️", disabled=st.session_state.page_number == 0):
        st.session_state.page_number -= 1
        st.rerun()
        
    if col3.button("➡️", disabled=st.session_state.page_number >= pages - 1):
        st.session_state.page_number += 1
        st.rerun()
        
    start = st.session_state.page_number * limit
    st.dataframe(df.iloc[start:start+limit], use_container_width=True)
    st.caption(f"Página {st.session_state.page_number + 1}/{pages}")
    
    st.download_button("⬇️ Baixar CSV", df.to_csv(index=False).encode('utf-8'), "data.csv")

def render_main():
    st.title("🌷 Explorador de Dados Iris")
    
    if st.session_state.full_df is None:
        load_data_controller("local")
        
    filtered_df = render_sidebar()
    
    if filtered_df is not None and not filtered_df.empty:
        render_metrics(filtered_df)
        
        tab1, tab2, tab3 = st.tabs(["📋 Dados", "📊 Análise Visual", "🧊 Laboratório 3D"])
        
        with tab1: render_data_tab(filtered_df)
            
        with tab2:
            st.subheader("Análise Híbrida (Plotly + Altair)")
            # Delegação total para o Engine
            charts = IrisEngine.generate_plots(filtered_df)
            
            row1 = st.columns(2)
            row1[0].plotly_chart(charts['plotly_scatter'], use_container_width=True)
            row1[1].altair_chart(charts['altair_scatter'], use_container_width=True)
            
            row2 = st.columns(2)
            row2[0].altair_chart(charts['altair_bar'], use_container_width=True)
            row2[1].plotly_chart(charts['plotly_box'], use_container_width=True)
            
            st.altair_chart(charts['altair_hist'], use_container_width=True)
                
        with tab3:
            st.subheader("Projeção Latente (PCA)")
            pca_fig = IrisEngine.perform_pca(filtered_df)
            if pca_fig: st.plotly_chart(pca_fig, use_container_width=True)
            else: st.warning("Dados insuficientes.")

    else:
        st.info("Carregue os dados para iniciar.")

if __name__ == "__main__":
    init_state()
    render_main()