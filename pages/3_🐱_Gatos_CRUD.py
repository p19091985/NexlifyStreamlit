import streamlit as st
import sys                                             
import os                                              

                        
                                                                                    

from utils.st_utils import st_check_session, check_access
from components.gatos_controller import GatosController   

st.set_page_config(page_title="Gerenciador de Gatos", layout="wide")
st_check_session()
check_access([])

controller = GatosController()
controller.run()