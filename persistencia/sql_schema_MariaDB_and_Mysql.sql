CREATE TABLE IF NOT EXISTS perfil_acesso (
    perfil_id INT AUTO_INCREMENT PRIMARY KEY,
    nome_perfil VARCHAR(255) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS usuarios (
    usuario_id INT AUTO_INCREMENT PRIMARY KEY,
    login_usuario VARCHAR(255) NOT NULL UNIQUE,
    senha_criptografada TEXT NOT NULL,
    nome_completo TEXT NOT NULL,
    perfil_id INT NOT NULL,
    FOREIGN KEY (perfil_id) REFERENCES perfil_acesso(perfil_id)
);
CREATE TABLE IF NOT EXISTS pagina (
    pagina_id INT AUTO_INCREMENT PRIMARY KEY,
    nome_arquivo VARCHAR(255) NOT NULL UNIQUE,
    nome_amigavel TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS perfil_pagina_permissao (
    permissao_id INT AUTO_INCREMENT PRIMARY KEY,
    perfil_id INT NOT NULL,
    pagina_id INT NOT NULL,
    FOREIGN KEY (perfil_id) REFERENCES perfil_acesso(perfil_id) ON DELETE CASCADE,
    FOREIGN KEY (pagina_id) REFERENCES pagina(pagina_id) ON DELETE CASCADE,
    UNIQUE(perfil_id, pagina_id)
);
CREATE TABLE IF NOT EXISTS especie_gatos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome_especie VARCHAR(255) NOT NULL UNIQUE,
    pais_origem TEXT,
    temperamento TEXT
);
INSERT INTO perfil_acesso (perfil_id, nome_perfil) VALUES
	 (1, 'Administrador Global'),
	 (2, 'Sócio-Diretor'),
	 (3, 'Gerente de Informática'),
	 (4, 'Coordenador de Desenvolvimento'),
	 (5, 'Analista de Sistemas Sênior'),
	 (6, 'Programador Delphi / VB'),
	 (7, 'Webmaster / Webdesigner'),
	 (8, 'Analista de Testes'),
	 (9, 'Analista de Suporte / Redes'),
	 (10, 'Técnico de Informática'),
	 (11, 'Consultor Comercial'),
	 (12, 'Auxiliar Administrativo / DP');
INSERT INTO usuarios (login_usuario, senha_criptografada, nome_completo, perfil_id) VALUES
	 ('admin', '$2b$12$EzaobIi.BJeAbu3xbR0sr.2viD6cOJ9h.c7snQk9TYlnetxd3IhNG', 'Administrador do Sistema', 1),
	 ('carlos.diretor', '$2b$12$EzaobIi.BJeAbu3xbR0sr.2viD6cOJ9h.c7snQk9TYlnetxd3IhNG', 'Carlos Sócio', 2),
	 ('amanda.gerente', '$2b$12$EzaobIi.BJeAbu3xbR0sr.2viD6cOJ9h.c7snQk9TYlnetxd3IhNG', 'Amanda Gerente TI', 3),
	 ('roberto.coord', '$2b$12$EzaobIi.BJeAbu3xbR0sr.2viD6cOJ9h.c7snQk9TYlnetxd3IhNG', 'Roberto Coordenador', 4),
	 ('julia.analista', '$2b$12$EzaobIi.BJeAbu3xbR0sr.2viD6cOJ9h.c7snQk9TYlnetxd3IhNG', 'Júlia Analista Sênior', 5),
	 ('lucas.delphi', '$2b$12$EzaobIi.BJeAbu3xbR0sr.2viD6cOJ9h.c7snQk9TYlnetxd3IhNG', 'Lucas Programador Delphi', 6),
	 ('pedro.vb', '$2b$12$EzaobIi.BJeAbu3xbR0sr.2viD6cOJ9h.c7snQk9TYlnetxd3IhNG', 'Pedro Programador VB', 6),
	 ('tiago.java', '$2b$12$EzaobIi.BJeAbu3xbR0sr.2viD6cOJ9h.c7snQk9TYlnetxd3IhNG', 'Tiago Programador Java', 6),
	 ('rafael.prog', '$2b$12$EzaobIi.BJeAbu3xbR0sr.2viD6cOJ9h.c7snQk9TYlnetxd3IhNG', 'Rafael Programador', 6),
	 ('bruno.prog', '$2b$12$EzaobIi.BJeAbu3xbR0sr.2viD6cOJ9h.c7snQk9TYlnetxd3IhNG', 'Bruno Programador', 6),
	 ('ana.web', '$2b$12$EzaobIi.BJeAbu3xbR0sr.2viD6cOJ9h.c7snQk9TYlnetxd3IhNG', 'Ana Webdesigner', 7),
	 ('mariana.web', '$2b$12$EzaobIi.BJeAbu3xbR0sr.2viD6cOJ9h.c7snQk9TYlnetxd3IhNG', 'Mariana Webmaster', 7),
	 ('carol.html', '$2b$12$EzaobIi.BJeAbu3xbR0sr.2viD6cOJ9h.c7snQk9TYlnetxd3IhNG', 'Carol HTML', 7),
	 ('gabriel.flash', '$2b$12$EzaobIi.BJeAbu3xbR0sr.2viD6cOJ9h.c7snQk9TYlnetxd3IhNG', 'Gabriel Flash Designer', 7),
	 ('fernanda.teste', '$2b$12$EzaobIi.BJeAbu3xbR0sr.2viD6cOJ9h.c7snQk9TYlnetxd3IhNG', 'Fernanda Testes', 8),
	 ('patricia.homol', '$2b$12$EzaobIi.BJeAbu3xbR0sr.2viD6cOJ9h.c7snQk9TYlnetxd3IhNG', 'Patrícia Homologação', 8),
	 ('ricardo.teste', '$2b$12$EzaobIi.BJeAbu3xbR0sr.2viD6cOJ9h.c7snQk9TYlnetxd3IhNG', 'Ricardo Testes', 8),
	 ('felipe.redes', '$2b$12$EzaobIi.BJeAbu3xbR0sr.2viD6cOJ9h.c7snQk9TYlnetxd3IhNG', 'Felipe Redes/Linux', 9),
	 ('diogo.nt', '$2b$12$EzaobIi.BJeAbu3xbR0sr.2viD6cOJ9h.c7snQk9TYlnetxd3IhNG', 'Diogo Servidores NT', 9),
	 ('suporte.joao', '$2b$12$EzaobIi.BJeAbu3xbR0sr.2viD6cOJ9h.c7snQk9TYlnetxd3IhNG', 'João Técnico', 10),
	 ('suporte.maria', '$2b$12$EzaobIi.BJeAbu3xbR0sr.2viD6cOJ9h.c7snQk9TYlnetxd3IhNG', 'Maria Técnica', 10),
	 ('suporte.jose', '$2b$12$EzaobIi.BJeAbu3xbR0sr.2viD6cOJ9h.c7snQk9TYlnetxd3IhNG', 'José Técnico', 10),
	 ('vendas.paulo', '$2b$12$EzaobIi.BJeAbu3xbR0sr.2viD6cOJ9h.c7snQk9TYlnetxd3IhNG', 'Paulo Vendas', 11),
	 ('vendas.clara', '$2b$12$EzaobIi.BJeAbu3xbR0sr.2viD6cOJ9h.c7snQk9TYlnetxd3IhNG', 'Clara Vendas', 11),
	 ('vendas.exec', '$2b$12$EzaobIi.BJeAbu3xbR0sr.2viD6cOJ9h.c7snQk9TYlnetxd3IhNG', 'Executivo de Contas', 11),
	 ('dp.bea', '$2b$12$EzaobIi.BJeAbu3xbR0sr.2viD6cOJ9h.c7snQk9TYlnetxd3IhNG', 'Beatriz DP', 12),
	 ('adm.fin', '$2b$12$EzaobIi.BJeAbu3xbR0sr.2viD6cOJ9h.c7snQk9TYlnetxd3IhNG', 'Financeiro', 12),
	 ('recepcao', '$2b$12$EzaobIi.BJeAbu3xbR0sr.2viD6cOJ9h.c7snQk9TYlnetxd3IhNG', 'Recepcionista', 12);
INSERT INTO pagina (pagina_id, nome_arquivo, nome_amigavel) VALUES
	 (1, '01_🏠_Pagina_Inicial.py','Página Inicial'),
	 (2, '02_📈_Painel_Analise_Iris.py','Análise Iris'),
	 (3, '03_📈_Painel_Analise_Covertype.py','Análise Covertype'),
	 (4, '04_🐱_Gatos_CRUD.py','Gestão de Gatos'),
	 (5, '05_📋_Painel_Modelo.py','Painel Modelo'),
	 (6, '06_👤_Gestao_Usuarios.py','Gestão de Usuários'),
	 (7, '07_🔒_Gerenciar_Permissoes.py','Gerenciar Permissões'),
	 (8, '08_📄_Gerenciar_Paginas.py','Gerenciar Páginas'),
	 (9, '09_🎨_Editor_de_Tema.py','Editor de Tema'),
	 (10, '10_✨_Alternar_Modos.py','Alternar Modos'),
	 (11, '11_ℹ️_Sobre.py','Sobre');
INSERT IGNORE INTO perfil_pagina_permissao (perfil_id, pagina_id) SELECT 1, pagina_id FROM pagina;
INSERT IGNORE INTO perfil_pagina_permissao (perfil_id, pagina_id) SELECT 3, pagina_id FROM pagina;
INSERT IGNORE INTO perfil_pagina_permissao (perfil_id, pagina_id)
SELECT p.perfil_id, pg.pagina_id
FROM perfil_acesso p, pagina pg
WHERE p.perfil_id NOT IN (1, 3) AND pg.pagina_id IN (1, 6, 11);
INSERT IGNORE INTO perfil_pagina_permissao (perfil_id, pagina_id)
SELECT p.perfil_id, pg.pagina_id
FROM perfil_acesso p, pagina pg
WHERE p.perfil_id IN (5, 6, 7, 8, 9) AND pg.pagina_id IN (2, 3, 4, 5);
INSERT IGNORE INTO perfil_pagina_permissao (perfil_id, pagina_id)
SELECT p.perfil_id, pg.pagina_id
FROM perfil_acesso p, pagina pg
WHERE p.perfil_id IN (2, 4) AND pg.pagina_id IN (2, 3);