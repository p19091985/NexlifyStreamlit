import pandas as pd
import numpy as np
import os
import logging
from sklearn.datasets import fetch_covtype
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, f1_score
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis
from sklearn.neural_network import MLPClassifier
from typing import Optional, Dict, List, Tuple

logger = logging.getLogger(__name__)

class CovertypeEngine:
    """
    Engine para processamento de Machine Learning do dataset Covertype.
    """
    
    CSV_DIR = 'csv'
    DEFAULT_FILENAME = 'covertype_dataset.csv'

    @staticmethod
    def get_dataset_path() -> Optional[str]:
        """Obtém ou baixa o dataset."""
        if not os.path.exists(CovertypeEngine.CSV_DIR):
             os.makedirs(CovertypeEngine.CSV_DIR, exist_ok=True)
             
        file_path = os.path.join(CovertypeEngine.CSV_DIR, CovertypeEngine.DEFAULT_FILENAME)
        
        if os.path.exists(file_path):
            return file_path
            
        try:
            logger.info("Baixando Covertype Dataset da API Sklearn...")
            covtype = fetch_covtype(as_frame=True)
            df = covtype.frame
            df.to_csv(file_path, index=False)
            return file_path
        except Exception as e:
            logger.error(f"Erro ao baixar Covertype: {e}")
            return None

    @staticmethod
    def get_balanced_sample(df: pd.DataFrame, n_per_class: int = 1000) -> pd.DataFrame:
        """Retorna uma amostra balanceada do dataset para performance."""
        target_col = 'Cover_Type'
        if target_col not in df.columns: return df
        
        sampled_dfs = []
        for _, group_df in df.groupby(target_col):
            try:
                # Se a classe tiver menos que N, pega tudo
                n = min(len(group_df), n_per_class)
                sampled_dfs.append(group_df.sample(n=n, random_state=42))
            except Exception:
                sampled_dfs.append(group_df)
                
        return pd.concat(sampled_dfs)

    @staticmethod
    def run_benchmark(df: pd.DataFrame, callback_progress=None) -> pd.DataFrame:
        """Executa o torneio de modelos."""
        target_col = 'Cover_Type'
        
        # 1. Preparação
        df_sample = CovertypeEngine.get_balanced_sample(df)
        X = df_sample.drop(target_col, axis=1)
        y = df_sample[target_col]
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.3, random_state=42, stratify=y
        )
        
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # 2. Definição de Modelos
        models = {
            "Logística": LogisticRegression(max_iter=500, n_jobs=-1),
            "KNN": KNeighborsClassifier(n_jobs=-1),
            "Decision Tree": DecisionTreeClassifier(),
            "Random Forest": RandomForestClassifier(n_jobs=-1),
            "Naive Bayes": GaussianNB(),
            "Gradient Boosting": GradientBoostingClassifier(max_depth=3, n_estimators=50), # Lightweight config
        }
        
        results = []
        total = len(models)
        
        for i, (name, model) in enumerate(models.items()):
            if callback_progress:
                callback_progress((i)/total, f"Treinando {name}...")
            
            try:
                # Estratégia de dados escalados vs brutos
                if name in ["Logística", "KNN", "LDA", "QDA", "MLP"]:
                    model.fit(X_train_scaled, y_train)
                    yp = model.predict(X_test_scaled)
                else:
                    model.fit(X_train, y_train)
                    yp = model.predict(X_test)
                    
                acc = accuracy_score(y_test, yp)
                f1 = f1_score(y_test, yp, average='weighted', zero_division=0)
                
                logger.info(f"Modelo {name}: Acc={acc:.2f}, F1={f1:.2f}")
                results.append({"Modelo": name, "Acurácia": acc, "F1-Score": f1})
                
            except Exception as e:
                logger.error(f"Erro em {name}: {e}")
        
        if callback_progress: callback_progress(1.0, "Concluído!")
        
        return pd.DataFrame(results).sort_values(by="F1-Score", ascending=False)

    @staticmethod
    def get_stats(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Retorna estatísticas descritivas."""
        info = pd.DataFrame({
            "Coluna": df.columns, "Tipo": df.dtypes.astype(str),
            "Nulos": df.isnull().sum().values
        })
        
        target_dist = df['Cover_Type'].value_counts().reset_index()
        target_dist.columns = ['Cover_Type', 'Count']
        target_dist['Cover_Type'] = target_dist['Cover_Type'].astype(str)
        
        return info, df.describe(), target_dist
