import streamlit as st
import sys
import os
from utils.st_utils import st_check_session, check_access

# =============================================================================
# 1. CONFIGURAÇÃO DA PÁGINA E VERIFICAÇÃO DE ACESSO
# =============================================================================

st.set_page_config(page_title="Painel Modelo", layout="wide")

# Verifica se o usuário está logado e se tem permissão
st_check_session()
check_access([])  # Lista vazia significa que todos os logados podem ver


# =============================================================================
# 2. INICIALIZAÇÃO DO ESTADO DA PÁGINA (st.session_state)
# =============================================================================

# (Esta página é simples e não precisa de estado,
# mas aqui é onde você colocaria:)
#
# if "variavel_exemplo" not in st.session_state:
#     st.session_state.variavel_exemplo = "Valor Padrão"

# =============================================================================
# 3. FUNÇÕES DE ACESSO AO BANCO DE DADOS (Lógica "Repository")
# =============================================================================

# (Esta página não acessa o banco,
# mas aqui é onde você colocaria suas funções de CRUD:)
#
# def get_all_items():
#     return GenericRepository.read_table_to_dataframe('nome_tabela')
#
# def add_item(nome):
#     df = pd.DataFrame([{'nome': nome}])
#     GenericRepository.write_dataframe_to_table(df, 'nome_tabela')

# =============================================================================
# 4. FUNÇÕES DE LÓGICA DE UI (Lógica "Controller" / Callbacks)
# =============================================================================

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


# =============================================================================
# 5. FUNÇÕES DE RENDERIZAÇÃO DA INTERFACE (Lógica "View")
# =============================================================================

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

        # O 'on_click' agora chama nossa função local 'handle_test_interaction'
        st.button(
            "Testar Interação",
            type="primary",
            on_click=handle_test_interaction
        )


# =============================================================================
# 6. EXECUÇÃO PRINCIPAL DA PÁGINA
# (Este é o "cérebro" que decide o que mostrar e quando)
# =============================================================================

# Simplesmente chamamos nossa função principal de renderização
render_main_panel()