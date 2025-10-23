import streamlit as st
import sys
import os
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.decomposition import PCA
import numpy as np
import plotly.express as px  # Importação para gráficos interativos

# --- CONFIGURAÇÃO DO PROJETO (Importações e Path) ---
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from utils.st_utils import st_check_session, check_access
except ImportError:
    st.warning("Não foi possível importar 'st_utils'. Funções de sessão e acesso podem não funcionar.")


    def st_check_session():
        pass


    def check_access(levels):
        pass

# --- SEÇÃO 1: Configuração da Página ---
st.set_page_config(page_title="Painel Análise Iris", layout="wide")

# --- SEÇÃO 2: Verificação de Sessão e Estado ---
st_check_session()
check_access([])


def init_state():
    """Inicializa as variáveis de estado da sessão."""
    if 'page_number' not in st.session_state:
        st.session_state.page_number = 0
    if 'full_df' not in st.session_state:
        st.session_state.full_df = None


# --- SEÇÃO 3: Lógica de Análise (Back-end) ---

@st.cache_data
def export_iris_to_csv():
    """
    Carrega o dataset Iris, cria um diretório 'csv' e salva o dataset nele.
    Retorna o caminho do arquivo.
    """
    csv_dir = 'csv'
    file_path = os.path.join(csv_dir, 'iris_dataset.csv')

    if not os.path.exists(csv_dir):
        try:
            os.makedirs(csv_dir)
        except OSError as e:
            st.error(f"Não foi possível criar o diretório '{csv_dir}': {e}")
            return None
    try:
        iris = load_iris(as_frame=True)
        df = pd.concat([iris.data, iris.target], axis=1)
        df.to_csv(file_path, index=False)
        return file_path
    except Exception as e:
        st.error(f"Não foi possível salvar o dataset: {e}")
        return None


def _prepare_species_column(df):
    """
    Função auxiliar para garantir que a coluna 'species' exista.
    Modifica o DataFrame 'df' diretamente (por isso é chamada com df.copy()).
    """
    if 'species' in df.columns:
        # Coluna já existe (ex: arquivo CSV enviado pelo usuário)
        return df

    if 'target' in df.columns:
        # Cria 'species' a partir de 'target' (ex: CSV padrão)
        target_names = {0: 'setosa', 1: 'versicolor', 2: 'virginica'}
        df['species'] = df['target'].map(target_names)
        # Preenche valores não mapeados (caso 'target' tenha outros números)
        df['species'] = df['species'].fillna('unknown')
    else:
        # Nem 'species' nem 'target' existem
        st.warning("Não foi possível encontrar 'target' ou 'species'. Os gráficos podem ficar incorretos.")
        df['species'] = 'unknown'
    return df


def get_interactive_eda_figs(df):
    """
    Cria e RETORNA uma lista de 6 gráficos interativos (Plotly) de EDA.
    """
    # Garante que a coluna 'species' exista
    df = _prepare_species_column(df)

    figs = []

    # Gráfico 1: Scatter Petal
    fig1 = px.scatter(
        df, x='petal length (cm)', y='petal width (cm)',
        color='species', title='Comprimento vs. Largura da Pétala'
    )
    figs.append(fig1)

    # Gráfico 2: Scatter Sepal
    fig2 = px.scatter(
        df, x='sepal length (cm)', y='sepal width (cm)',
        color='species', title='Comprimento vs. Largura da Sépala'
    )
    figs.append(fig2)

    # Gráfico 3: Countplot (Bar)
    count_df = df['species'].value_counts().reset_index()
    count_df.columns = ['species', 'count']
    fig3 = px.bar(
        count_df, x='species', y='count',
        color='species', title='Contagem por Espécie'
    )
    figs.append(fig3)

    # Gráfico 4: Boxplot Sepal
    fig4 = px.box(
        df, x='species', y='sepal length (cm)',
        color='species', title='Box Plot do Comprimento da Sépala'
    )
    figs.append(fig4)

    # Gráfico 5: Violinplot Petal
    fig5 = px.violin(
        df, x='species', y='petal width (cm)',
        color='species', title='Violin Plot da Largura da Pétala'
    )
    figs.append(fig5)

    # Gráfico 6: Histograma Petal Length
    fig6 = px.histogram(
        df, x='petal length (cm)',
        color='species', title='Distribuição do Comprimento da Pétala'
    )
    figs.append(fig6)

    return figs


def get_interactive_pca_fig(df):
    """
    Cria e RETORNA um gráfico PCA 3D interativo (Plotly).
    """
    try:
        # --- CORREÇÃO APLICADA AQUI ---
        # Garante que a coluna 'species' exista ANTES de tentar usá-la.
        df = _prepare_species_column(df)

        # Agora 'species' está garantido de existir
        y_species = df['species']

        # Prepara X (features) e y (target numérico)
        if 'target' in df.columns:
            y_target = df['target']
            X = df.drop(columns=['target', 'species'], errors='ignore')
        else:
            # Se não houver 'target', cria um a partir de 'species'
            species_map = {name: i for i, name in enumerate(df['species'].unique())}
            y_target = df['species'].map(species_map)
            X = df.drop(columns=['species'], errors='ignore')

        # --- FIM DA CORREÇÃO ---

        X_numeric = X.select_dtypes(include=[np.number])

        if X_numeric.shape[1] < 3:
            st.error(f"Dataset possui apenas {X_numeric.shape[1]} colunas numéricas. PCA 3D requer ao menos 3.")
            return None

        X_reduced = PCA(n_components=3).fit_transform(X_numeric)

        # Cria um DataFrame para o Plotly
        pca_df = pd.DataFrame(X_reduced, columns=['1º Autovetor', '2º Autovetor', '3º Autovetor'])
        pca_df['species'] = y_species  # y_species foi definido acima

        # Cria o gráfico 3D interativo
        fig_pca = px.scatter_3d(
            pca_df,
            x='1º Autovetor',
            y='2º Autovetor',
            z='3º Autovetor',
            color='species',
            title='Primeiras três dimensões do PCA (Interativo)'
        )

        return fig_pca

    except Exception as e:
        # O erro 'species' não deve mais acontecer, mas mantemos o 'catch'
        st.error(f"Ocorreu um erro ao gerar o gráfico PCA:\n{e}")
        return None


# --- SEÇÃO 4: Lógica de UI (Callbacks e Carregamento) ---

def next_page():
    st.session_state.page_number += 1


def prev_page():
    st.session_state.page_number -= 1


def load_and_store_data(uploaded_file, default_csv_path):
    """Carrega o DataFrame e o armazena no session_state"""
    df = None
    try:
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            st.success("Arquivo enviado com sucesso!")
        elif default_csv_path and os.path.exists(default_csv_path):
            df = pd.read_csv(default_csv_path)
            st.info(f"Usando dataset padrão: {default_csv_path}")
        else:
            st.error("Nenhum arquivo CSV padrão encontrado e nenhum arquivo enviado.")
            st.stop()

        st.session_state.full_df = df
        st.session_state.page_number = 0
        return df

    except Exception as e:
        st.error(f"Ocorreu um erro ao processar o arquivo:\n{e}")
        st.stop()


# --- SEÇÃO 5: Renderização (View) ---

def render_paginated_table():
    """Renderiza a tabela com paginação de 30 em 30 e todas as colunas"""
    st.subheader("Visualização dos Dados (Paginação)")

    PAGE_SIZE = 30
    df = st.session_state.full_df

    if df is None:
        st.warning("Nenhum dado carregado para exibir na tabela.")
        return

    total_rows = len(df)
    total_pages = (total_rows // PAGE_SIZE) + (1 if total_rows % PAGE_SIZE > 0 else 0)
    current_page = st.session_state.page_number

    if current_page < 0: current_page = 0
    if current_page >= total_pages: current_page = total_pages - 1
    st.session_state.page_number = current_page

    start_idx = current_page * PAGE_SIZE
    end_idx = min(start_idx + PAGE_SIZE, total_rows)

    st.dataframe(df.iloc[start_idx:end_idx], use_container_width=True)

    st.text(
        f"Mostrando {start_idx + 1}-{end_idx} de {total_rows} registros | Página {current_page + 1} de {total_pages}")

    col1, col2, col3 = st.columns([2, 6, 2])
    col1.button("Anterior", on_click=prev_page, disabled=(current_page == 0), use_container_width=True)
    col3.button("Próximo", on_click=next_page, disabled=(current_page >= total_pages - 1), use_container_width=True)


def render_main_panel():
    """
    Desenha os componentes visuais da página na tela.
    """
    st.title("📈 Painel de Análise do Dataset Iris (EDA + PCA)")

    # --- UPLOADER NO PAINEL PRINCIPAL ---
    with st.expander("Passo 1: Configuração da Análise", expanded=True):
        st.write("Selecione um arquivo CSV para análise ou use o dataset Iris padrão.")
        default_csv_path = export_iris_to_csv()

        uploaded_file = st.file_uploader(
            "Selecione um arquivo CSV (Opcional)",
            type="csv",
            help=f"Se nenhum arquivo for enviado, o dataset padrão '{default_csv_path}' será usado.",
            key="iris_uploader_main"
        )

        if st.button("Carregar Dados", type="primary"):
            load_and_store_data(uploaded_file, default_csv_path)

    # --- TABELA PAGINADA ---
    if st.session_state.full_df is not None:
        render_paginated_table()
    else:
        st.info("Clique em 'Carregar Dados' acima para visualizar a tabela.")

    # --- BOTÃO DE ANÁLISE NA PÁGINA PRINCIPAL ---
    with st.expander("Passo 2: Análise Gráfica Interativa", expanded=True):
        st.write("Clique no botão abaixo para gerar os gráficos com base nos dados carregados.")

        if st.button("Iniciar Análise Gráfica (EDA + PCA)"):

            df = st.session_state.full_df
            if df is None:
                st.error("Por favor, carregue os dados no 'Passo 1' antes de iniciar a análise.")
                st.stop()

            # --- RENDERIZAÇÃO DOS GRÁFICOS INTERATIVOS ---
            with st.spinner("Gerando gráficos de análise exploratória..."):
                st.subheader("Análise Exploratória de Dados (EDA)")
                # Passa uma cópia para as funções de plotagem
                eda_figs = get_interactive_eda_figs(df.copy())

                col1, col2 = st.columns(2)
                col1.plotly_chart(eda_figs[0], use_container_width=True)
                col2.plotly_chart(eda_figs[1], use_container_width=True)
                col1.plotly_chart(eda_figs[2], use_container_width=True)
                col2.plotly_chart(eda_figs[3], use_container_width=True)
                col1.plotly_chart(eda_figs[4], use_container_width=True)
                col2.plotly_chart(eda_figs[5], use_container_width=True)

            with st.spinner("Gerando gráfico PCA..."):
                st.subheader("Análise de Componentes Principais (PCA)")
                # Passa uma cópia para as funções de plotagem
                pca_fig = get_interactive_pca_fig(df.copy())
                if pca_fig:
                    st.plotly_chart(pca_fig, use_container_width=True)
                else:
                    st.error("Não foi possível gerar o gráfico PCA.")

            st.success("Análise concluída!")


# --- SEÇÃO 6: Execução Principal ---
if __name__ == "__main__":
    init_state()
    render_main_panel()