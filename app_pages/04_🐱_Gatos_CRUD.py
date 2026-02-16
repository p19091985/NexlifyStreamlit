import streamlit as st
import pandas as pd
import config
import logging
import time
from pathlib import Path
from persistencia.unit_of_work import UnitOfWork
from utils.st_utils import st_check_session, check_access
from components import servicos_gerenciador as servico
st.set_page_config(page_title='Gerenciador de Gatos', layout='wide', page_icon='🐱')
log = logging.getLogger(__name__)
st_check_session()
try:
    allowed_roles = servico.get_allowed_roles_for_page(Path(__file__).name)
    check_access(allowed_roles)
except Exception as e:
    st.error(f'Erro ao verificar permissões: {e}')
    st.stop()
if not config.DATABASE_ENABLED:
    st.title('🐱 Gerenciador de Espécies de Gatos')
    st.warning('Funcionalidade indisponível: O banco de dados está desabilitado no arquivo de configuração.')
    st.stop()
if 'cat_show_form' not in st.session_state:
    st.session_state.cat_show_form = False
if 'cat_editing' not in st.session_state:
    st.session_state.cat_editing = None
if 'cat_feedback_msg' not in st.session_state:
    st.session_state.cat_feedback_msg = None

def mostrar_feedback():
    if st.session_state.cat_feedback_msg:
        tipo = st.session_state.cat_feedback_msg.get('tipo')
        texto = st.session_state.cat_feedback_msg.get('texto')
        if tipo == 'sucesso':
            st.success(texto, icon='✅')
        elif tipo == 'erro':
            st.error(texto, icon='❌')
        elif tipo == 'aviso':
            st.warning(texto, icon='⚠️')

def get_all_gatos():
    try:
        with UnitOfWork() as uow:
            return uow.gatos.get_all_gatos()
    except Exception as e:
        log.error(f'Erro ao carregar gatos: {e}')
        return pd.DataFrame()
st.title('🐱 Gerenciador de Espécies de Gatos')
st.markdown('Use a tabela abaixo para visualizar, editar ou excluir espécies.')
c1, c2 = st.columns([4, 1])
c1.caption('Clique em uma linha para editar.')
if c2.button('➕ Nova Espécie', width='stretch'):
    st.session_state.cat_show_form = True
    st.session_state.cat_editing = None
    st.session_state.cat_feedback_msg = None
    st.rerun()
df_gatos = get_all_gatos()
if st.session_state.cat_show_form:
    item = st.session_state.cat_editing
    with st.container(border=True):
        st.markdown(f'### 📝 {('Editar' if item else 'Nova')} Espécie')
        mostrar_feedback()
        with st.form('form_cat'):
            c_a, c_b = st.columns(2)
            nome = c_a.text_input('Nome da Espécie', value=item['nome_especie'] if item else '')
            origem = c_b.text_input('País de Origem', value=item['pais_origem'] if item else '')
            temperamento = st.text_area('Temperamento', value=item['temperamento'] if item else '')
            b1, b2 = st.columns(2)
            if b1.form_submit_button('💾 Salvar', type='primary', width='stretch'):
                if not nome.strip():
                    st.session_state.cat_feedback_msg = {'tipo': 'erro', 'texto': 'O nome da espécie é obrigatório.'}
                    st.rerun()
                else:
                    try:
                        data = {'nome_especie': nome.strip(), 'pais_origem': origem.strip(), 'temperamento': temperamento.strip()}
                        with UnitOfWork() as uow:
                            item_id = int(item['id']) if item else None
                            uow.gatos.save_gato(data, item_id)
                        st.balloons()
                        st.toast('Espécie salva com sucesso!', icon='✅')
                        st.session_state.cat_show_form = False
                        st.session_state.cat_feedback_msg = None
                        time.sleep(1.2)
                        st.rerun()
                    except Exception as e:
                        log.error(f'Erro ao salvar espécie: {e}')
                        msg = 'Erro: Já existe uma espécie com este nome.' if 'unique' in str(e).lower() else f'Erro técnico: {e}'
                        st.session_state.cat_feedback_msg = {'tipo': 'erro', 'texto': msg}
                        st.rerun()
            if item and b2.form_submit_button('🗑️ Excluir', type='secondary', width='stretch'):
                try:
                    with UnitOfWork() as uow:
                        uow.gatos.delete_gato(int(item['id']))
                    st.balloons()
                    st.toast('Espécie excluída com sucesso!', icon='🗑️')
                    st.session_state.cat_show_form = False
                    st.session_state.cat_feedback_msg = None
                    time.sleep(1.2)
                    st.rerun()
                except Exception as e:
                    st.session_state.cat_feedback_msg = {'tipo': 'erro', 'texto': f'Erro ao excluir: {e}'}
                    st.rerun()
            elif not item and b2.form_submit_button('Cancelar'):
                st.session_state.cat_show_form = False
                st.session_state.cat_feedback_msg = None
                st.rerun()
if not df_gatos.empty:
    event = st.dataframe(df_gatos, width='stretch', hide_index=True, on_select='rerun', selection_mode='single-row', column_config={'id': None, 'nome_especie': 'Nome da Espécie', 'pais_origem': 'País de Origem', 'temperamento': 'Temperamento'})
    if event.selection.rows:
        idx = event.selection.rows[0]
        selected_row_data = df_gatos.iloc[idx].to_dict()
        current_id = st.session_state.cat_editing['id'] if st.session_state.cat_editing else None
        new_id = selected_row_data['id']
        if current_id != new_id:
            st.session_state.cat_editing = selected_row_data
            st.session_state.cat_show_form = True
            st.session_state.cat_feedback_msg = None
            st.rerun()
elif not st.session_state.cat_show_form:
    st.info('Nenhuma espécie cadastrada. Clique em "➕ Nova Espécie" para começar.')