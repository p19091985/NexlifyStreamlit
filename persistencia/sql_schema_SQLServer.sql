IF OBJECT_ID('perfil_acesso', 'U') IS NULL
BEGIN
    CREATE TABLE perfil_acesso (
        perfil_id INT IDENTITY(1,1) PRIMARY KEY,
        nome_perfil NVARCHAR(255) NOT NULL UNIQUE
    );
END
IF OBJECT_ID('usuarios', 'U') IS NULL
BEGIN
    CREATE TABLE usuarios (
        usuario_id INT IDENTITY(1,1) PRIMARY KEY,
        login_usuario NVARCHAR(255) NOT NULL UNIQUE,
        senha_criptografada NVARCHAR(MAX) NOT NULL,
        nome_completo NVARCHAR(MAX) NOT NULL,
        perfil_id INT NOT NULL,
        FOREIGN KEY (perfil_id) REFERENCES perfil_acesso(perfil_id)
    );
END
IF OBJECT_ID('pagina', 'U') IS NULL
BEGIN
    CREATE TABLE pagina (
        pagina_id INT IDENTITY(1,1) PRIMARY KEY,
        nome_arquivo NVARCHAR(255) NOT NULL UNIQUE,
        nome_amigavel NVARCHAR(MAX) NOT NULL
    );
END
IF OBJECT_ID('perfil_pagina_permissao', 'U') IS NULL
BEGIN
    CREATE TABLE perfil_pagina_permissao (
        permissao_id INT IDENTITY(1,1) PRIMARY KEY,
        perfil_id INT NOT NULL,
        pagina_id INT NOT NULL,
        FOREIGN KEY (perfil_id) REFERENCES perfil_acesso(perfil_id) ON DELETE CASCADE,
        FOREIGN KEY (pagina_id) REFERENCES pagina(pagina_id) ON DELETE CASCADE,
        UNIQUE(perfil_id, pagina_id)
    );
END
IF OBJECT_ID('especie_gatos', 'U') IS NULL
BEGIN
    CREATE TABLE especie_gatos (
        id INT IDENTITY(1,1) PRIMARY KEY,
        nome_especie NVARCHAR(255) NOT NULL UNIQUE,
        pais_origem NVARCHAR(MAX),
        temperamento NVARCHAR(MAX)
    );
END

-- DML: Perfis de Acesso
SET IDENTITY_INSERT perfil_acesso ON;
IF NOT EXISTS (SELECT 1 FROM perfil_acesso WHERE perfil_id = 1)
INSERT INTO perfil_acesso (perfil_id, nome_perfil) VALUES
	 (1, 'Administrador'),
	 (2, 'Diretoria'),
	 (3, N'Gerência de TI'),
	 (4, N'Coordenação'),
	 (5, N'Análise de Sistemas'),
	 (6, N'Programação'),
	 (7, 'Web/Design'),
	 (8, N'Testes/Homologação'),
	 (9, 'Infraestrutura'),
	 (10, N'Suporte Técnico'),
	 (11, 'Comercial/Vendas'),
	 (12, 'Administrativo/Financeiro');
SET IDENTITY_INSERT perfil_acesso OFF;

-- DML: Usuários (senha padrão: 123)
IF NOT EXISTS (SELECT 1 FROM usuarios WHERE login_usuario = 'admin')
INSERT INTO usuarios (login_usuario, senha_criptografada, nome_completo, perfil_id) VALUES
	 ('admin', '$2b$12$EzaobIi.BJeAbu3xbR0sr.2viD6cOJ9h.c7snQk9TYlnetxd3IhNG', 'Administrador do Sistema', 1),
	 ('carlos.diretor', '$2b$12$EzaobIi.BJeAbu3xbR0sr.2viD6cOJ9h.c7snQk9TYlnetxd3IhNG', N'Carlos Sócio', 2),
	 ('amanda.gerente', '$2b$12$EzaobIi.BJeAbu3xbR0sr.2viD6cOJ9h.c7snQk9TYlnetxd3IhNG', 'Amanda Gerente TI', 3),
	 ('roberto.coord', '$2b$12$EzaobIi.BJeAbu3xbR0sr.2viD6cOJ9h.c7snQk9TYlnetxd3IhNG', 'Roberto Coordenador', 4),
	 ('julia.analista', '$2b$12$EzaobIi.BJeAbu3xbR0sr.2viD6cOJ9h.c7snQk9TYlnetxd3IhNG', N'Júlia Analista Sênior', 5),
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
	 ('patricia.homol', '$2b$12$EzaobIi.BJeAbu3xbR0sr.2viD6cOJ9h.c7snQk9TYlnetxd3IhNG', N'Patrícia Homologação', 8),
	 ('ricardo.teste', '$2b$12$EzaobIi.BJeAbu3xbR0sr.2viD6cOJ9h.c7snQk9TYlnetxd3IhNG', 'Ricardo Testes', 8),
	 ('felipe.redes', '$2b$12$EzaobIi.BJeAbu3xbR0sr.2viD6cOJ9h.c7snQk9TYlnetxd3IhNG', 'Felipe Redes/Linux', 9),
	 ('diogo.nt', '$2b$12$EzaobIi.BJeAbu3xbR0sr.2viD6cOJ9h.c7snQk9TYlnetxd3IhNG', 'Diogo Servidores NT', 9),
	 ('suporte.joao', '$2b$12$EzaobIi.BJeAbu3xbR0sr.2viD6cOJ9h.c7snQk9TYlnetxd3IhNG', N'João Técnico', 10),
	 ('suporte.maria', '$2b$12$EzaobIi.BJeAbu3xbR0sr.2viD6cOJ9h.c7snQk9TYlnetxd3IhNG', N'Maria Técnica', 10),
	 ('suporte.jose', '$2b$12$EzaobIi.BJeAbu3xbR0sr.2viD6cOJ9h.c7snQk9TYlnetxd3IhNG', N'José Técnico', 10),
	 ('vendas.paulo', '$2b$12$EzaobIi.BJeAbu3xbR0sr.2viD6cOJ9h.c7snQk9TYlnetxd3IhNG', 'Paulo Vendas', 11),
	 ('vendas.clara', '$2b$12$EzaobIi.BJeAbu3xbR0sr.2viD6cOJ9h.c7snQk9TYlnetxd3IhNG', 'Clara Vendas', 11),
	 ('vendas.exec', '$2b$12$EzaobIi.BJeAbu3xbR0sr.2viD6cOJ9h.c7snQk9TYlnetxd3IhNG', 'Executivo de Contas', 11),
	 ('dp.bea', '$2b$12$EzaobIi.BJeAbu3xbR0sr.2viD6cOJ9h.c7snQk9TYlnetxd3IhNG', 'Beatriz DP', 12),
	 ('adm.fin', '$2b$12$EzaobIi.BJeAbu3xbR0sr.2viD6cOJ9h.c7snQk9TYlnetxd3IhNG', 'Financeiro', 12),
	 ('recepcao', '$2b$12$EzaobIi.BJeAbu3xbR0sr.2viD6cOJ9h.c7snQk9TYlnetxd3IhNG', 'Recepcionista', 12);

-- DML: Páginas
SET IDENTITY_INSERT pagina ON;
IF NOT EXISTS (SELECT 1 FROM pagina WHERE pagina_id = 1)
INSERT INTO pagina (pagina_id, nome_arquivo, nome_amigavel) VALUES
	 (1, N'01_🏠_Pagina_Inicial.py', N'Página Inicial'),
	 (2, N'02_📈_Painel_Analise_Iris.py', N'Análise Iris'),
	 (3, N'03_📈_Painel_Analise_Covertype.py', N'Análise Covertype'),
	 (4, N'04_🐱_Gatos_CRUD.py', N'Gestão de Gatos'),
	 (5, N'05_📋_Painel_Modelo.py', 'Painel Modelo'),
	 (6, N'06_👤_Gestao_Usuarios.py', N'Gestão de Usuários'),
	 (7, N'07_🔒_Gerenciar_Permissoes.py', N'Gerenciar Permissões'),
	 (8, N'08_📄_Gerenciar_Paginas.py', N'Gerenciar Páginas'),
	 (9, N'09_🎨_Editor_de_Tema.py', 'Editor de Tema'),
	 (10, N'10_✨_Alternar_Modos.py', 'Alternar Modos'),
	 (11, N'11_ℹ️_Sobre.py', 'Sobre');
SET IDENTITY_INSERT pagina OFF;

-- DML: Permissões
INSERT INTO perfil_pagina_permissao (perfil_id, pagina_id)
SELECT 1, pagina_id FROM pagina
WHERE NOT EXISTS (SELECT 1 FROM perfil_pagina_permissao WHERE perfil_id = 1 AND perfil_pagina_permissao.pagina_id = pagina.pagina_id);
INSERT INTO perfil_pagina_permissao (perfil_id, pagina_id)
SELECT 3, pagina_id FROM pagina
WHERE NOT EXISTS (SELECT 1 FROM perfil_pagina_permissao WHERE perfil_id = 3 AND perfil_pagina_permissao.pagina_id = pagina.pagina_id);
INSERT INTO perfil_pagina_permissao (perfil_id, pagina_id)
SELECT p.perfil_id, pg.pagina_id
FROM perfil_acesso p, pagina pg
WHERE p.perfil_id NOT IN (1, 3) AND pg.pagina_id IN (1, 6, 11)
AND NOT EXISTS (SELECT 1 FROM perfil_pagina_permissao ppp WHERE ppp.perfil_id = p.perfil_id AND ppp.pagina_id = pg.pagina_id);
INSERT INTO perfil_pagina_permissao (perfil_id, pagina_id)
SELECT p.perfil_id, pg.pagina_id
FROM perfil_acesso p, pagina pg
WHERE p.perfil_id IN (5, 6, 7, 9) AND pg.pagina_id IN (2, 3, 4, 5)
AND NOT EXISTS (SELECT 1 FROM perfil_pagina_permissao ppp WHERE ppp.perfil_id = p.perfil_id AND ppp.pagina_id = pg.pagina_id);
INSERT INTO perfil_pagina_permissao (perfil_id, pagina_id)
SELECT p.perfil_id, pg.pagina_id
FROM perfil_acesso p, pagina pg
WHERE p.perfil_id IN (2, 4) AND pg.pagina_id IN (2, 3)
AND NOT EXISTS (SELECT 1 FROM perfil_pagina_permissao ppp WHERE ppp.perfil_id = p.perfil_id AND ppp.pagina_id = pg.pagina_id);