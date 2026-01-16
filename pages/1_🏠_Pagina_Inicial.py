import streamlit as st
import logging
from utils.st_utils import st_check_session

logger = logging.getLogger(__name__)

# Configuração consistente
st.set_page_config(page_title="Página Inicial", layout="wide")

st_check_session()
logger.info("Acessando página: Home")

def render_main_panel():
    st.title("🏠 Nexlify Streamlit")
    st.subheader("Plataforma de Demonstração de Arquitetura Serverless")
    st.markdown("---")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("""
        ### Bem-vindo ao Sistema
        
        O **Nexlify Streamlit** é uma aplicação de referência construída para demonstrar padrões modernos de desenvolvimento em Python.
        O foco principal é oferecer uma experiência fluida de análise de dados e machine learning, sustentada por uma arquitetura de dados leve e portátil.

        #### 🚀 Funcionalidades Ativas:
        
        *   **Análise de Dados Avançada:**
            *   Exploração interativa do dataset **Iris** com gráficos híbridos (Plotly + Altair).
            *   Benchmark de algoritmos de ML com o dataset **Covertype**.
        
        *   **Personalização:**
            *   Editor de temas em tempo real para ajuste da identidade visual.
            *   Layout responsivo e adaptável (Wide Mode).

        *   **Arquitetura:**
            *   Persistência de dados em JSON local (Serverless).
            *   Totalmente Open Access (Livre de autenticação).
        """)

    with col2:
        st.info("""
        **Navegação Rápida**
        
        Use o menu à esquerda para acessar:
        
        1. **Pagina Inicial** (Você está aqui)
        2. **Painel Modelo** (Template Dev)
        3. **Explorador Iris** 🌷
        4. **Predição Covertype** 🌲
        5. **Editor de Tema** 🎨
        6. **Sobre o Sistema** ℹ️
        """)

    st.markdown("---")
    st.success("✅ O sistema está online e operando em modo de Acesso Aberto v3.1.")

if __name__ == "__main__":
    render_main_panel()