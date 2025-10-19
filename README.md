# ✨ NexlifyStreamlit ✨ - Manual Técnico e Guia de Uso Definitivo

**NexlifyStreamlit** é uma plataforma de aplicação web avançada, evoluída de um sistema desktop, focada na aplicação rigorosa de padrões de projeto para garantir máxima **manutenibilidade**, **testabilidade** e **flexibilidade**. A arquitetura é estritamente em camadas, garantindo que a lógica de negócios e a camada de persistência sejam completamente agnósticas à interface do usuário construída com Streamlit.

Este documento é a referência canônica do projeto, servindo como um guia completo para desenvolvedores, arquitetos e administradores de sistema.

## 🎯 Principais Pilares e Recursos

- **Arquitetura Limpa (MVP Adaptado):** Separação estrita entre Interface (View), Lógica de UI (Controller/Presenter) e serviços de back-end, promovendo um baixo acoplamento e alta coesão.
- **Abstração de Persistência (Padrão Repository):** Suporte agnóstico a múltiplos SGBDs (SQLite, PostgreSQL, MariaDB/MySQL, SQL Server) através do SQLAlchemy Core, isolando o núcleo da aplicação dos detalhes do banco de dados.
- **Transações Atômicas (ACID):** A Camada de Serviço (DataService) gerencia operações de negócio complexas de forma atômica, garantindo a integridade dos dados e a rastreabilidade através de logs de auditoria.
- **Autenticação e RBAC (Role-Based Access Control):** Sistema de login seguro com hashing bcrypt e controle de acesso por perfil de usuário, garantindo que páginas e funcionalidades sejam acessíveis apenas a usuários autorizados.
- **Configuração Dinâmica e Centralizada:** O comportamento do sistema é controlado por *Feature Flags* no `config_settings.ini`, com validação de consistência na inicialização para operar em diferentes modos (Produção, Desenvolvimento Back-end, Desenvolvimento Front-end/Offline).
- **Segurança End-to-End:** Credenciais de banco de dados são criptografadas em repouso (Fernet), e senhas de usuário são armazenadas como hashes robustos (bcrypt).
- **Editor de Tema Dinâmico:** Permite a personalização visual da UI em tempo de execução, com salvamento das configurações para persistência.

## 🚀 Guia de Início Rápido (Para Usuários e Desenvolvedores)

Siga estes passos para configurar e executar o projeto.

### 1. Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes do Python)

### 2. Instalação

1. **Clone o Repositório:**
   ```bash
   git clone <URL_DO_REPOSITORIO> && cd <NOME_DA_PASTA>
   ```

2. **Crie e Ative um Ambiente Virtual:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. **Instale as Dependências:**
   Crie um arquivo `requirements.txt` com o conteúdo abaixo e execute:
   ```bash
   pip install -r requirements.txt
   ```
   Conteúdo do `requirements.txt`:
   ```
   streamlit
   pandas
   sqlalchemy
   bcrypt
   cryptography
   # Adicione o driver do seu banco de dados:
   # psycopg2-binary  # para PostgreSQL
   # PyMySQL          # para MySQL
   # mariadb          # para MariaDB
   # pymssql          # para SQL Server
   ```

### 3. Configuração (Método Fácil)

Utilize as ferramentas gráficas fornecidas para uma configuração rápida e sem erros.

1. **Execute o Lançador de Ferramentas:**
   ```bash
   python instalacao/launch_devtools.py
   ```

2. **Configure a Conexão (`banco.ini`):**
   - Na ferramenta, clique em **"🗃️ Configurar Conexão (banco.ini)"**.
   - Selecione o banco de dados que você deseja usar (ex: PostgreSQL) e clique em "Salvar".
   - Se o seu banco não for SQLite, você **precisará** criptografar as credenciais.

3. **Gere Credenciais e Hashes:**
   - Na ferramenta, clique em **"🔑 Gerar Credenciais / Hashes"**.
   - **Aba .ini:** Insira o usuário e senha **reais** do seu banco de dados, gere as credenciais e cole o resultado no `banco.ini`.
   - **Aba .sql:** Use esta aba para gerar hashes de senha para novos usuários nos seus scripts SQL.

4. **Ajuste as Flags (`config_settings.ini`):**
   - Na ferramenta, clique em **"⚙️ Configurar Flags (config.py)"**.
   - Ajuste os modos de operação conforme sua necessidade (ex: desabilitar o login durante o desenvolvimento).

### 4. Preparação do Banco de Dados

- Localize o script SQL correspondente ao seu SGBD na pasta `persistencia/` (ex: `sql_schema_Postgresql.sql`).
- Execute este script em seu SGBD para criar todas as tabelas e inserir os dados iniciais.

### 5. Execução

Com tudo configurado, inicie a aplicação:
```bash
streamlit run main.py
```

A aplicação será aberta no seu navegador. As credenciais padrão para o primeiro login são `admin` / `admin123`.

## 🏛️ Arquitetura Aprofundada e Filosofia de Design

A arquitetura foi concebida para maximizar o **desacoplamento** e a **coesão**. Cada camada tem uma responsabilidade única, permitindo que a UI ou o SGBD sejam trocados com impacto mínimo no núcleo de negócios.

### Diagrama da Arquitetura em Camadas

```mermaid
graph TD
    subgraph "Camada de Apresentação (View)"
        A[Interface Streamlit <br> `pages/*.py` <br> `components/*_view.py`]
    end

    subgraph "Camada de Controle (Controller/Presenter)"
        B[Lógica de Estado da UI <br> `components/*_controller.py`]
    end

    subgraph "Camada de Serviço (Service)"
        C[Orquestração de Transações <br> `persistencia/data_service.py`]
    end

    subgraph "Camada de Repositório (Repository)"
        D[Abstração de Acesso a Dados (CRUD) <br> `persistencia/repository.py`]
    end

    subgraph "Camada de Persistência (Engine)"
        E[SQLAlchemy Core Engine <br> `persistencia/database.py`]
    end

    subgraph "Banco de Dados"
        F[(SGBD <br> SQLite / PostgreSQL / etc.)]
    end

    A -->|Interação do Usuário| B
    B -->|Chama Lógica Complexa| C
    B -->|Chama CRUD Simples| D
    C -->|Usa Múltiplas Operações| D
    D -->|Executa Queries| E
    E -->|Conecta e Transaciona| F
```