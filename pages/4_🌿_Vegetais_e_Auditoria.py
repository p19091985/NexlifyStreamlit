                                   
import streamlit as st
from utils.st_utils import st_check_session, check_access
from components.vegetais_auditoria_controller import VegetaisAuditoriaController

                                                       
st.set_page_config(page_title="Vegetais e Auditoria", layout="wide")
st_check_session()
check_access(['Administrador Global', 'Diretor de Operações', 'Gerente de TI', 'Analista de Dados'])

                                            
controller = VegetaisAuditoriaController()
controller.run()