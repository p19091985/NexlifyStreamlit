import streamlit as st
import pandas as pd
import config  # Para verificar se o BD está ativo
from persistencia.repository import GenericRepository  # Para acesso ao BD
from persistencia.auth import hash_password  # Para criptografar senhas
from utils.st_utils import st_check_session, check_access  # Para segurança

# =============================================================================
# 1. CONFIGURAÇÃO DA PÁGINA E VERIFICAÇÃO DE ACESSO
# (Isso veio do seu arquivo 6_👤_Gestao_Usuarios.py)
# =============================================================================

st.set_page_config(page_title="Gestão de Usuários", layout="wide")

# Verifica se o usuário está logado e se tem permissão
st_check_session()
check_access(['Administrador Global', 'Gerente de TI'])

# Verifica se o banco de dados está habilitado no config.py
if not config.DATABASE_ENABLED:
    st.title("👤 Gestão de Usuários")
    st.warning("Funcionalidade indisponível: O banco de dados está desabilitado.")
    st.stop()  # Para a execução da página aqui

# Constante com os perfis de acesso (veio de usuarios_view.py)
PERFIS_DE_ACESSO = [
    'Administrador Global',
    'Diretor de Operações',
    'Gerente de TI',
    'Supervisor de Produção',
    'Operador de Linha',
    'Analista de Dados',
    'Auditor Externo'
]

# =============================================================================
# 2. INICIALIZAÇÃO DO ESTADO DA PÁGINA (st.session_state)
# (Isso veio do seu 'usuarios_controller.py' -> _initialize_state)
#
# O 'st.session_state' é a "memória" da página.
# =============================================================================

# Inicializa o estado para controlar a visibilidade do formulário
if "show_user_form" not in st.session_state:
    st.session_state.show_user_form = False

# Inicializa o estado para guardar os dados do usuário em edição
if "editing_user_item" not in st.session_state:
    st.session_state.editing_user_item = None

# =============================================================================
# 3. FUNÇÕES DE ACESSO AO BANCO DE DADOS (Lógica "Repository")
# (Estas funções simplificam as chamadas ao GenericRepository)
# =============================================================================

def get_all_users():
    """Busca todos os usuários no banco, removendo a senha."""
    try:
        df = GenericRepository.read_table_to_dataframe("usuarios")
        # Remove a coluna da senha por segurança antes de exibir
        if 'senha_criptografada' in df.columns:
            df = df.drop(columns=['senha_criptografada'])
        return df
    except Exception as e:
        st.error(f"Não foi possível carregar os usuários. Detalhe: {e}")
        return pd.DataFrame()

def add_user(login, nome, tipo_acesso, password):
    """Adiciona um novo usuário ao banco de dados."""
    hashed_pw = hash_password(password)
    df = pd.DataFrame([{
        'login_usuario': login,
        'senha_criptografada': hashed_pw,
        'nome_completo': nome,
        'tipo_acesso': tipo_acesso
    }])
    GenericRepository.write_dataframe_to_table(df, "usuarios")

def update_user(login, nome, tipo_acesso, password):
    """Atualiza um usuário existente no banco de dados."""
    update_values = {
        'nome_completo': nome,
        'tipo_acesso': tipo_acesso
    }
    # Só atualiza a senha se uma nova for fornecida
    if password:
        hashed_pw = hash_password(password)
        update_values['senha_criptografada'] = hashed_pw

    where_conditions = {'login_usuario': login}
    GenericRepository.update_table("usuarios", update_values, where_conditions)

def delete_user(login):
    """Exclui um usuário do banco de dados."""
    where_conditions = {'login_usuario': login}
    GenericRepository.delete_from_table("usuarios", where_conditions)

# =============================================================================
# 4. FUNÇÕES DE LÓGICA DE UI (Lógica "Controller")
# (Estas são as funções que os botões irão chamar - 'callbacks')
# =============================================================================

def show_add_form():
    """Ativa o modo "Adicionar", mostrando o formulário vazio."""
    st.session_state.show_user_form = True
    st.session_state.editing_user_item = None

def show_edit_form(item_data):
    """Ativa o modo "Editar", mostrando o formulário preenchido."""
    st.session_state.show_user_form = True
    st.session_state.editing_user_item = item_data

def close_form_and_rerun():
    """Fecha o formulário e recarrega a página."""
    st.session_state.show_user_form = False
    st.session_state.editing_user_item = None
    st.rerun()

def handle_save(form_data: dict):
    """Processa o clique no botão 'Salvar' do formulário."""
    login = form_data['login_usuario'].strip()
    nome = form_data['nome_completo'].strip()
    tipo_acesso = form_data['tipo_acesso']
    password = form_data['password']  # Não usamos .strip() em senhas

    # Validação
    if not login or not nome:
        st.error("Os campos 'Login' e 'Nome Completo' são obrigatórios.")
        return  # Para a execução aqui e mantém o formulário aberto

    is_edit_mode = st.session_state.editing_user_item is not None

    if not is_edit_mode and not password:
        st.error("A 'Senha' é obrigatória para novos usuários.")
        return  # Para a execução

    try:
        if is_edit_mode:
            # MODO EDIÇÃO: Atualiza o usuário existente
            update_user(login, nome, tipo_acesso, password)
            st.toast(f"Usuário '{login}' atualizado com sucesso!", icon="✅")
        else:
            # MODO ADIÇÃO: Cria um novo usuário
            add_user(login, nome, tipo_acesso, password)
            st.toast(f"Usuário '{login}' criado com sucesso!", icon="🎉")

        # Se salvou com sucesso, fecha o formulário e recarrega
        close_form_and_rerun()

    except Exception as e:
        # Trata erro de login duplicado (chave única)
        if "UNIQUE constraint failed" in str(e) or "Duplicate entry" in str(e) or "unique constraint" in str(e):
            st.error(f"Erro: O login '{login}' já existe. Tente outro.")
        else:
            st.error(f"Erro ao salvar: {e}")

def handle_delete(item_data: dict):
    """Processa o clique no botão 'Confirmar Exclusão'."""
    try:
        login_to_delete = item_data['login_usuario']
        delete_user(login_to_delete)
        st.toast(f"Usuário '{login_to_delete}' excluído!", icon="🗑️")
        st.rerun()  # Recarrega a página para remover o item da lista
    except Exception as e:
        st.error(f"Erro ao excluir: {e}")

# =============================================================================
# 5. FUNÇÕES DE RENDERIZAÇÃO DA INTERFACE (Lógica "View")
# (Estas funções desenham os widgets do Streamlit na tela)
# =============================================================================

def render_form():
    """Desenha o formulário de Adicionar/Editar."""
    is_edit_mode = st.session_state.editing_user_item is not None
    title = "✏️ Editando Usuário" if is_edit_mode else "➕ Novo Usuário"
    item = st.session_state.editing_user_item or {}

    with st.container(border=True):
        st.subheader(title)

        with st.form(key="user_form"):
            # Campos do formulário
            login_usuario = st.text_input(
                "Login (ID)",
                value=item.get("login_usuario", ""),
                disabled=is_edit_mode,  # Não pode editar login
                help="O login não pode ser alterado após a criação."
            )
            nome_completo = st.text_input(
                "Nome Completo",
                value=item.get("nome_completo", "")
            )

            # Lógica para achar o índice padrão do selectbox
            default_index = 0
            if is_edit_mode and item.get("tipo_acesso") in PERFIS_DE_ACESSO:
                default_index = PERFIS_DE_ACESSO.index(item.get("tipo_acesso"))

            tipo_acesso = st.selectbox(
                "Perfil de Acesso",
                options=PERFIS_DE_ACESSO,
                index=default_index
            )

            password_help = ("Deixe em branco para manter a senha atual." if is_edit_mode
                             else "Senha obrigatória para novos usuários.")
            password = st.text_input(
                "Senha" if not is_edit_mode else "Nova Senha",
                type="password",
                help=password_help
            )

            # Botões do formulário
            form_cols = st.columns(2)
            submitted = form_cols[0].form_submit_button("Salvar", type="primary", width='stretch')
            cancelled = form_cols[1].form_submit_button("Cancelar", width='stretch')

            if submitted:
                # Junta os dados do formulário em um dicionário
                form_data = {
                    'login_usuario': login_usuario,
                    'nome_completo': nome_completo,
                    'tipo_acesso': tipo_acesso,
                    'password': password
                }
                # Chama a função de lógica "handle_save"
                handle_save(form_data)
            if cancelled:
                # Fecha o formulário e recarrega
                close_form_and_rerun()

def render_table():
    """Desenha a tabela com os usuários e os botões de ação."""
    st.divider()
    st.subheader("Usuários Cadastrados")

    df_users = get_all_users()
    if df_users.empty and not st.session_state.show_user_form:
        st.info("Nenhum usuário cadastrado. Clique em 'Adicionar' para começar.")
        return

    # Cabeçalho da tabela
    header_cols = st.columns([2, 3, 2, 1, 1])
    header_cols[0].markdown("**Login (ID)**")
    header_cols[1].markdown("**Nome Completo**")
    header_cols[2].markdown("**Perfil de Acesso**")
    header_cols[3].markdown("**Ações**")

    # Linhas da tabela
    for index, row in df_users.iterrows():
        row_data = row.to_dict()
        row_cols = st.columns([2, 3, 2, 1, 1])

        row_cols[0].write(row_data['login_usuario'])
        row_cols[1].write(row_data['nome_completo'])
        row_cols[2].write(row_data['tipo_acesso'])

        # Botão Editar
        row_cols[3].button(
            "✏️",
            key=f"edit_{row_data['login_usuario']}",
            on_click=show_edit_form,  # Chama a função de lógica
            args=(row_data,)
        )

        # Botão Excluir (com pop-up de confirmação)
        # Note: O popover NÃO precisa de 'key'
        popover = row_cols[4].popover("🗑️", help=f"Excluir {row_data['login_usuario']}?")
        popover.warning(f"Confirmar exclusão de '{row_data['nome_completo']}'?")
        popover.button(
            "Confirmar",
            key=f"del_{row_data['login_usuario']}",
            on_click=handle_delete,  # Chama a função de lógica
            args=(row_data,)
        )

# =============================================================================
# 6. EXECUÇÃO PRINCIPAL DA PÁGINA
# (Decide o que mostrar)
# =============================================================================

st.title("👤 Gestão de Usuários")
st.markdown("Crie, edite ou remova usuários do sistema.")

# Lógica principal: ou mostra o formulário, ou mostra o botão "Adicionar"
if st.session_state.show_user_form:
    render_form()
else:
    st.button(
        "➕ Adicionar Novo Usuário",
        on_click=show_add_form,  # Chama a função de lógica
        type="primary"
    )

# A tabela é sempre renderizada
render_table()