import streamlit as st
import pandas as pd
import config  # Para verificar se o BD está ativo
from persistencia.repository import GenericRepository  # Para acesso ao BD
from utils.st_utils import st_check_session, check_access  # Para segurança

# =============================================================================
# 1. CONFIGURAÇÃO DA PÁGINA E VERIFICAÇÃO DE ACESSO
# (Isso veio do seu arquivo 3_🐱_Gatos_CRUD.py)
# =============================================================================

st.set_page_config(page_title="Gerenciador de Gatos", layout="wide")

# Verifica se o usuário está logado e se tem permissão
st_check_session()
check_access([])  # Lista vazia significa que todos os logados podem ver

# Verifica se o banco de dados está habilitado no config.py
if not config.DATABASE_ENABLED:
    st.title("🐱 Gerenciador de Espécies de Gatos")
    st.warning("Funcionalidade indisponível: O banco de dados está desabilitado no arquivo de configuração.")
    st.stop()  # Para a execução da página aqui

# =============================================================================
# 2. INICIALIZAÇÃO DO ESTADO DA PÁGINA (st.session_state)
# (Isso veio do seu 'gatos_controller.py' -> _initialize_state)
#
# O 'st.session_state' é a "memória" da página. É aqui que guardamos
# informações importantes, como "o formulário está visível?" ou
# "qual item estamos editando?".
# =============================================================================

# Inicializa o estado para controlar a visibilidade do formulário
if "show_form" not in st.session_state:
    st.session_state.show_form = False

# Inicializa o estado para guardar os dados do item em edição
if "editing_item" not in st.session_state:
    st.session_state.editing_item = None

# =============================================================================
# 3. FUNÇÕES DE ACESSO AO BANCO DE DADOS (Lógica "Repository")
# (Estas funções substituem as chamadas diretas ao GenericRepository)
#
# Criamos funções "wrapper" simples para cada operação de CRUD.
# Isso torna o resto do código mais legível e fácil de replicar.
# Para outra tabela, você só precisaria copiar e alterar estas funções.
# =============================================================================

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

# =============================================================================
# 4. FUNÇÕES DE LÓGICA DE UI (Lógica "Controller")
# (Estas são as funções que os botões irão chamar - 'callbacks')
#
# Elas controlam o "estado" da página, como abrir ou fechar o formulário
# e processar os dados salvos.
# =============================================================================

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
        return  # Para a execução aqui e mantém o formulário aberto

    try:
        if st.session_state.editing_item:
            # MODO EDIÇÃO: Atualiza o item existente
            item_id = st.session_state.editing_item['id']
            update_gato(item_id, nome, origem, temperamento)
            st.toast(f"'{nome}' atualizado com sucesso!", icon="✅")
        else:
            # MODO ADIÇÃO: Cria um novo item
            add_gato(nome, origem, temperamento)
            st.toast(f"'{nome}' cadastrado com sucesso!", icon="🎉")

        # Se salvou com sucesso, fecha o formulário e recarrega a página
        close_form_and_rerun()

    except Exception as e:
        st.error(f"Erro ao salvar: {e}")

def handle_delete(item_data):
    """Processa o clique no botão 'Confirmar Exclusão'."""
    try:
        delete_gato(item_data['id'])
        st.toast(f"'{item_data['nome_especie']}' excluído!", icon="🗑️")
        st.rerun()  # Recarrega a página para remover o item da lista
    except Exception as e:
        st.error(f"Erro ao excluir: {e}")

# =============================================================================
# 5. FUNÇÕES DE RENDERIZAÇÃO DA INTERFACE (Lógica "View")
# (Estas funções desenham os widgets do Streamlit na tela)
# =============================================================================

def render_form():
    """Desenha o formulário de Adicionar/Editar."""
    is_edit_mode = st.session_state.editing_item is not None
    title = "✏️ Editando Espécie" if is_edit_mode else "➕ Adicionar Nova Espécie"
    item = st.session_state.editing_item or {}

    with st.container(border=True):
        st.subheader(title)
        with st.form(key="cat_form"):
            # Campos do formulário
            nome = st.text_input("Nome da Espécie", value=item.get("nome_especie", ""))
            origem = st.text_input("País de Origem", value=item.get("pais_origem", ""))
            temperamento = st.text_area("Temperamento", value=item.get("temperamento", ""))

            # Botões do formulário
            form_cols = st.columns(2)
            submitted = form_cols[0].form_submit_button("Salvar", type="primary", width='stretch')
            cancelled = form_cols[1].form_submit_button("Cancelar", width='stretch')

            if submitted:
                # Chama a função de lógica "handle_save"
                handle_save(nome, origem, temperamento)
            if cancelled:
                # Fecha o formulário e recarrega
                close_form_and_rerun()

def render_table():
    """Desenha a tabela com os dados e os botões de ação."""
    st.divider()
    df_gatos = get_all_gatos()

    if df_gatos.empty and not st.session_state.show_form:
        st.info("Nenhuma espécie cadastrada. Clique em 'Adicionar' para começar.")
        return

    # Cabeçalho da tabela
    header_cols = st.columns([3, 2, 3, 1, 1])
    header_cols[0].markdown("**Nome da Espécie**")
    header_cols[1].markdown("**País de Origem**")
    header_cols[2].markdown("**Temperamento**")
    header_cols[3].markdown("**Ações**", help="Editar / Excluir")

    # Linhas da tabela
    for index, row in df_gatos.iterrows():
        row_data = row.to_dict()
        row_cols = st.columns([3, 2, 3, 1, 1])

        row_cols[0].write(row_data['nome_especie'])
        row_cols[1].write(row_data['pais_origem'])
        row_cols[2].write(row_data['temperamento'])

        # Botão Editar
        row_cols[3].button(
            "✏️",
            key=f"edit_{row_data['id']}",
            on_click=show_edit_form,  # Chama a função de lógica
            args=(row_data,)
        )

        # Botão Excluir (com pop-up de confirmação)
        popover = row_cols[4].popover("🗑️")
        popover.warning(f"Excluir '{row_data['nome_especie']}'?")
        popover.button(
            "Confirmar Exclusão",
            key=f"del_{row_data['id']}",
            on_click=handle_delete,  # Chama a função de lógica
            args=(row_data,)
        )

# =============================================================================
# 6. EXECUÇÃO PRINCIPAL DA PÁGINA
# (Este é o "cérebro" que decide o que mostrar)
# (Este é o "cérebro" que decide o que mostrar)
# =============================================================================

st.title("🐱 Gerenciador de Espécies de Gatos")
st.markdown("Use a tabela abaixo para visualizar, editar ou excluir espécies.")

# Lógica principal: ou mostra o formulário, ou mostra o botão "Adicionar"
if st.session_state.show_form:
    render_form()
else:
    st.button(
        "➕ Adicionar Nova Espécie",
        on_click=show_add_form,  # Chama a função de lógica
        type="primary"
    )

# A tabela é sempre renderizada
render_table()