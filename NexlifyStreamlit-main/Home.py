import sys
import os
import streamlit as st
import config
from persistencia import auth, database, logger

def validar_configuracoes():
    """
    Verifica se a combinação de flags no arquivo config.py é lógica e válida.
    Se uma combinação inválida for encontrada, exibe um erro e para a aplicação.
    """

    if config.USE_LOGIN and not config.DATABASE_ENABLED:
        st.set_page_config(page_title="Erro de Configuração", layout="centered")
        st.title("❌ Erro de Configuração Inválida")
        st.error(
            "A aplicação não pode iniciar devido a uma configuração inconsistente."
        )
        st.warning(
            """
            **Problema Detectado:**
            - `USE_LOGIN` está definido como `True`.
            - `DATABASE_ENABLED` está definido como `False`.

            **Motivo:** O sistema de login requer acesso ao banco de dados para verificar
            as credenciais dos usuários. É impossível autenticar um usuário com o banco
            de dados desativado.
            """
        )
        st.info("**Solução:** Altere seu arquivo `config.py` para uma das opções abaixo e reinicie o servidor:"
                "\n1. Habilite o banco de dados: `DATABASE_ENABLED = True`"
                "\n2. Desabilite o login: `USE_LOGIN = False` (Modo de Desenvolvimento Offline)")
        st.stop()

    if config.INITIALIZE_DATABASE_ON_STARTUP and not config.DATABASE_ENABLED:
        st.set_page_config(page_title="Erro de Configuração", layout="centered")
        st.title("❌ Erro de Configuração Inválida")
        st.error(
            "A aplicação não pode iniciar devido a uma configuração inconsistente."
        )
        st.warning(
            """
            **Problema Detectado:**
            - `INITIALIZE_DATABASE_ON_STARTUP` está definido como `True`.
            - `DATABASE_ENABLED` está definido como `False`.

            **Motivo:** O sistema não pode criar as tabelas do banco de dados (schema)
            se o acesso ao banco de dados como um todo está desativado.
            """
        )
        st.info("**Solução:** Altere seu arquivo `config.py` para uma das opções abaixo e reinicie o servidor:"
                "\n1. Habilite o banco de dados: `DATABASE_ENABLED = True`"
                "\n2. Desabilite a inicialização automática: `INITIALIZE_DATABASE_ON_STARTUP = False`")
        st.stop()

validar_configuracoes()

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

st.set_page_config(page_title="Painel de Controle", layout="wide")

if 'logger_setup' not in st.session_state:
    logger.setup_loggers()
    st.session_state.logger_setup = True

if 'db_initialized' not in st.session_state and config.DATABASE_ENABLED:
    if config.INITIALIZE_DATABASE_ON_STARTUP:
        try:
            database.DatabaseManager.initialize_database()
            st.session_state.db_initialized = True
        except Exception as e:
            st.error(f"Falha crítica na inicialização do banco de dados: {e}")
            st.stop()
    else:
        st.session_state.db_initialized = True

if 'user_info' not in st.session_state:
    st.session_state.user_info = None
if 'login_attempts' not in st.session_state:
    st.session_state.login_attempts = 0

@st.dialog("Autenticação Necessária", dismissible=False)
def login_dialog():
    """Renderiza o formulário de login."""
    st.markdown("### Por favor, faça o login para continuar")

    if st.session_state.login_attempts >= config.MAX_LOGIN_ATTEMPTS:
        st.error("Acesso bloqueado. Número máximo de tentativas de login excedido.")
                                                                      
        if st.button("OK"):
            st.stop()
        return                                             

    show_password = st.checkbox("Mostrar senha", key="show_password_dialog")
    password_type = "text" if show_password else "password"

    with st.form("login_form_dialog"):
        username = st.text_input("Usuário", key="username_input_dialog")
        password = st.text_input("Senha", type=password_type, key="password_input_dialog")
        submitted = st.form_submit_button("Entrar", type="primary")

        if submitted:
            if not config.DATABASE_ENABLED:
                st.error("O sistema de login está desabilitado pois o banco de dados não está ativo.")
                                                           
                return

            user_data = auth.verify_user_credentials(username, password)
            if user_data == "connection_error":
                st.error("Falha na conexão com o banco de dados.")
                                                           
            elif user_data:
                               
                st.session_state.user_info = user_data
                st.session_state.login_attempts = 0
                st.rerun()                                                                  
            else:
                              
                st.session_state.login_attempts += 1
                st.error("Usuário ou senha inválidos.")                            
                remaining = config.MAX_LOGIN_ATTEMPTS - st.session_state.login_attempts
                if remaining > 0:
                    st.warning(f"Você tem {remaining} tentativa(s) restante(s).")
                else:
                    st.error("Acesso bloqueado!")

st.title("🚀 Painel de Controle Moderno")
st.header("Sistema de Demonstração")
st.markdown("---")

if config.USE_LOGIN:
                                                   
    if st.session_state.user_info is None:
        st.info("Aguardando autenticação do usuário...")
        login_dialog()                           
                                                                        
    else:
        st.success(f"Autenticado como {st.session_state.user_info['name']}! Redirecionando...")
        st.switch_page("pages/1_🏠_Pagina_Inicial.py")
else:
                                       
    if st.session_state.user_info is None:
        st.session_state.user_info = {
            'username': 'dev_user',
            'name': 'Usuário de Desenvolvimento',
            'access_level': 'Administrador Global'
        }
    st.info("Login desabilitado em modo de desenvolvimento. Redirecionando...")
    st.switch_page("pages/1_🏠_Pagina_Inicial.py")