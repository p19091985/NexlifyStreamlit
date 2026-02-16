import streamlit as st

PERFIS_DE_ACESSO = [
    'Administrador Global',
    'Diretor de Operações',
    'Gerente de TI',
    'Supervisor de Produção',
    'Operador de Linha',
    'Analista de Dados',
    'Auditor Externo'
]

class UsuariosView:
    def __init__(self, controller):
        self.controller = controller

    def render(self):
        """Renderiza a página inteira."""
        st.title("👤 Gestão de Usuários")
        st.markdown("Crie, edite ou remova usuários do sistema.")

        if st.session_state.show_user_form:
            self._render_form()
        else:
            st.button("➕ Adicionar Novo Usuário", on_click=self.controller.open_form, type="primary")

        st.divider()
        self._render_table()

    def _render_table(self):
        """Renderiza a tabela de usuários."""
        st.subheader("Usuários Cadastrados")

        df_users = self.controller.get_all_users()
        if df_users.empty and not st.session_state.show_user_form:
            st.info("Nenhum usuário cadastrado. Clique em 'Adicionar' para começar.")
            return

        header_cols = st.columns([2, 3, 2, 1, 1])
        header_cols[0].markdown("**Login (ID)**")
        header_cols[1].markdown("**Nome Completo**")
        header_cols[2].markdown("**Perfil de Acesso**")
        header_cols[3].markdown("**Ações**")

        for index, row in df_users.iterrows():
            row_data = row.to_dict()
            row_cols = st.columns([2, 3, 2, 1, 1])

            row_cols[0].write(row_data['login_usuario'])
            row_cols[1].write(row_data['nome_completo'])
            row_cols[2].write(row_data['tipo_acesso'])

            row_cols[3].button("✏️", key=f"edit_{row_data['login_usuario']}",
                               on_click=self.controller.open_form, args=(row_data,))

            popover = row_cols[4].popover("🗑️", help=f"Excluir {row_data['login_usuario']}?")
            popover.warning(f"Confirmar exclusão de '{row_data['nome_completo']}'?")
            popover.button("Confirmar", key=f"del_{row_data['login_usuario']}",
                           on_click=self.controller.delete_item, args=(row_data,))

    def _render_form(self):
        """Renderiza o formulário de adição/edição."""
        is_edit_mode = st.session_state.editing_user_item is not None
        title = "✏️ Editando Usuário" if is_edit_mode else "➕ Novo Usuário"
        item = st.session_state.editing_user_item or {}

        with st.container(border=True):
            st.subheader(title)

            with st.form(key="user_form"):
                                                       
                login_usuario = st.text_input(
                    "Login (ID)",
                    value=item.get("login_usuario", ""),
                    disabled=is_edit_mode,
                    help="O login não pode ser alterado após a criação."
                )

                nome_completo = st.text_input(
                    "Nome Completo",
                    value=item.get("nome_completo", "")
                )

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

                form_cols = st.columns(2)
                submitted = form_cols[0].form_submit_button("Salvar", type="primary", width='stretch')
                cancelled = form_cols[1].form_submit_button("Cancelar", width='stretch')

                if submitted:
                                                          
                    form_data = {
                        'login_usuario': login_usuario,
                        'nome_completo': nome_completo,
                        'tipo_acesso': tipo_acesso,
                        'password': password
                    }
                    self.controller.save_item(form_data, is_edit_mode)

                if cancelled:
                    self.controller.close_form()