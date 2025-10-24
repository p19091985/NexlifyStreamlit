                            
import streamlit as st
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.st_utils import st_check_session, check_access
from components.painel_modelo_controller import PainelModeloController

st.set_page_config(page_title="Painel Modelo", layout="wide")
st_check_session()
check_access([])

controller = PainelModeloController()
controller.run()