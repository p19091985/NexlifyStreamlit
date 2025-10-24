import streamlit as st
import logging
import config


def st_check_session():
    """
    Verifica se o usuário está logado.
    Se não, redireciona para a tela de login.
    Se sim, e se o login estiver ativado, renderiza a barra lateral com
    informações do usuário e botão de logout.
    A navegação de páginas é gerenciada automaticamente pelo Streamlit.
    """
    if 'user_info' not in st.session_state or st.session_state.user_info is None:
        st.warning("Acesso negado. Por favor, faça o login.")
        st.switch_page("Home.py")
        st.stop()

                                            
    if config.USE_LOGIN:
        #st.sidebar.divider()
        st.sidebar.title("Painel de Controle")
        st.sidebar.markdown(f"**Usuário:** `{st.session_state.user_info['name']}`")
        st.sidebar.markdown(f"**Perfil:** `{st.session_state.user_info['access_level']}`")

                                                               
        if st.sidebar.button("🚪 Sair", width='stretch', type="primary"):
            logger = logging.getLogger("main_app")
            logger.info(f"Usuário '{st.session_state.user_info['username']}' fez logout.")

                                    
            for key in st.session_state.keys():
                del st.session_state[key]

            st.switch_page("Home.py")
            st.stop()


def check_access(allowed_roles: list):
    """
    Verifica se o nível de acesso do usuário logado está na lista de perfis permitidos.
    Esta função deve ser chamada DEPOIS de st_check_session.
    """
    if not allowed_roles:
        return True

    user_access_level = st.session_state.user_info.get('access_level')
    if user_access_level not in allowed_roles:
        st.error("Você não tem permissão para acessar esta página.")

                                                     
                                                                  
                                                 
        st.image("https://http.cat/401", width='stretch')
                                                        

        st.stop()

    return True