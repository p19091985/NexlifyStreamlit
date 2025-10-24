import streamlit as st
from utils.st_utils import st_check_session

st_check_session()

st.title(f"Bem-vindo, {st.session_state.user_info['name']}!")
st.header("Painel de Controle Moderno")
st.markdown("""
Este é o sistema de demonstração migrado para a arquitetura Streamlit.

**Utilize a barra lateral à esquerda para navegar entre as diferentes páginas do sistema.**

Cada página representa um "painel" da aplicação original, adaptado para o ambiente web.
A lógica de negócios e o acesso ao banco de dados foram preservados.
""")