from sqlalchemy import text
from persistencia.repositorios.base import BaseRepository
import pandas as pd
import logging
log = logging.getLogger(__name__)

class GatosRepository(BaseRepository):

    def get_all_gatos(self) -> pd.DataFrame:
        query = 'SELECT * FROM especie_gatos'
        return self._execute_query_to_dataframe(query)

    def save_gato(self, data: dict, gato_id: int=None) -> bool:
        if gato_id:
            return self._update_table('especie_gatos', data, {'id': gato_id})
        else:
            return self._write_dataframe_to_table(pd.DataFrame([data]), 'especie_gatos')

    def delete_gato(self, gato_id: int) -> bool:
        return self._delete_from_table('especie_gatos', {'id': gato_id})