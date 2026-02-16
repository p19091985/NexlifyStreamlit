PRAGMA foreign_keys=ON;
BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS perfil_acesso (
    perfil_id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_perfil TEXT NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS usuarios (
    usuario_id INTEGER PRIMARY KEY AUTOINCREMENT,
    login_usuario TEXT NOT NULL UNIQUE,
    senha_criptografada TEXT NOT NULL,
    nome_completo TEXT NOT NULL,
    perfil_id INTEGER NOT NULL,
    FOREIGN KEY (perfil_id) REFERENCES perfil_acesso(perfil_id)
);
CREATE TABLE IF NOT EXISTS pagina (
    pagina_id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_arquivo TEXT NOT NULL UNIQUE,
    nome_amigavel TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS perfil_pagina_permissao (
    permissao_id INTEGER PRIMARY KEY AUTOINCREMENT,
    perfil_id INTEGER NOT NULL,
    pagina_id INTEGER NOT NULL,
    FOREIGN KEY (perfil_id) REFERENCES perfil_acesso(perfil_id) ON DELETE CASCADE,
    FOREIGN KEY (pagina_id) REFERENCES pagina(pagina_id) ON DELETE CASCADE,
    UNIQUE(perfil_id, pagina_id)
);
CREATE TABLE IF NOT EXISTS especie_gatos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_especie TEXT NOT NULL UNIQUE,
    pais_origem TEXT,
    temperamento TEXT
);