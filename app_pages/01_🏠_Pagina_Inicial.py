import streamlit as st
from utils.st_utils import st_check_session, check_access
from pathlib import Path
from components import servicos_gerenciador as servico
st.set_page_config(page_title='Página Inicial', layout='wide', page_icon='🏠')
st_check_session()
try:
    allowed_roles = servico.get_allowed_roles_for_page(Path(__file__).name)
    check_access(allowed_roles)
except Exception as e:
    st.error(f'Erro ao verificar permissões: {e}')
    st.stop()
user_name = st.session_state.get('usuario_nome', st.session_state.get('user_info', {}).get('name', 'Usuário'))
st.title(f'Bem-vindo, {user_name}!')
st.header('Painel de Controle Moderno')
st.markdown('\nEste é o sistema de demonstração migrado para a arquitetura Streamlit.\n\n**Utilize a barra lateral à esquerda para navegar entre as diferentes páginas do sistema.**\n\nCada página representa um "painel" da aplicação original, adaptado para o ambiente web.\nA lógica de negócios e o acesso ao banco de dados foram preservados.\n')