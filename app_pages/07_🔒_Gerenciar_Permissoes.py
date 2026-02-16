import streamlit as st
import pandas as pd
import logging
import time
from pathlib import Path
from components import servicos_gerenciador as servico
from utils.st_utils import st_check_session, check_access
from persistencia.unit_of_work import UnitOfWork
st.set_page_config(page_title='Gerenciar Permissões', layout='wide', page_icon='🔒')
st_check_session()
try:
    allowed_roles = servico.get_allowed_roles_for_page(Path(__file__).name)
    check_access(allowed_roles)
except Exception as e:
    st.error(f'Erro ao verificar permissões: {e}')
    st.stop()
log = logging.getLogger(__name__)

def load_data():
    with UnitOfWork() as uow:
        df_paginas = uow.permissoes.get_all_pages()
        df_perfis = uow.permissoes.get_all_profiles()
        mapa_permissoes = uow.permissoes.get_permissions_map()
    return (df_paginas, df_perfis, mapa_permissoes)

def build_permission_matrix(df_paginas, df_perfis, mapa_permissoes):
    matrix_df = df_paginas[['pagina_id', 'nome_amigavel']].copy()
    matrix_df = matrix_df.rename(columns={'nome_amigavel': 'Página'})
    for _, perfil in df_perfis.iterrows():
        perfil_id = perfil['perfil_id']
        perfil_nome = perfil['nome_perfil']
        matrix_df[perfil_nome] = matrix_df['pagina_id'].apply(lambda pagina_id: perfil_id in mapa_permissoes.get(pagina_id, []))
    return matrix_df

def save_permission_matrix(edited_matrix_df, df_perfis):
    try:
        perfil_lookup = dict(zip(df_perfis['nome_perfil'], df_perfis['perfil_id']))
        id_vars = ['pagina_id', 'Página']
        value_vars = [col for col in edited_matrix_df.columns if col not in id_vars]
        df_long = edited_matrix_df.melt(id_vars=id_vars, value_vars=value_vars, var_name='nome_perfil', value_name='tem_permissao')
        df_permissoes_concedidas = df_long[df_long['tem_permissao'] == True].copy()
        df_permissoes_concedidas['perfil_id'] = df_permissoes_concedidas['nome_perfil'].map(perfil_lookup)
        df_final_para_db = df_permissoes_concedidas[['pagina_id', 'perfil_id']].dropna().astype(int)
        with UnitOfWork() as uow:
            uow.permissoes.salvar_matriz_permissoes(df_final_para_db)
        st.balloons()
        st.toast('Alterações salvas com sucesso!', icon='✅')
        time.sleep(1.2)
        st.rerun()
    except Exception as e:
        log.error(f'Erro ao salvar: {e}')
        erro_str = str(e).lower()
        if 'constraint' in erro_str or 'foreign key' in erro_str:
            st.warning('Não foi possível remover algumas permissões pois existem registros dependentes (Restrição de Integridade).', icon='⚠️')
        else:
            st.error(f'Erro ao processar a solicitação: {e}')
st.title('🔒 Gerenciador de Permissões de Página')
st.markdown('Defina quais perfis de usuário podem acessar quais páginas.')
df_paginas, df_perfis, mapa_permissoes = load_data()
if df_paginas.empty:
    st.error('Tabela de páginas vazia.')
    st.stop()
matrix_df = build_permission_matrix(df_paginas, df_perfis, mapa_permissoes)
st.info('O perfil **Administrador Global** sempre tem acesso a tudo.', icon='ℹ️')
with st.form('matrix_form'):
    st.markdown('Marque as caixas para conceder permissão.')
    column_config = {'pagina_id': None, 'Página': st.column_config.TextColumn(label='Página', disabled=True, width='large')}
    for perfil_nome in df_perfis['nome_perfil']:
        column_config[perfil_nome] = st.column_config.CheckboxColumn(label=perfil_nome, width='medium')
    edited_df = st.data_editor(matrix_df, column_config=column_config, hide_index=True, key='permission_matrix')
    if st.form_submit_button('💾 Salvar Todas as Alterações', type='primary', use_container_width=True):
        save_permission_matrix(edited_df, df_perfis)