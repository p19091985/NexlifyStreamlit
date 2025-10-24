import streamlit as st
import pandas as pd
import config
from persistencia.repository import GenericRepository
from components.gatos_view import GatosView

class GatosController:
    def __init__(self):
        self.view = GatosView(self)
        self._initialize_state()

    def _initialize_state(self):
        if "show_form" not in st.session_state:
            st.session_state.show_form = False
        if "editing_item" not in st.session_state:  
            st.session_state.editing_item = None  

    def run(self):
        if not config.DATABASE_ENABLED:
            st.title("🐱 Gerenciador de Espécies de Gatos")
            st.warning("Funcionalidade indisponível: O banco de dados está desabilitado no arquivo de configuração.")
            return

        self.view.render()

    def open_form(self, item=None):
        st.session_state.editing_item = item  
        st.session_state.show_form = True

    def close_form(self):
        st.session_state.show_form = False
        st.session_state.editing_item = None
        st.rerun()

    def save_item(self, nome, origem, temperamento):
        if not nome.strip():
            st.error("O nome da espécie é obrigatório.")
            return
        try:  
            is_edit_mode = st.session_state.editing_item is not None
            if is_edit_mode:
                item = st.session_state.editing_item
                update_values = {'nome_especie': nome.strip(), 'pais_origem': origem.strip(),  
                                 'temperamento': temperamento.strip()}

                where = {'id': int(item['id'])}

                GenericRepository.update_table('especie_gatos', update_values, where)  
                st.toast(f"'{nome}' atualizado com sucesso!", icon="✅")  
            else:
                df = pd.DataFrame([{'nome_especie': nome.strip(), 'pais_origem': origem.strip(),
                                    'temperamento': temperamento.strip()}])

                GenericRepository.write_dataframe_to_table(df, 'especie_gatos')  
                st.toast(f"'{nome}' cadastrado com sucesso!", icon="🎉")

            self.close_form()
        except Exception as e:
            st.error(f"Erro ao salvar: {e}")

    def delete_item(self, item):
        try:
                                                            
            GenericRepository.delete_from_table('especie_gatos', {'id': item['id']})  
            st.toast(f"'{item['nome_especie']}' excluído!", icon="🗑️")
                                              
            st.rerun()                                                            
        except Exception as e:
            st.error(f"Erro ao excluir: {e}")

    def get_all_gatos(self):
        try:
                                              
            df = GenericRepository.read_table_to_dataframe('especie_gatos')

            return df   
        except Exception as e:
            st.error(f"Não foi possível carregar as espécies. Detalhe: {e}")
            return pd.DataFrame()