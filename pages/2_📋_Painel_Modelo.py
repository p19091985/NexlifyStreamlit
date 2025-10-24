import streamlit as st
import sys
import os
from utils.st_utils import st_check_session, check_access

st.set_page_config(page_title="Painel Modelo", layout="wide")

st_check_session()
check_access([])

def handle_test_interaction():
    """
    Função chamada quando o botão "Testar Interação" é clicado.
    (Esta lógica veio do antigo 'painel_modelo_controller.py')
    """
    try:
        usuario_atual = st.session_state.user_info
        st.success(f"Olá, {usuario_atual['name']}! A interatividade está funcionando corretamente.")
        st.balloons()
    except Exception as e:
        st.error(f"Erro ao testar interação: {e}")

def render_main_panel():
    """
    Desenha os componentes visuais da página na tela.
    (Esta lógica veio do antigo 'painel_modelo_view.py' e foi atualizada)
    """
    st.title("📋 Estrutura de um Novo Painel (Método Simplificado)")

    with st.container(border=True):
        st.subheader("Guia Rápido (Estrutura de Arquivo Único)")
        st.markdown("""
        Este painel serve como um **ponto de partida** para novas telas no padrão simplificado.
        Para criar uma nova funcionalidade (como Gatos ou Usuários), basta copiar este arquivo.

        **Passos para criar uma nova página de CRUD:**

        1.  **Copie este Arquivo:** Copie `2_📋_Painel_Modelo.py` para um novo arquivo em `pages/`
            (ex: `pages/4_📦_Meus_Itens.py`).

        2.  **Seção 1: Configuração:** Ajuste o `st.set_page_config` e as permissões em `check_access`.

        3.  **Seção 2: Estado:** Adicione as variáveis do `st.session_state` que você precisa
            (ex: `show_form` e `editing_item`).

        4.  **Seção 3: Lógica de BD:** Crie suas funções de CRUD (ex: `get_all_items`, `add_item`,
            `update_item`, `delete_item`) usando o `GenericRepository`.

        5.  **Seção 4: Lógica de UI (Callbacks):** Crie as funções que os botões irão chamar
            (ex: `handle_save`, `handle_delete`, `show_add_form`, `close_form_and_rerun`).

        6.  **Seção 5: Renderização (View):** Crie as funções que desenham a interface
            (ex: `render_form` e `render_table`).

        7.  **Seção 6: Execução Principal:** Adapte o código no final do arquivo para
            chamar suas funções de renderização na ordem correta.
        """)
        st.divider()

        st.button(
            "Testar Interação",
            type="primary",
            on_click=handle_test_interaction
        )

render_main_panel()