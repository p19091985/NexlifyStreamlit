import streamlit as st
import pandas as pd
import config
from persistencia.repository import GenericRepository
from persistencia.data_service import DataService
from components.vegetais_auditoria_view import VegetaisAuditoriaView


class VegetaisAuditoriaController:
    def __init__(self):
        self.view = VegetaisAuditoriaView(self)
        self._initialize_state()

    def _initialize_state(self):
        """Inicializa as variáveis de estado da sessão para este painel."""
        if "veg_show_tipo_form" not in st.session_state:  
            st.session_state.veg_show_tipo_form = False  
        if "veg_editing_tipo_item" not in st.session_state:  
            st.session_state.veg_editing_tipo_item = None  

    def run(self):
        """Renderiza a view principal."""

        if not config.DATABASE_ENABLED:
            st.title("🌿 Vegetais e Auditoria")
            st.warning("Funcionalidade indisponível: O banco de dados está desabilitado no arquivo de configuração.")  
            return

        self.view.render()

    def open_tipo_form(self, item=None):
        """Abre o formulário para criar/editar um Tipo de Vegetal."""
        st.session_state.veg_editing_tipo_item = item
        st.session_state.veg_show_tipo_form = True
                                                                        

    def close_tipo_form(self):
        """Fecha o formulário de Tipo de Vegetal."""
        st.session_state.veg_show_tipo_form = False  
        st.session_state.veg_editing_tipo_item = None  
        st.rerun()                                                                                   

    def save_vegetal(self, nome, tipo_nome):
        """Salva um vegetal (novo ou existente)."""
                                                                                           
        if not nome or not tipo_nome:
            st.error("Os campos 'Nome' e 'Tipo' são obrigatórios.")
            return

        try:
                                            
            df_tipo = GenericRepository.read_table_to_dataframe("tipos_vegetais", where_conditions={'nome': tipo_nome})  
            if df_tipo.empty:
                st.error(f"O tipo '{tipo_nome}' não foi encontrado.")
                return

            id_tipo = int(df_tipo.iloc[0]['id'])  
                                            
            data = {'nome': nome, 'id_tipo': id_tipo}  

            GenericRepository.write_dataframe_to_table(pd.DataFrame([data]), "vegetais")
            st.toast(f"Vegetal '{nome}' cadastrado com sucesso!", icon="🎉")
            st.rerun()                                                 
        except Exception as e:
            st.error(f"Não foi possível salvar o registro: {e}")

    def save_tipo_vegetal(self, nome):
        """Salva um tipo de vegetal (novo ou editado)."""  
        if not nome:
            st.error("O nome do tipo é obrigatório.")
            return

        try:
            is_edit = st.session_state.veg_editing_tipo_item is not None
            if is_edit:
                item_id = st.session_state.veg_editing_tipo_item['id']  
                                                
                GenericRepository.update_table("tipos_vegetais", {'nome': nome}, {'id': item_id})  
                st.toast(f"Tipo '{nome}' atualizado!", icon="✅")
            else:
                                                  
                df = pd.DataFrame([{'nome': nome}])  
                GenericRepository.write_dataframe_to_table(df, "tipos_vegetais")  
                st.toast(f"Tipo '{nome}' criado!", icon="🎉")

            self.close_tipo_form()                            
                                                                       
        except Exception as e:
            st.error(f"Erro ao salvar o tipo: {e}")  

    def delete_tipo_vegetal(self, item):
        """Exclui um tipo de vegetal."""
        try:
                                            
            GenericRepository.delete_from_table("tipos_vegetais", {'id': item['id']})  
            st.toast(f"Tipo '{item['nome']}' excluído!", icon="🗑️")
                                              
            st.rerun()                                                            
        except Exception as e:
            st.error(f"Não foi possível excluir. O tipo pode estar em uso. Detalhe: {e}")  

    def executar_reclassificacao(self, vegetal_selecionado, novo_tipo_nome):
        """Executa a transação de reclassificação de um vegetal."""
        if not vegetal_selecionado or not novo_tipo_nome:
            st.warning("Selecione um vegetal e um novo tipo para reclassificar.")
            return

        nome_vegetal = vegetal_selecionado.split(' (ID:')[0]
        usuario = st.session_state.user_info['username']

        sucesso, mensagem = DataService.reclassificar_vegetal_e_logar(nome_vegetal, novo_tipo_nome, usuario)  

        if sucesso:
            st.toast(mensagem, icon="✅")
                                              
            st.rerun()                                                          
        else:
            st.error(mensagem)

    def get_all_tipos(self):
        return GenericRepository.read_table_to_dataframe("tipos_vegetais")

    def get_all_vegetais(self):
        return GenericRepository.read_vegetais_com_tipo()

    def get_all_logs(self):  
        df = GenericRepository.read_table_to_dataframe("log_alteracoes")
        if not df.empty and 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df = df.sort_values(by='timestamp', ascending=False)
                                               
            df['timestamp'] = df['timestamp'].dt.strftime('%d/%m/%Y %H:%M:%S')
        return df