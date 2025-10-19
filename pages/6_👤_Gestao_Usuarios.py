import streamlit as st
import sys          
import os           

                        
                                                                                    

from utils.st_utils import st_check_session, check_access
from components.usuarios_controller import UsuariosController

                           
st.set_page_config(page_title="Gestão de Usuários", layout="wide")

                                   
st_check_session()
                                                                  
check_access(['Administrador Global', 'Gerente de TI'])

                                   
controller = UsuariosController()
controller.run()