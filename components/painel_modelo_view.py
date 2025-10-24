import streamlit as st

class PainelModeloView:
                                                                            
    def __init__(self, controller):
        self.controller = controller

    def render(self):
        st.title("📋 Estrutura de um Novo Painel (Streamlit)")
        with st.container(border=True):
            st.subheader("Guia Rápido")
            st.markdown("""
            Este painel serve como um ponto de partida para novas telas no padrão Streamlit.
            **Passos para criar uma nova página:**

            1. Crie um novo arquivo Python na pasta `pages/` (ex: `pages/X_📁_Meu_Painel.py`). O nome do arquivo define o título e a ordem no menu.
            2. Importe o `streamlit` e as funções utilitárias:
               ```python
               import streamlit as st
               from utils.st_utils import st_check_session, check_access
               ```
            3. No início do arquivo, configure a página e execute as verificações de sessão e acesso:
               ```python
               st.set_page_config(page_title="Meu Painel", layout="wide")
               st_check_session()
               check_access(['Perfil_Permitido_1', 'Perfil_Permitido_2']) # Lista vazia para todos
               ```
            4. Adicione seus widgets e lógica usando as funções do Streamlit (`st.title`, `st.button`, `st.dataframe`, etc.).
            5. Use o `st.session_state` para manter o estado das variáveis entre as interações do usuário.
            """)
            st.divider()
                                                                             
            if st.button("Testar Interação", type="primary", on_click=self.controller.testar_interacao):
                pass