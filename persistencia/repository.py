import pandas as pd
import logging
import json
from pathlib import Path
from typing import List, Dict, Optional, Any
from filelock import FileLock

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class GenericRepository:
    """
    Classe genérica para interagir com o armazenamento em arquivos JSON.
    Implementa thread-safety usando FileLock para evitar condições de corrida durante escritas.
    """
    
    # Resolve para caminho absoluto para evitar ambiguidades em diferentes OS
    DATA_DIR: Path = (Path(__file__).parent.parent / "data").resolve()

    @staticmethod
    def _get_file_path(table_name: str) -> Path:
        """Retorna o caminho do arquivo JSON correspondente à tabela."""
        return GenericRepository.DATA_DIR / f"{table_name}.json"

    @staticmethod
    def _get_lock_path(table_name: str) -> Path:
        """Retorna o caminho do arquivo de lock correspondente à tabela."""
        return GenericRepository.DATA_DIR / f"{table_name}.json.lock"

    @staticmethod
    def _load_data(table_name: str) -> List[Dict[str, Any]]:
        """Lê os dados do arquivo JSON de forma segura."""
        file_path = GenericRepository._get_file_path(table_name)
        if not file_path.exists():
            logging.warning(f"Arquivo de dados não encontrado: {file_path}")
            return []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            logging.error(f"Arquivo corrompido ou vazio: {file_path}")
            return []
        except Exception as e:
            logging.error(f"Erro ao ler arquivo {file_path}: {e}")
            return []

    @staticmethod
    def _save_data(table_name: str, data: List[Dict[str, Any]]) -> None:
        """Salva os dados no arquivo JSON usando FileLock para exclusão mútua."""
        file_path = GenericRepository._get_file_path(table_name)
        lock_path = GenericRepository._get_lock_path(table_name)
        lock = FileLock(str(lock_path))

        try:
            with lock.acquire(timeout=10):  # Wait up to 10 seconds for the lock
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            logging.error(f"Erro ao salvar arquivo {file_path} com lock: {e}")
            raise

    @staticmethod
    def read_table_to_dataframe(
        table_name: str, 
        columns: Optional[List[str]] = None, 
        where_conditions: Optional[Dict[str, Any]] = None
    ) -> pd.DataFrame:
        """Lê dados de um arquivo JSON (simulando uma tabela) e retorna DataFrame."""
        try:
            data = GenericRepository._load_data(table_name)
            df = pd.DataFrame(data)

            if df.empty:
                 if columns:
                     return pd.DataFrame(columns=[col.lower() for col in columns])
                 return df

            # Normaliza colunas para minúsculo
            df.columns = [str(col).lower() for col in df.columns]

            # Filtros (WHERE)
            if where_conditions:
                 for col, val in where_conditions.items():
                     col_lower = col.lower()
                     if col_lower in df.columns:
                         # Handle simple equality check
                         df = df[df[col_lower] == val]
            
            # Seleção de colunas
            if columns:
                cols_lower = [col.lower() for col in columns]
                existing_cols = [c for c in cols_lower if c in df.columns]
                df = df[existing_cols]

            return df
        except Exception as e:
            logging.error(f"Erro ao ler tabela '{table_name}': {e}")
            return pd.DataFrame()

    @staticmethod
    def write_dataframe_to_table(df: pd.DataFrame, table_name: str) -> None:
        """
        Escreve (append) um DataFrame no arquivo JSON.
        """
        lock_path = GenericRepository._get_lock_path(table_name)
        lock = FileLock(str(lock_path))

        try:
            with lock.acquire(timeout=10):
                # 1. READ (Atomic start)
                current_data = GenericRepository._load_data(table_name)
                
                # Converter DF para lista de dicionários
                df_to_write = df.copy()
                df_to_write.columns = [str(col).lower() for col in df_to_write.columns]
                new_records = df_to_write.to_dict(orient='records')
                
                # 2. VALIDATE
                if table_name == 'especie_gatos':
                    existing_names = {r.get('nome_especie') for r in current_data}
                    # Calcular próximo ID
                    max_id = 0
                    if current_data:
                        max_id = max((int(r.get('id', 0)) for r in current_data if str(r.get('id', '0')).isdigit()), default=0)
                    
                    for rec in new_records:
                        if rec.get('nome_especie') in existing_names:
                            raise ValueError(f"UNIQUE constraint failed: nome_especie '{rec.get('nome_especie')}' já existe.")
                        
                        # Auto-increment ID
                        if 'id' not in rec or pd.isna(rec['id']):
                            max_id += 1
                            rec['id'] = max_id

                # 3. APPEND & SAVE
                current_data.extend(new_records)
                
                # Reuse the inner save logic but without re-locking since we hold the lock
                file_path = GenericRepository._get_file_path(table_name)
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(current_data, f, indent=4, ensure_ascii=False)
                
            logging.info(f"{len(new_records)} registros inseridos com sucesso em '{table_name}'.")

        except Exception as e:
            logging.error(f"Erro na transação de escrita em '{table_name}': {e}")
            raise

    @staticmethod
    def update_table(table_name: str, update_values: Dict[str, Any], where_conditions: Dict[str, Any]) -> None:
        """Atualiza registros no arquivo JSON com lock."""
        lock_path = GenericRepository._get_lock_path(table_name)
        lock = FileLock(str(lock_path))

        try:
            with lock.acquire(timeout=10):
                current_data = GenericRepository._load_data(table_name)
                updated_count = 0
                
                update_values_lower = {k.lower(): v for k, v in update_values.items()}
                where_conditions_lower = {k.lower(): v for k, v in where_conditions.items()}

                for row in current_data:
                    match = True
                    for wc_key, wc_val in where_conditions_lower.items():
                        if row.get(wc_key) != wc_val:
                            match = False
                            break
                    
                    if match:
                        for uv_key, uv_val in update_values_lower.items():
                            row[uv_key] = uv_val
                        updated_count += 1
                
                if updated_count > 0:
                    file_path = GenericRepository._get_file_path(table_name)
                    with open(file_path, 'w', encoding='utf-8') as f:
                        json.dump(current_data, f, indent=4, ensure_ascii=False)
                    logging.info(f"Tabela '{table_name}' atualizada com sucesso. {updated_count} registros afetados.")
                else:
                    logging.warning(f"Nenhum registro encontrado para atualização em '{table_name}'.")

        except Exception as e:
            logging.error(f"Erro ao atualizar '{table_name}': {e}")
            raise

    @staticmethod
    def delete_from_table(table_name: str, where_conditions: Dict[str, Any]) -> None:
        """Deleta registros do arquivo JSON com lock."""
        lock_path = GenericRepository._get_lock_path(table_name)
        lock = FileLock(str(lock_path))

        try:
            with lock.acquire(timeout=10):
                current_data = GenericRepository._load_data(table_name)
                initial_count = len(current_data)
                
                where_conditions_lower = {k.lower(): v for k, v in where_conditions.items()}

                new_data = []
                for row in current_data:
                    match = True
                    for wc_key, wc_val in where_conditions_lower.items():
                        if row.get(wc_key) != wc_val:
                            match = False
                            break
                    
                    if not match:
                        new_data.append(row)
                
                deleted_count = initial_count - len(new_data)
                
                if deleted_count > 0:
                    file_path = GenericRepository._get_file_path(table_name)
                    with open(file_path, 'w', encoding='utf-8') as f:
                        json.dump(new_data, f, indent=4, ensure_ascii=False)
                    logging.info(f"Registros da tabela '{table_name}' deletados com sucesso. {deleted_count} removidos.")
                else:
                    logging.warning(f"Nenhum registro encontrado para deleção em '{table_name}'.")

        except Exception as e:
            logging.error(f"Erro ao deletar de '{table_name}': {e}")
            raise