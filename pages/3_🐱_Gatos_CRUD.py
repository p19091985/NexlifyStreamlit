import streamlit as st
import pandas as pd
import config
from persistencia.repository import GenericRepository
from utils.st_utils import st_check_session, check_access

st.set_page_config(page_title="Gerenciador de Gatos", layout="wide")

st_check_session()
check_access([])

if not config.DATABASE_ENABLED:
    st.title("🐱 Gerenciador de Espécies de Gatos")
    st.warning("Funcionalidade indisponível: O banco de dados está desabilitado no arquivo de configuração.")
    st.stop()

if "show_form" not in st.session_state:
    st.session_state.show_form = False

if "editing_item" not in st.session_state:
    st.session_state.editing_item = None

def get_all_gatos():
    """Busca todas as espécies de gatos no banco de dados."""
    try:
        df = GenericRepository.read_table_to_dataframe('especie_gatos')
        return df
    except Exception as e:
        st.error(f"Não foi possível carregar as espécies. Detalhe: {e}")
        return pd.DataFrame()

def add_gato(nome, origem, temperamento):
    """Adiciona uma nova espécie de gato ao banco de dados."""
    df = pd.DataFrame([{'nome_especie': nome.strip(),
                        'pais_origem': origem.strip(),
                        'temperamento': temperamento.strip()}])
    GenericRepository.write_dataframe_to_table(df, 'especie_gatos')

def update_gato(item_id, nome, origem, temperamento):
    """Atualiza uma espécie de gato existente no banco de dados."""
    update_values = {'nome_especie': nome.strip(),
                     'pais_origem': origem.strip(),
                     'temperamento': temperamento.strip()}
    where_conditions = {'id': int(item_id)}
    GenericRepository.update_table('especie_gatos', update_values, where_conditions)

def delete_gato(item_id):
    """Exclui uma espécie de gato do banco de dados."""
    where_conditions = {'id': int(item_id)}
    GenericRepository.delete_from_table('especie_gatos', where_conditions)

def show_add_form():
    """Ativa o modo "Adicionar", mostrando o formulário vazio."""
    st.session_state.show_form = True
    st.session_state.editing_item = None

def show_edit_form(item_data):
    """Ativa o modo "Editar", mostrando o formulário preenchido."""
    st.session_state.show_form = True
    st.session_state.editing_item = item_data

def close_form_and_rerun():
    """Fecha o formulário e recarrega a página."""
    st.session_state.show_form = False
    st.session_state.editing_item = None
    st.rerun()

def handle_save(nome, origem, temperamento):
    """Processa o clique no botão 'Salvar' do formulário."""
    if not nome.strip():
        st.error("O nome da espécie é obrigatório.")
        return

    try:
        if st.session_state.editing_item:
            item_id = st.session_state.editing_item['id']
            update_gato(item_id, nome, origem, temperamento)
            st.toast(f"'{nome}' atualizado com sucesso!", icon="✅")
        else:
            add_gato(nome, origem, temperamento)
            st.toast(f"'{nome}' cadastrado com sucesso!", icon="🎉")

        close_form_and_rerun()

    except Exception as e:
        st.error(f"Erro ao salvar: {e}")

def handle_delete(item_data):
    """Processa o clique no botão 'Confirmar Exclusão'."""
    try:
        delete_gato(item_data['id'])
        st.toast(f"'{item_data['nome_especie']}' excluído!", icon="🗑️")
        st.rerun()
    except Exception as e:
        st.error(f"Erro ao excluir: {e}")

def render_form():
    """Desenha o formulário de Adicionar/Editar."""
    is_edit_mode = st.session_state.editing_item is not None
    title = "✏️ Editando Espécie" if is_edit_mode else "➕ Adicionar Nova Espécie"
    item = st.session_state.editing_item or {}

    with st.container(border=True):
        st.subheader(title)
        with st.form(key="cat_form"):
            nome = st.text_input("Nome da Espécie", value=item.get("nome_especie", ""))
            origem = st.text_input("País de Origem", value=item.get("pais_origem", ""))
            temperamento = st.text_area("Temperamento", value=item.get("temperamento", ""))

            form_cols = st.columns(2)
            submitted = form_cols[0].form_submit_button("Salvar", type="primary", width='stretch')
            cancelled = form_cols[1].form_submit_button("Cancelar", width='stretch')

            if submitted:
                handle_save(nome, origem, temperamento)
            if cancelled:
                close_form_and_rerun()

def render_table():
    """Desenha a tabela com os dados e os botões de ação."""
    st.divider()
    df_gatos = get_all_gatos()

    if df_gatos.empty and not st.session_state.show_form:
        st.info("Nenhuma espécie cadastrada. Clique em 'Adicionar' para começar.")
        return

    header_cols = st.columns([3, 2, 3, 1, 1])
    header_cols[0].markdown("**Nome da Espécie**")
    header_cols[1].markdown("**País de Origem**")
    header_cols[2].markdown("**Temperamento**")
    header_cols[3].markdown("**Ações**", help="Editar / Excluir")

    for index, row in df_gatos.iterrows():
        row_data = row.to_dict()
        row_cols = st.columns([3, 2, 3, 1, 1])

        row_cols[0].write(row_data['nome_especie'])
        row_cols[1].write(row_data['pais_origem'])
        row_cols[2].write(row_data['temperamento'])

        row_cols[3].button(
            "✏️",
            key=f"edit_{row_data['id']}",
            on_click=show_edit_form,
            args=(row_data,)
        )

        popover = row_cols[4].popover("🗑️")
        popover.warning(f"Excluir '{row_data['nome_especie']}'?")
        popover.button(
            "Confirmar Exclusão",
            key=f"del_{row_data['id']}",
            on_click=handle_delete,
            args=(row_data,)
        )

st.title("🐱 Gerenciador de Espécies de Gatos")
st.markdown("Use a tabela abaixo para visualizar, editar ou excluir espécies.")

if st.session_state.show_form:
    render_form()
else:
    st.button(
        "➕ Adicionar Nova Espécie",
        on_click=show_add_form,
        type="primary"
    )

render_table()