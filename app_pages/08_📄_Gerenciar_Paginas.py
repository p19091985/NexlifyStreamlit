import streamlit as st
import pandas as pd
import config
from persistencia.unit_of_work import UnitOfWork
from utils.st_utils import st_check_session, check_access
from pathlib import Path
from components import servicos_gerenciador as servico
st.set_page_config(page_title='Gerenciar Páginas', layout='wide', page_icon='📄')
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
if 'pag_show_form' not in st.session_state:
    st.session_state.pag_show_form = False
if 'pag_editing' not in st.session_state:
    st.session_state.pag_editing = None
st.title('📄 Gerenciador de Páginas do Sistema')
st.markdown('Cadastre aqui os arquivos `.py` que compõem o sistema para gerenciar as permissões posteriormente.')
c1, c2 = st.columns([4, 1])
c1.subheader('Lista de Páginas Cadastradas')
if c2.button('➕ Nova Página', width='stretch'):
    st.session_state.pag_show_form = True
    st.session_state.pag_editing = None
    st.rerun()
with UnitOfWork() as uow:
    df = uow.paginas.get_all_paginas()
if st.session_state.pag_show_form:
    item = st.session_state.pag_editing
    with st.container(border=True):
        st.markdown(f'### 📝 {('Editar' if item else 'Nova')} Página')
        with st.form('form_pag'):
            c_a, c_b = st.columns([1, 1])
            nome_arquivo = c_a.text_input('Nome do Arquivo (ex: 1_Home.py)', value=item['nome_arquivo'] if item else '')
            nome_amigavel = c_b.text_input('Nome Amigável (Menu)', value=item['nome_amigavel'] if item else '')
            b1, b2 = st.columns(2)
            if b1.form_submit_button('💾 Salvar', type='primary', width='stretch'):
                if not nome_arquivo or not nome_amigavel:
                    st.error('Todos os campos são obrigatórios.')
                else:
                    try:
                        with UnitOfWork() as uow:
                            uow.paginas.salvar_pagina({'nome_arquivo': nome_arquivo, 'nome_amigavel': nome_amigavel}, item['pagina_id'] if item else None)
                        st.toast('Salvo com sucesso!', icon='✅')
                        st.session_state.pag_show_form = False
                        st.rerun()
                    except Exception as e:
                        if 'UNIQUE constraint failed' in str(e):
                            st.error('Erro: Já existe uma página cadastrada com este nome de arquivo.')
                        else:
                            st.error(f'Erro ao salvar: {e}')
            if item:
                if b2.form_submit_button('🗑️ Excluir', type='secondary', width='stretch'):
                    try:
                        with UnitOfWork() as uow:
                            uow.paginas.excluir_pagina(item['pagina_id'])
                        st.toast('Excluído com sucesso!', icon='🗑️')
                        st.session_state.pag_show_form = False
                        st.rerun()
                    except Exception as e:
                        st.error(f'Erro ao excluir (verifique se há permissões vinculadas): {e}')
            elif b2.form_submit_button('Cancelar', width='stretch'):
                st.session_state.pag_show_form = False
                st.rerun()
if df.empty:
    st.info('Nenhuma página cadastrada.')
else:
    col_config = {'pagina_id': st.column_config.NumberColumn('ID', width='small'), 'nome_arquivo': st.column_config.TextColumn('Nome do Arquivo', width='medium'), 'nome_amigavel': st.column_config.TextColumn('Nome no Menu', width='medium')}
    event = st.dataframe(df, width='stretch', hide_index=True, on_select='rerun', selection_mode='single-row', column_config=col_config, column_order=['pagina_id', 'nome_amigavel', 'nome_arquivo'])
    if event.selection.rows:
        idx = event.selection.rows[0]
        row = df.iloc[idx].to_dict()
        if not st.session_state.pag_show_form or st.session_state.pag_editing != row:
            st.session_state.pag_editing = row
            st.session_state.pag_show_form = True
            st.rerun()