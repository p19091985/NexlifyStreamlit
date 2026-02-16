import streamlit as st
import pandas as pd
import config
import logging
import time
from pathlib import Path
from persistencia.auth import hash_password
from persistencia.unit_of_work import UnitOfWork
from utils.st_utils import st_check_session, check_access
from streamlit_option_menu import option_menu
from components import servicos_gerenciador as servico
st.set_page_config(page_title='Gestão de Usuários', layout='wide', page_icon='👤')
log = logging.getLogger(__name__)
st_check_session()
try:
    allowed_roles = servico.get_allowed_roles_for_page(Path(__file__).name)
    check_access(allowed_roles)
except Exception as e:
    st.error(f'Erro ao verificar permissões: {e}')
    st.stop()
if not config.DATABASE_ENABLED:
    st.warning('Banco de dados desabilitado.')
    st.stop()
if 'user_show_form' not in st.session_state:
    st.session_state.user_show_form = False
if 'user_editing' not in st.session_state:
    st.session_state.user_editing = None
if 'perfil_show_form' not in st.session_state:
    st.session_state.perfil_show_form = False
if 'perfil_editing' not in st.session_state:
    st.session_state.perfil_editing = None
if 'feedback_msg' not in st.session_state:
    st.session_state.feedback_msg = None

def mostrar_feedback():
    if st.session_state.feedback_msg:
        tipo = st.session_state.feedback_msg.get('tipo')
        texto = st.session_state.feedback_msg.get('texto')
        if tipo == 'sucesso':
            st.success(texto, icon='✅')
        elif tipo == 'erro':
            st.error(texto, icon='❌')
        elif tipo == 'aviso':
            st.warning(texto, icon='⚠️')
st.title('👤 Gestão de Usuários e Perfis')
selected_tab = option_menu(None, options=['Gerenciar Usuários', 'Gerenciar Perfis de Acesso'], icons=['person-fill-gear', 'shield-lock-fill'], orientation='horizontal')
if selected_tab == 'Gerenciar Usuários':
    c1, c2 = st.columns([4, 1])
    c1.caption('Clique em uma linha para editar.')
    if c2.button('➕ Novo Usuário', width='stretch'):
        st.session_state.user_show_form = True
        st.session_state.user_editing = None
        st.session_state.feedback_msg = None
        st.rerun()
    with UnitOfWork() as uow:
        df_users = uow.usuarios.get_all_users_detailed()
        df_perfis_ref = uow.usuarios.get_all_perfis()
    perfis_map = dict(zip(df_perfis_ref['perfil_id'], df_perfis_ref['nome_perfil']))
    if st.session_state.user_show_form:
        item = st.session_state.user_editing
        with st.container(border=True):
            st.markdown(f'### 📝 {('Editar' if item else 'Novo')} Usuário')
            mostrar_feedback()
            with st.form('form_user'):
                c_a, c_b = st.columns(2)
                login = c_a.text_input('Login', value=item['login_usuario'] if item else '')
                nome = c_b.text_input('Nome', value=item['nome_completo'] if item else '')
                c_c, c_d = st.columns(2)
                idx_perfil = 0
                if item and item['perfil_id'] in perfis_map:
                    try:
                        idx_perfil = list(perfis_map.keys()).index(item['perfil_id'])
                    except ValueError:
                        idx_perfil = 0
                perfil_id = c_c.selectbox('Perfil', options=list(perfis_map.keys()), format_func=lambda x: perfis_map[x], index=idx_perfil)
                senha = c_d.text_input('Senha', type='password', placeholder='Vazio para manter atual' if item else 'Obrigatória')
                b1, b2 = st.columns(2)
                if b1.form_submit_button('💾 Salvar', type='primary', width='stretch'):
                    try:
                        data = {'login_usuario': login, 'nome_completo': nome, 'perfil_id': perfil_id}
                        if senha:
                            data['senha_criptografada'] = hash_password(senha)
                        elif not item:
                            st.session_state.feedback_msg = {'tipo': 'erro', 'texto': 'Senha é obrigatória para novos usuários.'}
                            st.rerun()
                        with UnitOfWork() as uow:
                            uow.usuarios.salvar_usuario(data, item['usuario_id'] if item else None)
                        st.balloons()
                        st.toast('Usuário salvo com sucesso!', icon='✅')
                        st.session_state.user_show_form = False
                        st.session_state.feedback_msg = None
                        time.sleep(1.2)
                        st.rerun()
                    except Exception as e:
                        log.error(f'Erro ao salvar usuário: {e}')
                        msg = 'Erro: Já existe um usuário com este Login.' if 'unique' in str(e).lower() else f'Erro técnico: {e}'
                        st.session_state.feedback_msg = {'tipo': 'erro', 'texto': msg}
                        st.rerun()
                if item and b2.form_submit_button('🗑️ Excluir', type='secondary', width='stretch'):
                    try:
                        with UnitOfWork() as uow:
                            uow.usuarios.excluir_usuario(item['usuario_id'])
                        st.balloons()
                        st.toast('Usuário excluído com sucesso!', icon='🗑️')
                        st.session_state.user_show_form = False
                        st.session_state.feedback_msg = None
                        time.sleep(1.2)
                        st.rerun()
                    except Exception as e:
                        erro_str = str(e).lower()
                        if 'constraint' in erro_str or 'foreign key' in erro_str or 'integrityerror' in erro_str:
                            st.session_state.feedback_msg = {'tipo': 'aviso', 'texto': 'Não é possível excluir este usuário pois ele possui registros vinculados (histórico, configurações, etc).'}
                        else:
                            st.session_state.feedback_msg = {'tipo': 'erro', 'texto': f'Erro técnico ao excluir: {e}'}
                        st.rerun()
                elif not item and b2.form_submit_button('Cancelar'):
                    st.session_state.user_show_form = False
                    st.session_state.feedback_msg = None
                    st.rerun()
    event = st.dataframe(df_users, width='stretch', hide_index=True, on_select='rerun', selection_mode='single-row', column_config={'usuario_id': None, 'perfil_id': None, 'login_usuario': 'Login', 'nome_completo': 'Nome', 'nome_perfil': 'Perfil'})
    if event.selection.rows:
        idx = event.selection.rows[0]
        selected_row_data = df_users.iloc[idx].to_dict()
        current_id = st.session_state.user_editing['usuario_id'] if st.session_state.user_editing else None
        new_id = selected_row_data['usuario_id']
        if current_id != new_id:
            st.session_state.user_editing = selected_row_data
            st.session_state.user_show_form = True
            st.session_state.feedback_msg = None
            st.rerun()
elif selected_tab == 'Gerenciar Perfis de Acesso':
    c1, c2 = st.columns([4, 1])
    c1.caption('Gestão de Perfis')
    if c2.button('➕ Novo Perfil', width='stretch'):
        st.session_state.perfil_show_form = True
        st.session_state.perfil_editing = None
        st.session_state.feedback_msg = None
        st.rerun()
    with UnitOfWork() as uow:
        df_perfis = uow.usuarios.get_all_perfis()
    if st.session_state.perfil_show_form:
        item = st.session_state.perfil_editing
        with st.container(border=True):
            mostrar_feedback()
            with st.form('form_perfil'):
                nome_perfil = st.text_input('Nome do Perfil', value=item['nome_perfil'] if item else '')
                b1, b2 = st.columns(2)
                if b1.form_submit_button('💾 Salvar', type='primary', width='stretch'):
                    try:
                        with UnitOfWork() as uow:
                            uow.usuarios.salvar_perfil({'nome_perfil': nome_perfil}, item['perfil_id'] if item else None)
                        st.balloons()
                        st.toast('Perfil salvo com sucesso!', icon='✅')
                        st.session_state.perfil_show_form = False
                        st.session_state.feedback_msg = None
                        time.sleep(1.2)
                        st.rerun()
                    except Exception as e:
                        st.session_state.feedback_msg = {'tipo': 'erro', 'texto': f'Erro ao salvar: {e}'}
                        st.rerun()
                if item and b2.form_submit_button('🗑️ Excluir', type='secondary', width='stretch'):
                    try:
                        with UnitOfWork() as uow:
                            uow.usuarios.excluir_perfil(item['perfil_id'])
                        st.balloons()
                        st.toast('Perfil excluído com sucesso!', icon='🗑️')
                        st.session_state.perfil_show_form = False
                        st.session_state.feedback_msg = None
                        time.sleep(1.2)
                        st.rerun()
                    except Exception as e:
                        erro_str = str(e).lower()
                        if 'constraint' in erro_str or 'foreign key' in erro_str or 'integrityerror' in erro_str:
                            st.session_state.feedback_msg = {'tipo': 'aviso', 'texto': 'Não é possível excluir este perfil pois existem usuários vinculados.'}
                        else:
                            st.session_state.feedback_msg = {'tipo': 'erro', 'texto': f'Erro técnico: {e}'}
                        st.rerun()
                elif not item and b2.form_submit_button('Cancelar'):
                    st.session_state.perfil_show_form = False
                    st.session_state.feedback_msg = None
                    st.rerun()
    event = st.dataframe(df_perfis, width='stretch', hide_index=True, on_select='rerun', selection_mode='single-row', column_config={'perfil_id': None})
    if event.selection.rows:
        idx = event.selection.rows[0]
        selected_row_data = df_perfis.iloc[idx].to_dict()
        current_id = st.session_state.perfil_editing['perfil_id'] if st.session_state.perfil_editing else None
        new_id = selected_row_data['perfil_id']
        if current_id != new_id:
            st.session_state.perfil_editing = selected_row_data
            st.session_state.perfil_show_form = True
            st.session_state.feedback_msg = None
            st.rerun()