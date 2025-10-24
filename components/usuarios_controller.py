import streamlit as st
import pandas as pd
import config
from persistencia.repository import GenericRepository
from persistencia.auth import hash_password
from components.usuarios_view import UsuariosView

class UsuariosController:
    def __init__(self):
        self.view = UsuariosView(self)
        self._initialize_state()

    def _initialize_state(self):
        if "show_user_form" not in st.session_state:
            st.session_state.show_user_form = False
        if "editing_user_item" not in st.session_state:
            st.session_state.editing_user_item = None

    def run(self):
        if not config.DATABASE_ENABLED:
            st.title("👤 Gestão de Usuários")
            st.warning("Funcionalidade indisponível: O banco de dados está desabilitado.")
            return
        self.view.render()

    def open_form(self, item=None):
        st.session_state.editing_user_item = item
        st.session_state.show_user_form = True

    def close_form(self):
        st.session_state.show_user_form = False
        st.session_state.editing_user_item = None
        st.rerun()

    def save_item(self, form_data: dict, is_edit_mode: bool):
        try:
            login = form_data['login_usuario'].strip()
            nome = form_data['nome_completo'].strip()
            tipo_acesso = form_data['tipo_acesso']
            password = form_data['password']

            if not login or not nome:
                st.error("Os campos 'Login' e 'Nome Completo' são obrigatórios.")
                return

            if is_edit_mode:
                update_values = {
                    'nome_completo': nome,                  
                    'tipo_acesso': tipo_acesso                   
                }
                if password:
                    hashed_pw = hash_password(password)
                    update_values['senha_criptografada'] = hashed_pw

                where_conditions = {'login_usuario': login}

                GenericRepository.update_table("usuarios", update_values, where_conditions)
                st.toast(f"Usuário '{login}' atualizado com sucesso!", icon="✅")

            else:
                if not password:
                    st.error("A 'Senha' é obrigatória para novos usuários.")
                    return

                hashed_pw = hash_password(password)

                df = pd.DataFrame([{
                    'login_usuario': login,
                    'senha_criptografada': hashed_pw,
                    'nome_completo': nome,
                    'tipo_acesso': tipo_acesso
                }])

                GenericRepository.write_dataframe_to_table(df, "usuarios")
                st.toast(f"Usuário '{login}' criado com sucesso!", icon="🎉")

            self.close_form()

        except Exception as e:
            if "UNIQUE constraint failed" in str(e) or "Duplicate entry" in str(e) or "unique constraint" in str(e):
                st.error(f"Erro: O login '{login}' já existe. Tente outro.")
            else:
                st.error(f"Erro ao salvar: {e}")

    def delete_item(self, item: dict):
        try:
            login_to_delete = item['login_usuario']

            where_conditions = {'login_usuario': login_to_delete}

            GenericRepository.delete_from_table("usuarios", where_conditions)
            st.toast(f"Usuário '{login_to_delete}' excluído!", icon="🗑️")
            st.rerun()
        except Exception as e:
            st.error(f"Erro ao excluir: {e}")

    def get_all_users(self):
        try:
                                                    
            df = GenericRepository.read_table_to_dataframe("usuarios")
            if 'senha_criptografada' in df.columns:
                df = df.drop(columns=['senha_criptografada'])
            return df
        except Exception as e:
            st.error(f"Não foi possível carregar os usuários. Detalhe: {e}")
            return pd.DataFrame()