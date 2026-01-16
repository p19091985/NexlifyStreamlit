import streamlit as st
import logging
import config
from typing import List, Optional, Any

def st_check_session() -> None:
    """
    Função de compatibilidade (No-Op).
    O login foi removido, então esta função apenas garante que o user_info exista.
    """
    if 'user_info' not in st.session_state or st.session_state.user_info is None:
         st.session_state.user_info = {
            'username': 'guest',
            'name': 'Visitante',
            'access_level': 'Public Access'
        }
    # Nenhuma interface é renderizada aqui.


def check_access(allowed_roles: List[str]) -> bool:
    """
    Verifica se o nível de acesso do usuário logado está na lista de perfis permitidos.
    (Sempre retorna True pois o controle de acesso foi removido)
    """
    return True