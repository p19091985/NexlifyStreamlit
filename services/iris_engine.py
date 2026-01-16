import pandas as pd
import numpy as np
import plotly.express as px
import altair as alt
from sklearn.datasets import load_iris
from sklearn.decomposition import PCA
import os
import logging
from typing import Optional, Tuple, Dict, Any, List

logger = logging.getLogger(__name__)

class IrisEngine:
    """
    Motor de processamento para o dataset Iris.
    Responsável por carregamento de dados, transformação e geração de artefatos visuais.
    """
    
    CSV_DIR = 'csv'
    DEFAULT_FILENAME = 'iris_dataset.csv'
    WEB_URL = "https://raw.githubusercontent.com/rhiever/Data-Analysis-and-Machine-Learning-Projects/master/example-data-science-notebook/iris-data-clean.csv"

    @staticmethod
    def _ensure_dir():
        if not os.path.exists(IrisEngine.CSV_DIR):
            try:
                os.makedirs(IrisEngine.CSV_DIR)
            except OSError as e:
                logger.error(f"Falha ao criar diretório {IrisEngine.CSV_DIR}: {e}")

    @staticmethod
    def get_default_csv_path() -> Optional[str]:
        """Garante a existência do CSV local padrão e retorna seu caminho."""
        IrisEngine._ensure_dir()
        file_path = os.path.join(IrisEngine.CSV_DIR, IrisEngine.DEFAULT_FILENAME)
        
        try:
            if not os.path.exists(file_path):
                logger.info("Gerando dataset Iris padrão a partir do Scikit-Learn...")
                iris = load_iris(as_frame=True)
                df = pd.concat([iris.data, iris.target], axis=1)
                df.to_csv(file_path, index=False)
            return file_path
        except Exception as e:
            logger.error(f"Erro crítico ao acessar dataset padrão: {e}")
            return None

    @staticmethod
    def fetch_from_web() -> Tuple[Optional[pd.DataFrame], Optional[str]]:
        """Baixa o dataset da fonte remota."""
        try:
            logger.info(f"Iniciando download de: {IrisEngine.WEB_URL}")
            df = pd.read_csv(IrisEngine.WEB_URL)
            return df, None
        except Exception as e:
            logger.error(f"Erro no download: {e}")
            return None, str(e)

    @staticmethod
    def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
        """Normaliza nomes de colunas e garante a existência da coluna 'species'."""
        df = df.copy()
        
        # Mapa de renomeação para consistência
        col_map = {
            'sepal_length_cm': 'sepal length (cm)', 
            'sepal_width_cm': 'sepal width (cm)',
            'petal_length_cm': 'petal length (cm)', 
            'petal_width_cm': 'petal width (cm)',
            'class': 'species'
        }
        df = df.rename(columns=col_map)
        
        if 'species' not in df.columns:
            if 'target' in df.columns:
                target_names = {0: 'setosa', 1: 'versicolor', 2: 'virginica'}
                df['species'] = df['target'].map(target_names).fillna('unknown')
            else:
                df['species'] = 'unknown'
                
        return df

    @staticmethod
    def generate_plots(df: pd.DataFrame) -> Dict[str, Any]:
        """Gera dicionário contendo objetos de gráfico (Plotly/Altair)."""
        charts = {}
        
        # Plotly Scatter
        charts['plotly_scatter'] = px.scatter(
            df, x='petal length (cm)', y='petal width (cm)', 
            color='species', title='Plotly: Pétala (Comp. vs Larg.)', height=400
        )

        # Altair Scatter
        charts['altair_scatter'] = alt.Chart(df).mark_circle(size=60).encode(
            x='sepal length (cm)', y='sepal width (cm)', color='species',
            tooltip=['species', 'sepal length (cm)', 'sepal width (cm)']
        ).properties(title='Altair: Sépala (Comp. vs Larg.)', height=400).interactive()

        # Altair Bar
        charts['altair_bar'] = alt.Chart(df).mark_bar().encode(
            x='species', y='count()', color='species', tooltip=['species', 'count()']
        ).properties(title='Altair: Contagem por Espécie')

        # Plotly Box
        charts['plotly_box'] = px.box(df, x='species', y='sepal length (cm)', color='species', title='Plotly Box: Sépala (Comp.)')
        
        # Altair Histogram
        charts['altair_hist'] = alt.Chart(df).mark_bar().encode(
            alt.X("petal length (cm)", bin=True), y='count()', color='species'
        ).properties(title="Altair: Histograma Pétala")

        return charts

    @staticmethod
    def perform_pca(df: pd.DataFrame) -> Optional[Any]:
        """Calcula PCA e retorna figura 3D."""
        try:
            y_species = df['species']
            X = df.drop(columns=['target', 'species'], errors='ignore')
            X_numeric = X.select_dtypes(include=[np.number])

            if X_numeric.shape[1] < 3:
                return None

            X_reduced = PCA(n_components=3).fit_transform(X_numeric)
            pca_df = pd.DataFrame(X_reduced, columns=['PC1', 'PC2', 'PC3'])
            pca_df['species'] = y_species.values

            return px.scatter_3d(
                pca_df, x='PC1', y='PC2', z='PC3', 
                color='species', title='Plotly: Projeção 3D (PCA)'
            )
        except Exception as e:
            logger.error(f"Erro no PCA: {e}")
            return None
