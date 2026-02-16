# NexlifyStreamlit: Empresa X White Label Edition

Este documento descreve a visão geral e a estrutura do projeto NexlifyStreamlit, o boilerplate oficial da **Empresa X** para aplicações Streamlit empresariais.

## 💎 Características Empresa X
O sistema é 100% "White Label", permitindo personalização total:
- **Títulos e Cabeçalhos**: Configuráveis via `config_settings.ini` (`app_title`, `app_header`).
- **Identidade Visual**: Tema padrão da Empresa X integrado com menus customizáveis.
- **DNA Original**: O NexlifyStreamlit nasce como uma folha em branco profissional, sem rastros de legados industriais ou clientes externos.

## 🏛️ Arquitetura e Engenharia
- **Clean Architecture**: Separação clara entre UI, Lógica de Negócio e Persistência.
- **Unit of Work**: Gerenciamento atômico de transações.
- **Segurança (RBAC)**: Controle de acesso baseado nos perfis clássicos da Empresa X (Sócio-Diretor, Gerente, Devs).
- **Multi-DB Suporte**: Schemas higienizados para SQLite, PostgreSQL, MySQL/MariaDB e SQL Server.

## 🚀 Como Iniciar
1. **Ambiente**: Instale as dependências via `pip install -r requirements.txt`.
2. **Setup**: Utilize `python instalacao/launch_devtools.py` para configurar.
3. **Database**: Para inicializar o banco com os dados da Empresa X, execute `python instalacao/reset_database_template.py`.
4. **Execução**: Rode com `streamlit run Home.py`.

## 🔒 Acesso Padrão
- **Administrador**: `admin` / `123`
- **Exemplo**: `lucas.delphi` / `123`

---
*Desenvolvido pela Empresa X - Qualidade e escalabilidade desde o primeiro dia.*
