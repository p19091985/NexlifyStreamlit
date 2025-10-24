import streamlit as st
import sys
import os
import pandas as pd
from sklearn.datasets import fetch_covtype
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis
from sklearn.neural_network import MLPClassifier
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from utils.st_utils import st_check_session, check_access
except ImportError:
    st.warning("Não foi possível importar 'st_utils'. Funções de sessão e acesso podem não funcionar.")

    def st_check_session():
        pass

    def check_access(levels):
        pass

st.set_page_config(page_title="Painel Análise Covertype", layout="wide")

st_check_session()
check_access([])

def init_state():
    """Inicializa as variáveis de estado da sessão."""
    if 'cov_page_number' not in st.session_state:
        st.session_state.cov_page_number = 0
    if 'cov_full_df' not in st.session_state:
        st.session_state.cov_full_df = None
    if 'cov_analysis_run' not in st.session_state:
        st.session_state.cov_analysis_run = False

@st.cache_data
def export_covertype_to_csv():
    """
    Busca o dataset Covertype (se não existir localmente),
    cria um diretório 'csv' e salva o dataset nele.
    Retorna o caminho do arquivo.
    """
    csv_dir = 'csv'
    file_path = os.path.join(csv_dir, 'covertype_dataset.csv')

    if os.path.exists(file_path):
        return file_path

    if not os.path.exists(csv_dir):
        try:
            os.makedirs(csv_dir)
        except OSError as e:
            st.error(f"Não foi possível criar o diretório '{csv_dir}': {e}")
            return None
    try:
        with st.spinner("Buscando o dataset Covertype da nuvem (primeira execução)..."):
            covtype = fetch_covtype(as_frame=True)
            df = covtype.frame
            df.to_csv(file_path, index=False)
        st.success(f"Dataset salvo em {file_path}")
        return file_path
    except Exception as e:
        st.error(f"Não foi possível salvar o dataset Covertype: {e}")
        return None

@st.cache_data
def get_statistical_summary(_df):
    """
    Gera resumos estatísticos em formato de DataFrame.
    Retorna (info_df, describe_df, target_distribution)
    """

    info_df = pd.DataFrame({
        "Coluna": _df.columns,
        "Tipo (Dtype)": _df.dtypes.astype(str),
        "Valores Não-Nulos": _df.count().values,
        "Valores Nulos": _df.isnull().sum().values,
        "Valores Únicos": _df.nunique().values
    }).reset_index(drop=True)

    describe_df = _df.describe()

    target_col = 'Cover_Type'
    if target_col in _df.columns:
        target_distribution = _df[target_col].value_counts().sort_index().to_frame()
    else:
        target_distribution = pd.DataFrame(columns=["count"])

    return info_df, describe_df, target_distribution

def get_balanced_sample(df, n_per_class=1000, target_col='Cover_Type'):
    """
    Extrai uma amostra balanceada do dataframe para acelerar o treinamento.
    Itera pelos grupos para evitar o FutureWarning do apply.
    """
    min_samples = df[target_col].value_counts().min()
    if n_per_class > min_samples:
        n_per_class = min_samples
        st.warning(f"Ajustando amostragem para {n_per_class} por classe (mínimo encontrado).")

    sampled_dfs = []
                            
    grouped = df.groupby(target_col)

    for group_name, group_df in grouped:
                                       
        sample = group_df.sample(n=n_per_class, random_state=42)
                                    
        sampled_dfs.append(sample)

    balanced_sample_df = pd.concat(sampled_dfs)

    return balanced_sample_df

@st.cache_data
def run_classification_models(_df):
    """
    Treina 10 classificadores em uma amostra balanceada dos dados
    e retorna um DataFrame com as métricas de performance.
    """
    target_col = 'Cover_Type'
    if target_col not in _df.columns:
        st.error("Coluna 'Cover_Type' não encontrada. Não é possível treinar modelos.")
        return pd.DataFrame()

    with st.spinner("Realizando amostragem balanceada (7000 amostras)..."):
        df_sample = get_balanced_sample(_df, n_per_class=1000, target_col=target_col)

    X = df_sample.drop(target_col, axis=1)
    y = df_sample[target_col]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    models = {
        "Regressão Logística": LogisticRegression(max_iter=1000, random_state=42, n_jobs=-1),
        "KNN (K-Vizinhos)": KNeighborsClassifier(n_jobs=-1),
        "Árvore de Decisão": DecisionTreeClassifier(random_state=42),
        "Random Forest": RandomForestClassifier(random_state=42, n_jobs=-1),
        "AdaBoost": AdaBoostClassifier(random_state=42),
        "Gradient Boosting": GradientBoostingClassifier(random_state=42),
        "Gaussian Naive Bayes": GaussianNB(),
        "Análise Discriminante Linear": LinearDiscriminantAnalysis(),
        "Análise Discriminante Quadrática": QuadraticDiscriminantAnalysis(reg_param=0.1),
                                           
        "MLP (Rede Neural)": MLPClassifier(max_iter=500, random_state=42, early_stopping=True, hidden_layer_sizes=(50,))
    }

    results = []
    total_models = len(models)

    progress_bar = st.progress(0, text="Iniciando treinamento...")

    for i, (name, model) in enumerate(models.items()):
        progress_text = f"Treinando {i + 1}/{total_models}: {name}..."
        progress_bar.progress((i) / total_models, text=progress_text)
        y_pred = None

        try:
            if name in ["Regressão Logística", "KNN (K-Vizinhos)", "MLP (Rede Neural)", "Análise Discriminante Linear"]:
                model.fit(X_train_scaled, y_train)
                y_pred = model.predict(X_test_scaled)
            else:
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)

        except Exception as e:
            st.warning(f"Falha ao treinar o modelo '{name}': {e}")

        if y_pred is not None:
            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
            recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
            f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
        else:
            accuracy, precision, recall, f1 = 0, 0, 0, 0

        results.append({
            "Classificador": name,
            "Acurácia": accuracy,
            "Precisão (Weighted)": precision,
            "Recall (Weighted)": recall,
            "F1-Score (Weighted)": f1
        })

    progress_bar.progress(1.0, text="Análise completa!")
    results_df = pd.DataFrame(results).sort_values(by="F1-Score (Weighted)", ascending=False)
    return results_df

def next_page():
    st.session_state.cov_page_number += 1

def prev_page():
    st.session_state.cov_page_number -= 1

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

        st.session_state.cov_full_df = df
        st.session_state.cov_page_number = 0
        st.session_state.cov_analysis_run = False

    except Exception as e:
        st.error(f"Ocorreu um erro ao processar o arquivo:\n{e}")
        st.session_state.cov_full_df = None
        st.session_state.cov_analysis_run = False
        st.stop()

def run_analysis_callback():
    """Callback para o botão 'Iniciar Análise'. Apenas ativa a flag."""
    if st.session_state.cov_full_df is not None:
        st.session_state.cov_analysis_run = True
    else:
        st.error("Por favor, carregue os dados no 'Passo 1' antes de iniciar a análise.")

def render_uploader_panel():
    """Renderiza o 'Passo 1', painel de upload e carregamento de dados."""
    with st.expander("Passo 1: Carregamento de Dados (Dataset Covertype)", expanded=True):
        st.write("Selecione um arquivo CSV para análise ou use o dataset Covertype padrão.")

        default_csv_path = export_covertype_to_csv()

        uploaded_file = st.file_uploader(
            "Selecione um arquivo CSV (Opcional)",
            type="csv",
            help=f"Se nenhum arquivo for enviado, o dataset padrão '{default_csv_path}' será usado.",
            key="covertype_uploader"
        )

        if st.button("Carregar Dados", type="primary", key="covertype_load"):
            load_and_store_data(uploaded_file, default_csv_path)
            st.rerun()

def render_paginated_table():
    """Renderiza a tabela com paginação."""
    st.subheader("Visualização dos Dados (Paginação)")
    PAGE_SIZE = 30
    df = st.session_state.cov_full_df

    if df is None or df.empty:
        st.warning("Os dados carregados estão vazios.")
        return

    total_rows = len(df)
    total_pages = (total_rows // PAGE_SIZE) + (1 if total_rows % PAGE_SIZE > 0 else 0)
    current_page = st.session_state.cov_page_number

    if current_page < 0: current_page = 0
    if current_page >= total_pages: current_page = total_pages - 1                                               
    st.session_state.cov_page_number = current_page

    start_idx = current_page * PAGE_SIZE
    end_idx = min(start_idx + PAGE_SIZE, total_rows)

    st.dataframe(df.iloc[start_idx:end_idx], width='stretch')
    st.text(
        f"Mostrando {start_idx + 1}-{end_idx} de {total_rows} registros | Página {current_page + 1} de {total_pages}")

    col1, col2, col3 = st.columns([2, 6, 2])
    col1.button("Anterior", on_click=prev_page, disabled=(current_page == 0), width='stretch')
    col3.button("Próximo", on_click=next_page, disabled=(current_page >= total_pages - 1), width='stretch')

def render_analysis_results():
    """
    Renderiza o Resumo Estatístico e a Tabela de Classificação
    se a flag 'cov_analysis_run' for Verdadeira.
    """
    if not st.session_state.get('cov_analysis_run') or st.session_state.cov_full_df is None:
        st.info("Clique em 'Iniciar Análise' acima para gerar os relatórios.")
        return

    with st.spinner("Gerando resumo estatístico..."):
        st.subheader("Análise Exploratória e Resumo dos Dados")

        info_df, describe_df, target_dist = get_statistical_summary(st.session_state.cov_full_df)

        st.markdown("##### Informações das Colunas (Tipos e Nulos)")
        st.dataframe(info_df, width='stretch', hide_index=True)
        st.markdown("---")

        st.markdown("##### Resumo Descritivo (Features Numéricas)")
        st.dataframe(describe_df, width='stretch')
        st.markdown("---")

        st.markdown("##### Distribuição das Classes (Alvo: `Cover_Type`)")
        col1, col2 = st.columns([1, 2])
        col1.dataframe(target_dist, width='stretch')
        col2.bar_chart(target_dist)
        st.markdown("---")

    with st.spinner("Treinando 10 modelos de classificação (pode levar alguns minutos)..."):
        st.subheader("Comparação de Modelos de Classificação (em 7000 amostras)")

        results_df = run_classification_models(st.session_state.cov_full_df)

        if not results_df.empty:
            st.success("Resultados da classificação carregados!")

            formatted_df = results_df.style.format({
                "Acurácia": "{:.2%}",
                "Precisão (Weighted)": "{:.2%}",
                "Recall (Weighted)": "{:.2%}",
                "F1-Score (Weighted)": "{:.2%}"
            }).highlight_max(subset=["Acurácia", "F1-Score (Weighted)"], color="#a8f0c4", axis=0)

            st.dataframe(formatted_df, width='stretch', hide_index=True)
        else:
            st.error("Não foi possível gerar os resultados da classificação.")

def render_main_panel():
    """Renderiza o painel principal orquestrando as sub-funções."""
    st.title("🌲 Painel de Análise do Dataset Covertype")

    render_uploader_panel()

    if st.session_state.cov_full_df is not None:
        render_paginated_table()
    else:
        st.info("Clique em 'Carregar Dados' acima para visualizar a tabela.")

    with st.expander("Passo 2: Análise Estatística e Classificação", expanded=True):
        st.write("Clique no botão abaixo para gerar o resumo estatístico e comparar 10 modelos de classificação.")

        st.button(
            "Iniciar Análise (Resumo + Modelos)",
            on_click=run_analysis_callback,
            type="primary",
            disabled=st.session_state.cov_full_df is None
        )

        render_analysis_results()

if __name__ == "__main__":
    init_state()
    render_main_panel()