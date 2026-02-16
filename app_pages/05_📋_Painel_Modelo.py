import streamlit as st
from utils.st_utils import st_check_session, check_access
from pathlib import Path
from components import servicos_gerenciador as servico
st.set_page_config(page_title='Painel Modelo', layout='wide', page_icon='📋')
st_check_session()
try:
    allowed_roles = servico.get_allowed_roles_for_page(Path(__file__).name)
    check_access(allowed_roles)
except Exception as e:
    st.error(f'Erro ao verificar permissões: {e}')
    st.stop()

def handle_test_interaction():
    try:
        user_name = st.session_state.get('usuario_nome', st.session_state.get('user_info', {}).get('name', 'Usuário'))
        st.success(f'Olá, {user_name}! A interatividade está funcionando corretamente.')
        st.balloons()
    except Exception as e:
        st.error(f'Erro ao testar interação: {e}')

def render_main_panel():
    st.title('📋 Estrutura de um Novo Painel (Método Simplificado)')
    with st.container(border=True):
        st.subheader('Guia Rápido (Estrutura de Arquivo Único)')
        st.markdown('\n        Este painel serve como um **ponto de partida** para novas telas no padrão simplificado.\n        Para criar uma nova funcionalidade (como Gatos ou Usuários), basta copiar este arquivo.\n\n        **Passos para criar uma nova página de CRUD:**\n\n        1.  **Copie este Arquivo:** Copie este `.py` para um novo arquivo em `app_pages/`\n            (ex: `app_pages/24_📦_Meus_Itens.py`).\n\n        2.  **Seção 1: Configuração:** Ajuste o `st.set_page_config` e registre a página\n            no banco (tabela `pagina`) para o sistema de permissões.\n\n        3.  **Seção 2: Estado:** Adicione as variáveis do `st.session_state` que você precisa\n            (ex: `show_form` e `editing_item`).\n\n        4.  **Seção 3: Lógica de BD:** Crie suas funções de CRUD usando o `UnitOfWork`\n            para acesso ao banco de dados.\n\n        5.  **Seção 4: Lógica de UI (Callbacks):** Crie as funções que os botões irão chamar\n            (ex: `handle_save`, `handle_delete`, `show_add_form`, `close_form_and_rerun`).\n\n        6.  **Seção 5: Renderização (View):** Crie as funções que desenham a interface\n            (ex: `render_form` e `render_table`).\n\n        7.  **Seção 6: Execução Principal:** Adapte o código no final do arquivo para\n            chamar suas funções de renderização na ordem correta.\n        ')
        st.divider()
        st.button('Testar Interação', type='primary', on_click=handle_test_interaction)
render_main_panel()