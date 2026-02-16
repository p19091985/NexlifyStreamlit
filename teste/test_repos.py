import pytest
from persistencia.unit_of_work import UnitOfWork
from sqlalchemy import text

def test_gatos_repository_crud():
    with UnitOfWork() as uow:
        
        data = {'nome_especie': 'Siames', 'pais_origem': 'Tailandia', 'temperamento': 'Vocal'}
        uow.gatos.save_gato(data)
        
    with UnitOfWork() as uow:
        
        df = uow.gatos.get_all_gatos()
        print(f"DEBUG GATOS COLS: {df.columns}")
        assert len(df) == 1
        assert df.iloc[0]['nome_especie'] == 'Siames'
        
        
        
        if 'id' in df.columns:
            gato_id = int(df.iloc[0]['id'])
            data_update = {'nome_especie': 'Siames Moderno', 'pais_origem': 'Tailandia', 'temperamento': 'Ativo'}
            uow.gatos.save_gato(data_update, gato_id)
        else:
            pytest.fail(f"Column 'id' missing in DF. Cols: {df.columns}")
        
    with UnitOfWork() as uow:
        df = uow.gatos.get_all_gatos()
        assert df.iloc[0]['nome_especie'] == 'Siames Moderno'
        
        gato_id = int(df.iloc[0]['id'])
        uow.gatos.delete_gato(gato_id)
        
    with UnitOfWork() as uow:
        df = uow.gatos.get_all_gatos()
        assert len(df) == 0

def test_pagina_repository_permissions(engine):
    
    with engine.connect() as conn:
        try:
            conn.execute(text("INSERT INTO pagina (nome_arquivo, nome_amigavel) VALUES ('01_Test.py', 'Test Page')"))
            conn.commit()
        except Exception as e:
            
            pass

    with UnitOfWork() as uow:
        
        roles = uow.paginas.get_allowed_roles_for_page('01_Test.py')
        assert roles is not None
