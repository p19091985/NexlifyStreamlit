import streamlit as st
import sys
import os
import pandas as pd
import plotly.express as px
import altair as alt
import logging

# Path setup
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from utils.st_utils import st_check_session, check_access
    from services.covertype_engine import CovertypeEngine
except ImportError:
    st.error("Erro fatal: Módulos de serviço não encontrados.")
    st.stop()

logger = logging.getLogger(__name__)

st.set_page_config(page_title="Predição Florestal (Covertype)", layout="wide")
st_check_session()
check_access([])
logger.info("Acessando página: Predição Florestal (v2 - Engine Based)")

# --- State ---
def init_state():
    if 'cov_page_number' not in st.session_state: st.session_state.cov_page_number = 0
    if 'cov_full_df' not in st.session_state: st.session_state.cov_full_df = None
    if 'cov_analysis_run' not in st.session_state: st.session_state.cov_analysis_run = False

# --- Controllers ---
def load_data_controller(uploaded_file=None):
    try:
        if uploaded_file:
            st.session_state.cov_full_df = pd.read_csv(uploaded_file)
        else:
            path = CovertypeEngine.get_dataset_path()
            if path:
                st.session_state.cov_full_df = pd.read_csv(path)
        
        st.session_state.cov_page_number = 0
        st.session_state.cov_analysis_run = False
        st.rerun()
    except Exception as e:
        logger.error(f"Erro ao carregar dados: {e}")
        st.error("Falha ao processar arquivo.")

def run_benchmark_controller():
    st.session_state.cov_analysis_run = True

# --- Views ---
def render_metrics_panel(df):
    info, desc, dist = CovertypeEngine.get_stats(df)
    
    st.subheader("📊 Estatísticas e Distribuição")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Altair para distribuição (limpo e estatístico)
        c = alt.Chart(dist).mark_bar().encode(
            x=alt.X('Cover_Type', title='Classe Florestal'),
            y=alt.Y('Count', title='Ocorrências'),
            color=alt.Color('Cover_Type', legend=None),
            tooltip=['Cover_Type', 'Count']
        ).properties(height=300).interactive()
        st.altair_chart(c, use_container_width=True)
        
    with col2:
        st.metric("Total de Amostras", len(df))
        st.metric("Classes Únicas", len(dist))

def render_benchmark_results(df):
    if not st.session_state.cov_analysis_run: return
    
    st.divider()
    st.subheader("🏆 Torneio de Modelos (Benchmark)")
    
    prog_bar = st.progress(0, "Iniciando Engine...")
    
    # Callback simples para atualizar a barra de progresso da UI
    def progress_callback(p, t):
        prog_bar.progress(p, text=t)
        
    results_df = CovertypeEngine.run_benchmark(df, callback_progress=progress_callback)
    
    if not results_df.empty:
        # Plotly para comparação detalhada
        fig = px.bar(
            results_df, x='F1-Score', y='Modelo', orientation='h',
            color='F1-Score', title='Performance Relativa (F1-Score)',
            text_auto='.2%', color_continuous_scale='Viridis'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(
            results_df.style.format({"Acurácia": "{:.2%}", "F1-Score": "{:.2%}"}),
            use_container_width=True
        )
    else:
        st.error("Nenhum resultado gerado.")

def render_main():
    st.title("🌲 Predição de Cobertura Florestal")
    
    with st.sidebar:
        st.header("Dados")
        if st.button("Carregar Padrão"):
            load_data_controller()
        st.file_uploader("Upload CSV", key="u_file", on_change=lambda: load_data_controller(st.session_state.u_file) if st.session_state.u_file else None)

    if st.session_state.cov_full_df is not None:
        render_metrics_panel(st.session_state.cov_full_df)
        
        if st.button("🚀 Iniciar Benchmark", type="primary"):
            run_benchmark_controller()
            
        render_benchmark_results(st.session_state.cov_full_df)
    else:
        st.info("Carregue o dataset para iniciar.")

if __name__ == "__main__":
    init_state()
    render_main()