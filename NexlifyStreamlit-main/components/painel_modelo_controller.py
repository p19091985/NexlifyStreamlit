                                        
import streamlit as st
                                                
from components.painel_modelo_view import PainelModeloView

class PainelModeloController:
    def __init__(self):
                                                  
        self.view = PainelModeloView(self)

    def run(self):
        self.view.render()

    def testar_interacao(self):
        usuario_atual = st.session_state.user_info
        st.success(f"Olá, {usuario_atual['name']}! A interatividade está funcionando corretamente.")
        st.balloons()