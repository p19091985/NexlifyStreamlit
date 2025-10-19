                                       
import streamlit as st


class VegetaisAuditoriaView:
    def __init__(self, controller):
        self.controller = controller

    def render(self):
        """Renderiza a página inteira de Vegetais e Auditoria."""
        st.title("🌿 Vegetais e Auditoria")

                                                     
        self._render_transaction_section()
        if st.session_state.veg_show_tipo_form:
            self._render_tipo_form()

        st.divider()

                                                
        col1, col2 = st.columns([3, 2])
        with col1:
            self._render_vegetais_table()
        with col2:
            self._render_log_table()

    def _render_transaction_section(self):
        """Renderiza a área de gerenciamento de tipos e transações."""
        with st.container(border=True):
            st.subheader("🔄 Operação Atômica (Transação)")

            df_vegetais = self.controller.get_all_vegetais()
            df_tipos = self.controller.get_all_tipos()

            vegetais_list = [f"{row['nome']} (ID: {row['id']})" for _, row in df_vegetais.iterrows()]
            tipos_list = df_tipos['nome'].tolist()

            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                vegetal_selecionado = st.selectbox("1. Selecione o Vegetal a Reclassificar", vegetais_list, index=None,
                                                   placeholder="Escolha um vegetal...")
            with col2:
                novo_tipo_nome = st.selectbox("2. Selecione o Novo Tipo", tipos_list, index=None,
                                              placeholder="Escolha um tipo...")
            with col3:
                st.markdown("<br/>", unsafe_allow_html=True)
                st.button("Executar", on_click=self.controller.executar_reclassificacao,
                          args=(vegetal_selecionado, novo_tipo_nome), width='stretch', type="primary")

            st.markdown("---")
            st.subheader("Gerenciar Tipos de Vegetais")
            if not st.session_state.veg_show_tipo_form:
                st.button("➕ Adicionar Novo Tipo", on_click=self.controller.open_tipo_form)
            self._render_tipos_table(df_tipos)

    def _render_tipos_table(self, df_tipos):
        """Renderiza a tabela de Tipos de Vegetais."""
        if df_tipos.empty:
            st.info("Nenhum tipo de vegetal cadastrado.")
            return

        for _, row in df_tipos.iterrows():
            row_data = row.to_dict()
            cols = st.columns([1, 4, 1, 1])
            cols[0].write(f"**ID: {row_data['id']}**")
            cols[1].write(row_data['nome'])
            cols[2].button("✏️", key=f"edit_tipo_{row_data['id']}", on_click=self.controller.open_tipo_form,
                           args=(row_data,))

            popover = cols[3].popover("🗑️", help=f"Excluir '{row_data['nome']}'?")
            popover.warning(f"Confirmar exclusão de '{row_data['nome']}'?")
            popover.button("Confirmar", key=f"del_tipo_{row_data['id']}", on_click=self.controller.delete_tipo_vegetal,
                           args=(row_data,))

    def _render_tipo_form(self):
        """Renderiza o formulário para adicionar/editar um Tipo de Vegetal."""
        is_edit = st.session_state.veg_editing_tipo_item is not None
        title = "✏️ Editando Tipo" if is_edit else "➕ Novo Tipo de Vegetal"
        item = st.session_state.veg_editing_tipo_item or {}

        with st.container(border=True):
            st.subheader(title)
            with st.form(key="tipo_form"):
                nome = st.text_input("Nome do Tipo", value=item.get("nome", ""))

                form_cols = st.columns(2)
                submitted = form_cols[0].form_submit_button("Salvar", type="primary", width='stretch')
                cancelled = form_cols[1].form_submit_button("Cancelar", width='stretch')

                if submitted:
                    self.controller.save_tipo_vegetal(nome)
                if cancelled:
                    self.controller.close_tipo_form()

    def _render_vegetais_table(self):
        """Renderiza a tabela principal de vegetais."""
        st.subheader("🍽️ Tabela 'VEGETAIS'")
        df_vegetais = self.controller.get_all_vegetais()
                                
        st.dataframe(df_vegetais, width='stretch', hide_index=True)

    def _render_log_table(self):
        """Renderiza a tabela de logs de auditoria."""
        st.subheader("🛡️ Tabela 'LOG_ALTERACOES'")
        df_logs = self.controller.get_all_logs()
                                
        st.dataframe(df_logs, width='stretch', hide_index=True)