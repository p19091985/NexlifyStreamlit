import streamlit as st
import sys
import os
import logging
from utils.st_utils import st_check_session, check_access

logger = logging.getLogger(__name__)

st.set_page_config(page_title="Painel Modelo", layout="wide")

st_check_session()
check_access([])
logger.info("Acessando página: Painel Modelo (Template)")

def handle_test_interaction():
    """
    Função chamada quando o botão "Testar Interação" é clicado.
    Demonstração simples de callback.
    """
    try:
        st.success(f"A interatividade está funcionando corretamente.")
        st.info("Sua sessão está ativa.")
        logger.info("Teste de interação executado com sucesso.")
        st.balloons()
    except Exception as e:
        logger.error(f"Erro no teste de interação: {e}")
        st.error(f"Erro ao testar interação: {e}")

def render_main_panel():
    """
    Desenha os componentes visuais da página de modelo.
    """
    st.title("📋 Estrutura de Novo Painel (Arquitetura JSON)")

    with st.container(border=True):
        st.subheader("Guia Rápido: Criando Páginas no Padrão v3.0")
        st.markdown("""
        Este arquivo (`2_📋_Painel_Modelo.py`) serve como template oficial para novas funcionalidades.
        O foco agora é **Simplicidade** e **Segurança de Dados** com arquitetura serverless.

        **Fluxo de Criação Sugerido:**

        1.  **Clonagem:**
            Copie este arquivo para `pages/nome_da_sua_pagina.py`.

        2.  **Configuração:**
            Mantenha `st_check_session()` e `check_access([])` no topo.

        3.  **Acesso a Dados (Thread-Safe):**
            Para ler ou gravar dados, use sempre o `GenericRepository`:
            ```python
            from persistencia.repository import GenericRepository

            # Leitura
            df = GenericRepository.read_table_to_dataframe("tabela_exemplo")

            # Escrita (Atomicamente Segura com FileLock)
            GenericRepository.write_dataframe_to_table(novo_df, "tabela_exemplo")
            ```

        4.  **Estado da Aplicação:**
             Use `st.session_state` para manter dados temporários.

        5.  **Interface (UI):**
            Construa a interface de cima para baixo.
        """)
        st.divider()

        st.button(
            "Testar Ambiente de Execução",
            type="primary",
            on_click=handle_test_interaction,
            help="Clique para verificar se o callback e o session_state estão respondendo."
        )

render_main_panel()