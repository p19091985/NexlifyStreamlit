import streamlit as st


class GatosView:
    def __init__(self, controller):
        self.controller = controller

    def render(self):
        st.title("🐱 Gerenciador de Espécies de Gatos")
        st.markdown("Use a tabela abaixo para visualizar, editar ou excluir espécies.")

        if st.session_state.show_form:
            self._render_form()
            st.divider()
        else:
            st.button("➕ Adicionar Nova Espécie", on_click=self.controller.open_form, type="primary")
            st.divider()

        self._render_table()

    def _render_table(self):
        df_gatos = self.controller.get_all_gatos()
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
            row_cols[3].button("✏️", key=f"edit_{row_data['id']}", on_click=self.controller.open_form, args=(row_data,))

                                      
            popover = row_cols[4].popover("🗑️")
            popover.warning(f"Excluir '{row_data['nome_especie']}'?")
            popover.button("Confirmar Exclusão", key=f"del_{row_data['id']}", on_click=self.controller.delete_item,
                           args=(row_data,))

    def _render_form(self):
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
                    self.controller.save_item(nome, origem, temperamento)
                if cancelled:
                    self.controller.close_form()

