import streamlit as st
import sys
import os
import logging

# Caminho para utils (ajuste relativo)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from utils.st_utils import st_check_session
except ImportError:
    def st_check_session(): pass

logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="Sobre o Sistema",
    layout="wide",
    page_icon="ℹ️"
)

st_check_session()
logger.info("Acessando página: Sobre")

def render_main_panel():
    st.title("ℹ️ Sobre o Sistema")
    st.markdown("---")

    st.info("""
        **Nexlify Streamlit - Versão 3.1**

        Plataforma moderna de **Demonstração de Arquitetura Serverless Local**.
        O sistema opera com uma abordagem centrada em arquivos para persistência de dados, garantindo portabilidade,
        alta performance e robustez sem dependências externas complexas.
    """)

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.subheader("🏗️ Arquitetura de Dados")
        st.markdown("""
        **Tecnologias de Persistência:**
        
        * **JSON Storage Engine:**
            * Todos os dados são armazenados na estrutura `data/*.json`.
            * Formato legível, fácil de transportar e ideal para ambientes locais.

        * **Atomic File Locking:**
            * Mecanismo avançado que previne conflitos de escrita (Race Conditions).
            * Garante integridade transacional mesmo em acessos simultâneos.

        * **Generic Repository Pattern:**
            * Abstração Pythonica para operações de I/O.
            * Separação completa entre a lógica de aplicação e a camada de dados.
        """)

    with col2:
        st.subheader("💻 Stack Tecnológico")
        st.markdown("""
        **Frontend & UX:**

        * **Pure Python UI (Streamlit):**
            * Interface declarativa construída 100% em Python.
            * Componentes ricos (Dataframes interativos, Gráficos Plotly/Altair).

        * **Visualização Híbrida:**
            * Integração simultânea de **Plotly Express** (Interatividade e 3D) e **Altair** (Estatística Declarativa).

        * **Política de Acesso:**
            * **Open Access:** Sistema totalmente aberto, focado na experiência do usuário e na análise de dados imediata.
        """)

    st.markdown("---")
    st.caption("© 2026 Nexlify Streamlit | Serverless Architecture Demonstration")

if __name__ == "__main__":
    render_main_panel()