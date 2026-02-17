<div align="center">

# ✨ NexlifyStreamlit ✨

<img src="https://img.shields.io/badge/python-3.9%2B-blue.svg" alt="Python Version">
<img src="https://img.shields.io/badge/framework-Streamlit_1.50-red" alt="Framework">
<img src="https://img.shields.io/badge/ORM-SQLAlchemy_2.0-green" alt="ORM">
<img src="https://img.shields.io/badge/architecture-Clean%20Architecture-brightgreen" alt="Architecture">
<img src="https://img.shields.io/badge/pattern-Unit%20of%20Work-blueviolet" alt="Pattern">
<img src="https://img.shields.io/badge/security-bcrypt%20%2B%20Fernet-orange" alt="Security">
<img src="https://img.shields.io/badge/databases-7%20engines-informational" alt="Databases">
<img src="https://img.shields.io/badge/license-MIT-lightgrey" alt="License">

**Um framework enterprise-grade para Streamlit com Clean Architecture, Unit of Work, RBAC e suporte multi-banco.**

*Template completo e pronto para produção — basta clonar, configurar e construir.*

</div>

---

## 📜 Índice

- [🎯 Filosofia](#-filosofia)
- [🏛️ Arquitetura](#️-arquitetura)
- [📁 Estrutura do Projeto](#-estrutura-do-projeto)
- [🛠️ Stack Tecnológica](#️-stack-tecnológica)
- [🚀 Início Rápido](#-início-rápido)
- [⚙️ Configuração](#️-configuração)
- [🗄️ Banco de Dados](#️-banco-de-dados)
- [🔐 Segurança e Autenticação](#-segurança-e-autenticação)
- [🔑 Credenciais do Template](#-credenciais-do-template)
- [📄 Criando Novas Páginas](#-criando-novas-páginas)
- [🔧 Ferramentas de Instalação](#-ferramentas-de-instalação)
- [🧪 Testes](#-testes)
- [📊 Páginas Incluídas](#-páginas-incluídas)
- [🤝 Contribuindo](#-contribuindo)
- [📝 Licença](#-licença)

---

## 🎯 Filosofia

O NexlifyStreamlit preenche a lacuna entre scripts simples de dados e aplicações web complexas. Ele serve como um **boilerplate avançado** para construir aplicações Streamlit escaláveis, seguras e com práticas profissionais de engenharia de software.

| Princípio | Implementação |
|-----------|---------------|
| **Clean Architecture** | Separação rigorosa entre UI (`app_pages/`), Lógica de Negócio (`components/`) e Acesso a Dados (`persistencia/repositorios/`) |
| **Unit of Work** | Gerenciamento atômico de transações com commit/rollback automático |
| **Database Agnostic** | Construído sobre SQLAlchemy 2.0, suportando **7 engines** de banco de dados |
| **Security First** | RBAC granular, hashing bcrypt, criptografia Fernet para credenciais |
| **Convention over Configuration** | Tudo funciona out-of-the-box com SQLite, sem setup extra necessário |

---

## 🏛️ Arquitetura

### Fluxo de Dados

```mermaid
graph TD
    subgraph "🖥️ Camada de Apresentação"
        UI["Streamlit Pages<br/><code>app_pages/*.py</code>"]
    end

    subgraph "🔒 Camada de Segurança"
        AUTH["Auth Guard<br/><code>st_check_session()</code><br/><code>check_access()</code>"]
        CRYPTO["Fernet Encryption<br/><code>security.py</code>"]
    end

    subgraph "⚙️ Camada de Serviço"
        SVC["Service Layer<br/><code>components/*.py</code>"]
    end

    subgraph "💾 Camada de Persistência"
        UOW["Unit of Work<br/><code>unit_of_work.py</code>"]
        REPO["Repositories<br/><code>repositorios/*.py</code>"]
        DB["DatabaseManager<br/><code>database.py</code>"]
    end

    subgraph "🗄️ Storage"
        SQLITE[(SQLite)]
        PG[(PostgreSQL)]
        MYSQL[(MySQL)]
        MSSQL[(SQL Server)]
        MORE["...+3 engines"]
    end

    UI --> AUTH
    AUTH --> SVC
    SVC --> UOW
    UOW --> REPO
    REPO --> DB
    DB --> SQLITE
    DB --> PG
    DB --> MYSQL
    DB --> MSSQL
    DB --> MORE
    CRYPTO -.-> DB
```

### Componentes Principais

| Componente | Caminho | Responsabilidade |
|-----------|--------|------------------|
| **Home** | `Home.py` | Entry point: login, inicialização do DB, roteamento de navegação |
| **Páginas** | `app_pages/` | Renderização pura de UI. Sem queries SQL diretas |
| **UnitOfWork** | `persistencia/unit_of_work.py` | Gerencia transações DB (commit/rollback) e expõe Repositories |
| **Repositories** | `persistencia/repositorios/` | Encapsula toda a lógica de acesso a dados (CRUD) |
| **BaseRepository** | `persistencia/repositorios/base.py` | Classe base com operações genéricas (query→DataFrame, raw SQL, scalar, insert, update, delete) |
| **DatabaseManager** | `persistencia/database.py` | Singleton que gerencia a engine SQLAlchemy e inicializa o schema |
| **Auth** | `persistencia/auth.py` | Autenticação com bcrypt e verificação de credenciais |
| **Security** | `persistencia/security.py` | Criptografia Fernet para senhas de banco em `banco.ini` |
| **Logger** | `persistencia/logger.py` | Sistema de logging com file handler e redirecionamento de stdout |
| **Config** | `config.py` + `config_settings.ini` | Configuração centralizada da aplicação |
| **Services** | `components/servicos_gerenciador.py` | Camada de serviço para lógica de negócio |
| **Utils** | `utils/st_utils.py` | Helpers de sessão e controle de acesso |

---

## 📁 Estrutura do Projeto

```
NexlifyStreamlit/
├── Home.py                          # 🏠 Entry point da aplicação
├── config.py                        # ⚙️ Configuração centralizada
├── config_settings.ini              # ⚙️ Parâmetros editáveis
├── banco.ini                        # 🗄️ Conexão com banco de dados
├── secret.key                       # 🔐 Chave Fernet (auto-gerada)
├── requirements.txt                 # 📦 Dependências Python
│
├── app_pages/                       # 📄 Páginas Streamlit (11 páginas)
│   ├── 01_🏠_Pagina_Inicial.py
│   ├── 02_📈_Painel_Analise_Iris.py
│   ├── 03_📈_Painel_Analise_Covertype.py
│   ├── 04_🐱_Gatos_CRUD.py
│   ├── 05_📋_Painel_Modelo.py
│   ├── 06_👤_Gestao_Usuarios.py
│   ├── 07_🔒_Gerenciar_Permissoes.py
│   ├── 08_📄_Gerenciar_Paginas.py
│   ├── 09_🎨_Editor_de_Tema.py
│   ├── 10_📖_Guia_Configuracao.py
│   └── 11_ℹ️_Sobre.py
│
├── persistencia/                    # 💾 Camada de dados
│   ├── database.py                  #   Singleton DatabaseManager
│   ├── unit_of_work.py              #   Padrão Unit of Work
│   ├── auth.py                      #   Autenticação bcrypt
│   ├── security.py                  #   Criptografia Fernet
│   ├── logger.py                    #   Sistema de logging
│   ├── repositorios/                #   Repositories
│   │   ├── base.py                  #     BaseRepository (CRUD genérico)
│   │   ├── usuario.py               #     UsuarioRepository
│   │   ├── paginas.py               #     PaginaRepository
│   │   ├── permissoes.py            #     PermissaoRepository
│   │   └── gatos.py                 #     GatosRepository (exemplo CRUD)
│   ├── sql_schema_SQLLite.sql       #   Schema SQLite (DDL + DML)
│   ├── sql_schema_Postgresql.sql    #   Schema PostgreSQL
│   ├── sql_schema_MariaDB_and_Mysql.sql  # Schema MySQL/MariaDB
│   └── sql_schema_SQLServer.sql     #   Schema SQL Server
│
├── components/                      # ⚙️ Camada de serviço
│   └── servicos_gerenciador.py      #   Service Manager
│
├── utils/                           # 🔧 Utilitários
│   └── st_utils.py                  #   Session & Access Control
│
├── instalacao/                      # 🛠️ Ferramentas de setup
│   ├── launch_devtools.py           #   Launcher de todas as ferramentas
│   ├── config_gui.py                #   Configurador geral (GUI)
│   ├── config_banco_gui.py          #   Configurador de banco (GUI)
│   ├── gerador_credenciais_gui.py   #   Encriptador de credenciais (GUI)
│   ├── gerador_schema_gui.py        #   Gerador de schema SQL (GUI)
│   ├── reset_database_template.py   #   Reset do banco para template
│   ├── limpeza_dev.py               #   Limpeza de artefatos dev
│   ├── reorder_pages_flat.py        #   Reordenador de páginas
│   ├── sql_schema_DDL.sql           #   DDL fonte (estrutura)
│   └── sql_schema_DML.sql           #   DML fonte (dados iniciais)
│
├── teste/                           # 🧪 Testes automatizados
│   ├── conftest.py                  #   Fixtures do pytest
│   ├── test_db_connection.py        #   Testes de conexão
│   ├── test_repos.py                #   Testes de repositórios
│   └── test_unit_of_work.py         #   Testes do UoW
│
├── logs/                            # 📋 Logs da aplicação
│   └── app.log
├── csv/                             # 📊 Dados CSV
└── .streamlit/                      # 🎨 Configuração do Streamlit
```

---

## 🛠️ Stack Tecnológica

| Categoria | Tecnologia | Versão |
|-----------|------------|--------|
| **Frontend** | Streamlit | 1.50+ |
| **Backend** | Python | 3.9+ |
| **ORM** | SQLAlchemy | 2.0+ |
| **Hashing** | bcrypt | 5.0 |
| **Criptografia** | cryptography (Fernet) | 46.0 |
| **Data Analysis** | Pandas, NumPy, Scikit-learn | Latest |
| **Visualização** | Plotly, Altair | Latest |
| **Testes** | pytest | 9.0 |
| **UI Components** | ttkbootstrap | 1.14 |

---

## 🚀 Início Rápido

### 1. Clone o Repositório

```bash
git clone https://github.com/your-org/NexlifyStreamlit.git
cd NexlifyStreamlit
```

### 2. Crie um Ambiente Virtual

```bash
python -m venv .venv
source .venv/bin/activate        # Linux/macOS
# .venv\Scripts\activate         # Windows
```

### 3. Instale as Dependências

```bash
pip install -r requirements.txt
```

### 4. Execute a Aplicação

```bash
streamlit run Home.py
```

> **Pronto!** Na primeira execução, o banco SQLite é inicializado automaticamente com todos os dados do template (perfis, usuários, páginas e permissões).

### 5. Faça Login

Use `admin` / `123` para acesso total, ou qualquer usuário da [tabela de credenciais](#-credenciais-do-template).

---

## ⚙️ Configuração

### `config_settings.ini`

Controla o comportamento global da aplicação:

```ini
[Settings]
database_enabled = True                    # Liga/desliga acesso ao banco
initialize_database_on_startup = True      # Auto-inicializa o schema na 1ª execução
redirect_console_to_log = False            # Redireciona stdout/stderr para logs
enable_theme_menu = False                  # Habilita menu de troca de tema
app_title = 🚀 Painel de Controle Moderno  # Título da aplicação
app_header = Sistema de Demonstração       # Subtítulo
```

### `banco.ini`

Define a conexão com o banco de dados. Por padrão, usa SQLite:

```ini
# Apenas descomente UM bloco de configuração por vez.

# ── SQLite (padrão) ──────────────
type = sqlite
path = nexlifyttk.db

# ── PostgreSQL ───────────────────
# type = postgresql
# host = localhost
# port = 5432
# dbname = nexlifydb
# user = <encrypted>
# password = <encrypted>
```

> **Nota:** Para bancos não-SQLite, as credenciais devem ser encriptadas com Fernet. Use a ferramenta `gerador_credenciais_gui.py` para isso.

### Variáveis Derivadas (`config.py`)

| Variável | Tipo | Padrão | Descrição |
|----------|------|--------|-----------|
| `DATABASE_ENABLED` | bool | `True` | Habilita acesso ao banco de dados |
| `INITIALIZE_DATABASE_ON_STARTUP` | bool | `True` | Auto-cria tabelas e dados na primeira execução |
| `REDIRECT_CONSOLE_TO_LOG` | bool | `False` | Redireciona print() para o sistema de logs |
| `ENABLE_THEME_MENU` | bool | `True` | Mostra o menu de temas na Home |
| `MAX_LOGIN_ATTEMPTS` | int | `3` | Limite de tentativas de login |
| `LOG_LEVEL` | str | `INFO` | Nível de log (DEBUG, INFO, WARNING, ERROR) |

---

## 🗄️ Banco de Dados

### Engines Suportadas

O `DatabaseManager` suporta **7 engines** via SQLAlchemy:

| Engine | Driver | String de Conexão |
|--------|--------|-------------------|
| **SQLite** | built-in | `sqlite:///path/to/db.db` |
| **PostgreSQL** | psycopg2 | `postgresql+psycopg2://user:pass@host:port/db` |
| **MySQL** | pymysql | `mysql+pymysql://user:pass@host:port/db` |
| **MariaDB** | mariadbconnector | `mariadb+mariadbconnector://user:pass@host:port/db` |
| **SQL Server** | pymssql | `mssql+pymssql://user:pass@host:port/db` |
| **Oracle** | oracledb | `oracle+oracledb://user:pass@host:port/db` |
| **Firebird** | fdb | `firebird+fdb://user:pass@host:port/db` |

> Para cada engine não-SQLite, instale o driver Python correspondente (ex: `pip install psycopg2-binary` para PostgreSQL).

### Schema do Banco

```mermaid
erDiagram
    perfil_acesso {
        int perfil_id PK
        text nome_perfil UK
    }
    usuarios {
        int usuario_id PK
        text login_usuario UK
        text senha_criptografada
        text nome_completo
        int perfil_id FK
    }
    pagina {
        int pagina_id PK
        text nome_arquivo UK
        text nome_amigavel
    }
    perfil_pagina_permissao {
        int permissao_id PK
        int perfil_id FK
        int pagina_id FK
    }
    especie_gatos {
        int id PK
        text nome_especie UK
        text pais_origem
        text temperamento
    }

    perfil_acesso ||--o{ usuarios : "has"
    perfil_acesso ||--o{ perfil_pagina_permissao : "grants"
    pagina ||--o{ perfil_pagina_permissao : "controlled by"
```

### Inicialização Automática

Na primeira execução com SQLite, o `DatabaseManager.initialize_database()`:
1. Detecta que o arquivo `.db` não existe ou está vazio
2. Lê o schema de `persistencia/sql_schema_SQLLite.sql`
3. Executa DDL (CREATE TABLE) + DML (INSERT dados iniciais)
4. Cria: 12 perfis, 28 usuários, 11 páginas e 72 permissões

### Unit of Work — Como Usar

```python
from persistencia.unit_of_work import UnitOfWork

# ✅ Uso correto — transação gerenciada automaticamente
with UnitOfWork() as uow:
    # Ler dados
    users_df = uow.usuarios.get_all_users()
    
    # Inserir dados
    uow.gatos.save_cat(nome="Siamês", pais="Tailândia", temperamento="Dócil")
    
    # Atualizar dados
    uow.usuarios.update_password(user_id=1, new_hash="...")
    
# ✅ Commit automático se nenhum erro ocorrer
# ✅ Rollback automático se uma exceção for lançada
# ✅ Conexão fechada automaticamente no finally
```

### Repositories Disponíveis

| Repository | Acesso via UoW | Responsabilidade |
|------------|---------------|------------------|
| `UsuarioRepository` | `uow.usuarios` | CRUD de usuários, busca por login |
| `PermissaoRepository` | `uow.permissoes` | Gerenciamento de permissões perfil↔página |
| `PaginaRepository` | `uow.paginas` | CRUD de páginas, busca de roles permitidas |
| `GatosRepository` | `uow.gatos` | CRUD exemplo para espécies de gatos |

---

## 🔐 Segurança e Autenticação

### Camadas de Segurança

```mermaid
graph LR
    A["👤 Usuário"] --> B["🔐 Login<br/>(bcrypt verify)"]
    B --> C["🎫 Sessão<br/>(st.session_state)"]
    C --> D["🛡️ RBAC Guard<br/>(check_access)"]
    D --> E["📄 Página"]
```

### 1. Autenticação (bcrypt)

- Senhas armazenadas como hashes bcrypt no banco
- Verificação via `auth.verify_user_credentials()`
- Limite de tentativas configurável (`MAX_LOGIN_ATTEMPTS = 3`)

### 2. Sessão

- Dados do usuário logado em `st.session_state.user_info`:
  ```python
  {
      "username": "admin",
      "name": "Administrador do Sistema",
      "access_level": "Administrador"
  }
  ```
- Botão de logout no sidebar limpa toda a sessão

### 3. Controle de Acesso (RBAC)

Cada página é protegida por dois guards obrigatórios:

```python
from utils.st_utils import st_check_session, check_access
from components import servicos_gerenciador as servico

st_check_session()  # Verifica se o usuário está logado

# Busca do banco quais perfis têm acesso a esta página
allowed_roles = servico.get_allowed_roles_for_page(Path(__file__).name)
check_access(allowed_roles)  # Bloqueia se o perfil não estiver na lista
```

### 4. Criptografia de Credenciais (Fernet)

Para bancos não-SQLite, as credenciais em `banco.ini` são encriptadas:

```bash
python instalacao/gerador_credenciais_gui.py  # Interface gráfica para encriptar
```

- Chave simétrica armazenada em `secret.key` (auto-gerado)
- Encriptação/decriptação via `security.encrypt_message()` / `security.decrypt_message()`

---

## 🔑 Credenciais do Template

> **Senha padrão para todos os usuários:** `123`

Este é um projeto template/demo. Todos os usuários abaixo são pré-configurados no schema SQL.

| Login | Nome Completo | Perfil | Nível de Acesso |
|-------|---------------|--------|-----------------|
| `admin` | Administrador do Sistema | Administrador | 🔓 Acesso Total |
| `carlos.diretor` | Carlos Sócio | Diretoria | Dashboards + Básico |
| `amanda.gerente` | Amanda Gerente TI | Gerência de TI | 🔓 Acesso Total |
| `roberto.coord` | Roberto Coordenador | Coordenação | Dashboards + Básico |
| `julia.analista` | Júlia Analista Sênior | Análise de Sistemas | Análise + Básico |
| `lucas.delphi` | Lucas Programador Delphi | Programação | Análise + Básico |
| `pedro.vb` | Pedro Programador VB | Programação | Análise + Básico |
| `tiago.java` | Tiago Programador Java | Programação | Análise + Básico |
| `rafael.prog` | Rafael Programador | Programação | Análise + Básico |
| `bruno.prog` | Bruno Programador | Programação | Análise + Básico |
| `ana.web` | Ana Webdesigner | Web/Design | Análise + Básico |
| `mariana.web` | Mariana Webmaster | Web/Design | Análise + Básico |
| `carol.html` | Carol HTML | Web/Design | Análise + Básico |
| `gabriel.flash` | Gabriel Flash Designer | Web/Design | Análise + Básico |
| `fernanda.teste` | Fernanda Testes | Testes/Homologação | Básico |
| `patricia.homol` | Patrícia Homologação | Testes/Homologação | Básico |
| `ricardo.teste` | Ricardo Testes | Testes/Homologação | Básico |
| `felipe.redes` | Felipe Redes/Linux | Infraestrutura | Análise + Básico |
| `diogo.nt` | Diogo Servidores NT | Infraestrutura | Análise + Básico |
| `suporte.joao` | João Técnico | Suporte Técnico | Básico |
| `suporte.maria` | Maria Técnica | Suporte Técnico | Básico |
| `suporte.jose` | José Técnico | Suporte Técnico | Básico |
| `vendas.paulo` | Paulo Vendas | Comercial/Vendas | Básico |
| `vendas.clara` | Clara Vendas | Comercial/Vendas | Básico |
| `vendas.exec` | Executivo de Contas | Comercial/Vendas | Básico |
| `dp.bea` | Beatriz DP | Adm/Financeiro | Básico |
| `adm.fin` | Financeiro | Adm/Financeiro | Básico |
| `recepcao` | Recepcionista | Adm/Financeiro | Básico |

**Legenda dos Níveis de Acesso:**

| Nível | Páginas |
|-------|---------|
| 🔓 **Acesso Total** | Todas as 11 páginas |
| **Dashboards + Básico** | Home, Análise Iris, Análise Covertype, Gestão Usuários, Sobre |
| **Análise + Básico** | Home, Análise Iris, Análise Covertype, Gatos CRUD, Painel Modelo, Gestão Usuários, Sobre |
| **Básico** | Home, Gestão Usuários, Sobre |

---

## 📄 Criando Novas Páginas

### Passo a Passo

**1. Crie o arquivo** em `app_pages/` seguindo a convenção de nomenclatura:

```
NN_EMOJI_Nome_Da_Pagina.py
```

Exemplo: `12_📊_Relatorio_Vendas.py`

**2. Use o template padrão:**

```python
import streamlit as st
from pathlib import Path
from utils.st_utils import st_check_session, check_access
from components import servicos_gerenciador as servico

st.set_page_config(page_title='Relatório de Vendas', layout='wide')
st_check_session()

try:
    allowed_roles = servico.get_allowed_roles_for_page(Path(__file__).name)
    check_access(allowed_roles)
except Exception as e:
    st.error(f'Erro ao verificar permissões: {e}')
    st.stop()

# ── Seu código aqui ──
st.title('📊 Relatório de Vendas')

from persistencia.unit_of_work import UnitOfWork

with UnitOfWork() as uow:
    # Use os repositories via uow
    dados = uow.paginas.get_all_pages()
    st.dataframe(dados)
```

**3. Registre a página no banco** via SQL ou pela tela de Gerenciar Páginas:

```sql
INSERT INTO pagina (nome_arquivo, nome_amigavel)
VALUES ('12_📊_Relatorio_Vendas.py', 'Relatório de Vendas');
```

**4. Atribua permissões** via SQL ou pela tela de Gerenciar Permissões:

```sql
-- Dar acesso ao Admin (perfil 1) e Diretoria (perfil 2)
INSERT INTO perfil_pagina_permissao (perfil_id, pagina_id)
VALUES (1, 12), (2, 12);
```

### Criando um Novo Repository

**1. Crie o arquivo** em `persistencia/repositorios/`:

```python
# persistencia/repositorios/vendas.py
from .base import BaseRepository

class VendasRepository(BaseRepository):
    def get_all_vendas(self):
        return self._execute_query_to_dataframe(
            "SELECT * FROM vendas ORDER BY data_venda DESC"
        )
    
    def save_venda(self, cliente, valor):
        self._execute_raw_sql(
            "INSERT INTO vendas (cliente, valor) VALUES (:cliente, :valor)",
            {"cliente": cliente, "valor": valor}
        )
```

**2. Registre no UnitOfWork** (`persistencia/unit_of_work.py`):

```python
from persistencia.repositorios.vendas import VendasRepository

class UnitOfWork:
    def __enter__(self):
        # ... existing code ...
        self.vendas = VendasRepository(self.connection)  # Adicione aqui
        return self
```

**3. Use nas páginas:**

```python
with UnitOfWork() as uow:
    vendas_df = uow.vendas.get_all_vendas()
    st.dataframe(vendas_df)
```

---

## 🔧 Ferramentas de Instalação

O diretório `instalacao/` contém ferramentas gráficas (tkinter) para configuração:

```bash
# Launcher central — abre todas as ferramentas
python instalacao/launch_devtools.py
```

| Ferramenta | Comando | Descrição |
|------------|---------|-----------|
| **DevTools Launcher** | `launch_devtools.py` | Menu central com acesso a todas as ferramentas |
| **Config Geral** | `config_gui.py` | Edita `config_settings.ini` via interface gráfica |
| **Config Banco** | `config_banco_gui.py` | Configura `banco.ini` com suporte a encriptação |
| **Encriptador** | `gerador_credenciais_gui.py` | Gera/encripta credenciais de banco com Fernet |
| **Gerador Schema** | `gerador_schema_gui.py` | Concatena DDL + DML → `sql_schema_SQLLite.sql` |
| **Reset DB** | `reset_database_template.py` | Reseta o banco ao estado template (28 usuários, senha `123`) |
| **Limpeza Dev** | `limpeza_dev.py` | Remove `__pycache__`, `.pyc`, logs e artefatos de desenvolvimento |
| **Reordenar Páginas** | `reorder_pages_flat.py` | Renumera os prefixos dos arquivos em `app_pages/` |

### Gerando o Schema Combinado

O arquivo `persistencia/sql_schema_SQLLite.sql` é gerado a partir de:
- `instalacao/sql_schema_DDL.sql` — Definição de tabelas (CREATE TABLE)
- `instalacao/sql_schema_DML.sql` — Dados iniciais (INSERT)

Para regenerar após alterações:
```bash
python instalacao/gerador_schema_gui.py
```

---

## 🧪 Testes

O projeto inclui testes automatizados com **pytest** cobrindo conexão, UoW e repositories:

```bash
# Executar todos os testes
python -m pytest teste/ -v

# Executar apenas testes de conexão
python -m pytest teste/test_db_connection.py -v
```

### Cobertura dos Testes

| Arquivo | Testes | O que cobre |
|---------|--------|-------------|
| `test_db_connection.py` | 2 | Fixture de conexão, Singleton do DatabaseManager |
| `test_repos.py` | 2 | CRUD de Gatos (save/get/update/delete), Permissões de página |
| `test_unit_of_work.py` | 2 | Context manager do UoW, Inicialização de repositories |

> Os testes usam um banco SQLite **in-memory** (`:memory:`), sem afetar o banco de produção.

---

## 📊 Páginas Incluídas

| # | Página | Descrição | Acesso Mínimo |
|---|--------|-----------|---------------|
| 01 | 🏠 **Página Inicial** | Dashboard de boas-vindas | Todos |
| 02 | 📈 **Análise Iris** | Dashboard com dataset Iris (classificação ML) | Análise+ |
| 03 | 📈 **Análise Covertype** | Dashboard com dataset Covertype (ML avançado) | Análise+ |
| 04 | 🐱 **Gatos CRUD** | Exemplo completo de CRUD com UoW e Repository | Análise+ |
| 05 | 📋 **Painel Modelo** | Template de página modelo para referência | Análise+ |
| 06 | 👤 **Gestão de Usuários** | Criar, editar, excluir usuários e alterar senhas | Todos |
| 07 | 🔒 **Gerenciar Permissões** | Atribuir/revogar permissões perfil↔página | Admin/Gerente |
| 08 | 📄 **Gerenciar Páginas** | Registrar/editar/remover páginas do sistema | Admin/Gerente |
| 09 | 🎨 **Editor de Tema** | Galeria de 30+ temas predefinidos com preview ao vivo | Admin/Gerente |
| 10 | 📖 **Guia de Configuração** | Documentação das flags de configuração do sistema | Admin/Gerente |
| 11 | ℹ️ **Sobre** | Informações sobre o sistema e versão | Todos |

---

## 🤝 Contribuindo

1. **Crie uma Página**: Adicione um novo arquivo em `app_pages/` seguindo o [template](#-criando-novas-páginas)
2. **Use o UnitOfWork**: Nunca importe `DatabaseManager` diretamente — use `with UnitOfWork() as uow:`
3. **Registre Permissões**: Cadastre a nova página no banco para controle de acesso
4. **Escreva Testes**: Adicione testes relevantes em `teste/`
5. **Siga a Arquitetura**: UI → Service → UoW → Repository → DB

### Regras de Ouro

> - **Páginas** nunca fazem queries SQL diretas
> - **Repositories** nunca conhecem Streamlit
> - **UnitOfWork** gerencia todas as transações
> - **Toda página** precisa de `st_check_session()` + `check_access()`

---

## 📝 Licença

Licenciado sob a [MIT License](LICENSE).

---

<div align="center">

**Feito com ❤️ usando Streamlit + Clean Architecture**

*NexlifyStreamlit — O template profissional para aplicações Streamlit enterprise-grade.*

</div>