import sys
import os
import pytest
from sqlalchemy import create_engine, text, event
from sqlalchemy.pool import StaticPool


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import config
from persistencia.database import DatabaseManager
from persistencia.unit_of_work import UnitOfWork


config.DATABASE_URL = 'sqlite:///:memory:'
config.DATABASE_ENABLED = True

@pytest.fixture(scope='session')
def engine():
    
    db_engine = create_engine(
        config.DATABASE_URL, 
        connect_args={'check_same_thread': False}, 
        poolclass=StaticPool
    )
    
    
    with db_engine.connect() as conn:
        statements = [
            "CREATE TABLE IF NOT EXISTS perfil_acesso (perfil_id INTEGER PRIMARY KEY AUTOINCREMENT, nome_perfil TEXT NOT NULL UNIQUE)",
            "CREATE TABLE IF NOT EXISTS usuarios (usuario_id INTEGER PRIMARY KEY AUTOINCREMENT, login_usuario TEXT NOT NULL UNIQUE, senha_criptografada TEXT NOT NULL, nome_completo TEXT NOT NULL, perfil_id INTEGER NOT NULL, FOREIGN KEY (perfil_id) REFERENCES perfil_acesso(perfil_id))",
            "CREATE TABLE IF NOT EXISTS pagina (pagina_id INTEGER PRIMARY KEY AUTOINCREMENT, nome_arquivo TEXT NOT NULL UNIQUE, nome_amigavel TEXT NOT NULL)",
            "CREATE TABLE IF NOT EXISTS perfil_pagina_permissao (permissao_id INTEGER PRIMARY KEY AUTOINCREMENT, perfil_id INTEGER NOT NULL, pagina_id INTEGER NOT NULL, FOREIGN KEY (perfil_id) REFERENCES perfil_acesso(perfil_id) ON DELETE CASCADE, FOREIGN KEY (pagina_id) REFERENCES pagina(pagina_id) ON DELETE CASCADE, UNIQUE(perfil_id, pagina_id))",
            "CREATE TABLE IF NOT EXISTS especie_gatos (id INTEGER PRIMARY KEY AUTOINCREMENT, nome_especie TEXT NOT NULL UNIQUE, pais_origem TEXT, temperamento TEXT)"
        ]
        
        for stmt in statements:
            conn.execute(text(stmt))
        conn.commit()
    
    DatabaseManager._engine = db_engine
    return db_engine

@pytest.fixture(autouse=True)
def version_reset(engine):
    
    pass

@pytest.fixture
def uow(engine):
    
    
    return UnitOfWork()
