import sys
import os
import streamlit as st
import config
from persistencia import logger
# 'auth' import removed

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

st.set_page_config(page_title="Painel de Controle", layout="wide")

if 'logger_setup' not in st.session_state:
    logger.setup_loggers()
    st.session_state.logger_setup = True

if 'db_initialized' not in st.session_state:
    st.session_state.db_initialized = True

# Dummy user info for legacy compatibility (if any page relies on it)
if 'user_info' not in st.session_state:
    st.session_state.user_info = {
        'username': 'guest',
        'name': 'Visitante',
        'access_level': 'Public Access'
    }

st.title("🚀 Painel de Controle Moderno")
st.header("Sistema de Demonstração (Acesso Aberto)")
st.markdown("---")

st.info("Sistema de Login removido. Acesso liberado.")
st.success(f"Bem-vindo, {st.session_state.user_info['name']}! Redirecionando...")
st.switch_page("pages/1_🏠_Pagina_Inicial.py")