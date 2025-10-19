                                      

import streamlit as st
import toml
import pandas as pd
import numpy as np
from pathlib import Path
from utils.st_utils import st_check_session, check_access

st.set_page_config(page_title="Santuário do Design", layout="wide")
st_check_session()
check_access(['Administrador Global', 'Gerente de TI'])

CONFIG_PATH = Path(".streamlit/config.toml")

                              
PRESET_THEMES = {
    "☀️ Temas Claros": {
        "Padrão Streamlit": {"primaryColor": "#FF4B4B", "backgroundColor": "#FFFFFF",
                             "secondaryBackgroundColor": "#F0F2F6", "textColor": "#31333F", "font": "sans serif"},
        "Menta Suave": {"primaryColor": "#1FAB89", "backgroundColor": "#D7FBE8", "secondaryBackgroundColor": "#9DF3C4",  
                        "textColor": "#042F1A", "font": "sans serif"},  
        "Algodão Doce": {"primaryColor": "#F76B8A", "backgroundColor": "#FDECF2", "secondaryBackgroundColor": "#FAD2E1",
                         "textColor": "#5E2E3B", "font": "sans serif"},
        "Areia e Céu": {"primaryColor": "#3C8DAD", "backgroundColor": "#F0EBE3", "secondaryBackgroundColor": "#D4C7B0",  
                        "textColor": "#1E3C4A", "font": "sans serif"},  
        "Lavanda": {"primaryColor": "#7F5A83", "backgroundColor": "#F4EEFF", "secondaryBackgroundColor": "#DCD6F7",
                    "textColor": "#2B192E", "font": "serif"},
                            
        "Limão Siciliano": {"primaryColor": "#D4E157", "backgroundColor": "#FFFDE7",  
                            "secondaryBackgroundColor": "#FFFACD",  
                            "textColor": "#4E342E", "font": "sans serif"},  
        "Pêssego": {"primaryColor": "#FF8A65", "backgroundColor": "#FFF3E0", "secondaryBackgroundColor": "#FFE0B2",
                    "textColor": "#4E342E", "font": "serif"},
        "Céu de Inverno": {"primaryColor": "#4FC3F7", "backgroundColor": "#E1F5FE",  
                           "secondaryBackgroundColor": "#B3E5FC",  
                           "textColor": "#1A237E", "font": "sans serif"},  
    },
    "🌙 Temas Escuros": {
        "Drácula": {"primaryColor": "#bd93f9", "backgroundColor": "#282a36", "secondaryBackgroundColor": "#44475a",  
                    "textColor": "#f8f8f2", "font": "sans serif"},  
        "Monokai Pro": {"primaryColor": "#ff6188", "backgroundColor": "#2D2A2E", "secondaryBackgroundColor": "#403E41",
                        "textColor": "#FCFCFA", "font": "monospace"},
        "Nord": {"primaryColor": "#88C0D0", "backgroundColor": "#2E3440", "secondaryBackgroundColor": "#3B4252",
                 "textColor": "#ECEFF4", "font": "sans serif"},
        "Synthwave '84": {"primaryColor": "#f92aad", "backgroundColor": "#2b213a",  
                           "secondaryBackgroundColor": "#34294f", "textColor": "#f8f8f2", "font": "sans serif"},  
        "One Dark Pro": {"primaryColor": "#61AFEF", "backgroundColor": "#282C34", "secondaryBackgroundColor": "#31353F",
                         "textColor": "#ABB2BF", "font": "monospace"},
                             
        "Meia-noite na Floresta": {"primaryColor": "#4DB6AC", "backgroundColor": "#1B2631",  
                                   "secondaryBackgroundColor": "#2C3E50",  
                                   "textColor": "#E0E0E0", "font": "sans serif"},  
        "Café Expresso": {"primaryColor": "#A1887F", "backgroundColor": "#211F1F",  
                          "secondaryBackgroundColor": "#3E2723",  
                          "textColor": "#D7CCC8", "font": "serif"},  
        "Retrô Sombrio (Gruvbox)": {"primaryColor": "#FABD2F", "backgroundColor": "#282828",  
                                    "secondaryBackgroundColor": "#3C3836",  
                                    "textColor": "#EBDBB2", "font": "monospace"},  
    },
    "🌈 Temas Vibrantes": {
        "Pôr do Sol Tropical": {"primaryColor": "#FF6B6B", "backgroundColor": "#FFF1C9",
                                "secondaryBackgroundColor": "#FFE69A", "textColor": "#8B4513", "font": "sans serif"},
        "Cyberpunk Neon": {"primaryColor": "#00F2FF", "backgroundColor": "#0C0032",  
                           "secondaryBackgroundColor": "#1D004D", "textColor": "#F0F0F0", "font": "monospace"},  
        "Vaporwave": {"primaryColor": "#F92AAD", "backgroundColor": "#2B213A", "secondaryBackgroundColor": "#34294F",
                      "textColor": "#F8F8f2", "font": "sans serif"},
        "Arco-íris Pastel": {"primaryColor": "#ff8b94", "backgroundColor": "#fcefee",  
                             "secondaryBackgroundColor": "#f8e0e2", "textColor": "#683135", "font": "serif"},  
                               
        "Magma": {"primaryColor": "#FF3D00", "backgroundColor": "#212121", "secondaryBackgroundColor": "#303030",
                  "textColor": "#F5F5F5", "font": "monospace"},
        "Oceano Elétrico": {"primaryColor": "#00E5FF", "backgroundColor": "#010A14",  
                            "secondaryBackgroundColor": "#02162B",  
                            "textColor": "#E0FFFF", "font": "sans serif"},  
        "Verde Limão Neon": {"primaryColor": "#76FF03", "backgroundColor": "#1B1B1B",  
                             "secondaryBackgroundColor": "#2C2C2C",  
                             "textColor": "#E6FEE9", "font": "sans serif"},  
    },
    "💼 Temas Corporativos": {
        "Azul Executivo": {"primaryColor": "#005A9E", "backgroundColor": "#F5F5F5",
                           "secondaryBackgroundColor": "#E1EBF5", "textColor": "#212121", "font": "sans serif"},
        "Grafite Sóbrio": {"primaryColor": "#4A4A4A", "backgroundColor": "#FFFFFF",  
                           "secondaryBackgroundColor": "#EAEAEA", "textColor": "#333333", "font": "sans serif"},  
        "Verde Confiança": {"primaryColor": "#007A5E", "backgroundColor": "#F7F9F9",
                            "secondaryBackgroundColor": "#E6F2F0", "textColor": "#1D1C1D", "font": "sans serif"},
        "Bordô Elegante": {"primaryColor": "#800020", "backgroundColor": "#FDF6F7",  
                           "secondaryBackgroundColor": "#FBEAEF", "textColor": "#33000A", "font": "serif"},  
                                  
        "Cinza Tecnológico": {"primaryColor": "#0078D4", "backgroundColor": "#F3F3F3",  
                              "secondaryBackgroundColor": "#E1E1E1",  
                              "textColor": "#141414", "font": "sans serif"},  
        "Ouro e Petróleo (Finanças)": {"primaryColor": "#B8860B", "backgroundColor": "#121212",  
                                       "secondaryBackgroundColor": "#282828",  
                                       "textColor": "#E5E5E5", "font": "serif"},  
        "Azul Saúde": {"primaryColor": "#00A0B0", "backgroundColor": "#FFFFFF", "secondaryBackgroundColor": "#EDF8F9",
                       "textColor": "#4A4A4A", "font": "sans serif"},
    }
}


def load_config():
    if not CONFIG_PATH.is_file(): return PRESET_THEMES["☀️ Temas Claros"]["Padrão Streamlit"]
    try:
        config = toml.load(CONFIG_PATH)
        return config.get("theme", PRESET_THEMES["☀️ Temas Claros"]["Padrão Streamlit"])
    except Exception:
        return PRESET_THEMES["☀️ Temas Claros"]["Padrão Streamlit"]  


def save_config(theme_settings):
    try:
        CONFIG_PATH.parent.mkdir(exist_ok=True)
        full_config = toml.load(CONFIG_PATH) if CONFIG_PATH.is_file() else {}
        full_config["theme"] = theme_settings
        with open(CONFIG_PATH, "w") as f:
            toml.dump(full_config, f)
        st.toast("Tema salvo com sucesso!", icon="✅")
        st.success("O tema foi atualizado. Recarregue a página (pressione 'R') para aplicar as mudanças globalmente.")  
        st.balloons()
    except Exception as e:
        st.error(f"Não foi possível salvar a configuração: {e}")


def restore_defaults():
    try:
        if not CONFIG_PATH.is_file(): st.toast("Nenhum tema customizado para restaurar.", icon="ℹ️"); return
        full_config = toml.load(CONFIG_PATH)
        if "theme" in full_config:
            del full_config["theme"]
            with open(CONFIG_PATH, "w") as f:  
                toml.dump(full_config, f)  
            st.toast("Tema padrão restaurado!", icon="✅")
            st.success("Recarregue a página para ver o tema padrão do Streamlit.")
        else:
            st.toast("Nenhum tema customizado encontrado para restaurar.", icon="ℹ️")
    except Exception as e:
        st.error(f"Não foi possível restaurar os padrões: {e}")  


if 'current_theme' not in st.session_state:
    st.session_state.current_theme = load_config()


def update_theme_value(theme_key, widget_key):
    if widget_key in st.session_state:
        st.session_state.current_theme[theme_key] = st.session_state[widget_key]


st.title("🌟 Santuário do Design")
st.caption("O centro de comando definitivo para a personalização visual da sua aplicação.")

main_cols = st.columns([1, 1.4])

with main_cols[0]:
    st.header("⚙️ Ferramentas de Customização")

    with st.expander("🎨 Galeria de Temas Predefinidos", expanded=True):
        theme_category = st.selectbox("Selecione uma categoria", options=PRESET_THEMES.keys())
        theme_name = st.selectbox("Selecione um tema", options=PRESET_THEMES[theme_category].keys())  

        if st.button("Aplicar Tema da Galeria", width='stretch'):
            st.session_state.current_theme = PRESET_THEMES[theme_category][theme_name].copy()
            st.rerun()

    tab_colors, tab_fonts, tab_export = st.tabs(["Cores", "Fontes", "Exportar"])

    with tab_colors:
        st.subheader("Ajuste Fino de Cores")
        st.color_picker("Cor Primária", value=st.session_state.current_theme.get("primaryColor", "#FF4B4B"),  
                        key="picker_primaryColor", on_change=update_theme_value,  
                        kwargs={'theme_key': 'primaryColor', 'widget_key': 'picker_primaryColor'})  
        st.color_picker("Fundo Principal", value=st.session_state.current_theme.get("backgroundColor", "#FFFFFF"),
                        key="picker_backgroundColor", on_change=update_theme_value,
                        kwargs={'theme_key': 'backgroundColor', 'widget_key': 'picker_backgroundColor'})
        st.color_picker("Fundo Secundário",  
                        value=st.session_state.current_theme.get("secondaryBackgroundColor", "#F0F2F6"),  
                        key="picker_secondaryBackgroundColor", on_change=update_theme_value,  
                        kwargs={'theme_key': 'secondaryBackgroundColor',  
                                'widget_key': 'picker_secondaryBackgroundColor'})  
        st.color_picker("Cor do Texto", value=st.session_state.current_theme.get("textColor", "#31333F"),
                        key="picker_textColor", on_change=update_theme_value,
                        kwargs={'theme_key': 'textColor', 'widget_key': 'picker_textColor'})

    with tab_fonts:
        st.subheader("Tipografia")
        font_options = ["sans serif", "serif", "monospace"]
        st.selectbox("Família da Fonte", options=font_options,  
                     index=font_options.index(st.session_state.current_theme.get("font", "sans serif")),  
                     key="selector_font", on_change=update_theme_value,  
                     kwargs={'theme_key': 'font', 'widget_key': 'selector_font'})  
        st.caption("A fonte será aplicada globalmente após salvar e recarregar a página.")

    with tab_export:  
        st.subheader("📥 Exportar Configuração TOML")
        st.markdown("Copie o código abaixo e cole no seu arquivo `.streamlit/config.toml`.")
        toml_string = "[theme]\n"
        for key, value in st.session_state.current_theme.items():
            toml_string += f'{key} = "{value}"\n'
        st.code(toml_string, language="toml")

    st.divider()
    st.subheader("⚡ Ações Finais")
    action_cols = st.columns(2)

    if action_cols[0].button("💾 Salvar Tema na Aplicação", type="primary", width='stretch'):  
        save_config(st.session_state.current_theme)

    if action_cols[1].button("🗑️ Restaurar Padrão", width='stretch'):
        restore_defaults()

with main_cols[1]:
    st.header("👁️ Pré-visualização Dinâmica")
    preview_css = f"""
    <style>
        .preview-container {{
            border: 2px solid {st.session_state.current_theme.get('secondaryBackgroundColor', '#F0F2F6')};
            background-color: {st.session_state.current_theme.get('backgroundColor', '#FFFFFF')}; #
            color: {st.session_state.current_theme.get('textColor', '#31333F')}; #
            border-radius: 0.75rem;
            padding: 20px; #
        }}
        .preview-container *, .preview-container h3, .preview-container p, .preview-container li {{
            color: {st.session_state.current_theme.get('textColor', '#31333F')} !important; #
        }}
    </style>
    """
    st.markdown(preview_css, unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="preview-container">', unsafe_allow_html=True)
        st.subheader("Componentes do Streamlit")
        st.write("Veja como os elementos se comportam com o tema selecionado.")
        st.info("Esta é uma mensagem de informação (st.info).")
        st.success("Operação concluída com sucesso (st.success).")
        st.warning("Atenção: verifique os dados (st.warning).")
        st.error("Ocorreu um erro na validação (st.error).")  
        st.markdown("##### Gráfico (st.line_chart)")
        chart_data = pd.DataFrame(np.random.randn(20, 3), columns=['Marketing', 'Vendas', 'Suporte'])
        st.line_chart(chart_data)
        st.progress(75, text="Barra de progresso (st.progress)")
        st.slider("Slider", 0, 100, 50, help="st.slider")
        btn_cols = st.columns(2)

        btn_cols[0].button("Botão Primário", type="primary", width='stretch')
        btn_cols[1].button("Botão Secundário", width='stretch')

        st.markdown("##### Tabela (st.dataframe)")  
        df = pd.DataFrame({
            "Produto": ["App A", "App B", "App C", "App D"],
            "Versão": ["1.2.0", "2.0.1", "3.4.0", "4.1.2"],
            "Status": ["✅ Ativo", "✅ Ativo", "⚠️ Manutenção", "❌ Descontinuado"]
        })

                                                  

        st.dataframe(df, use_container_width=True, hide_index=True)

        st.markdown('</div>', unsafe_allow_html=True)  