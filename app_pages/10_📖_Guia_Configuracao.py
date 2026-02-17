import streamlit as st
from utils.st_utils import st_check_session, check_access
from pathlib import Path
from components import servicos_gerenciador as servico
st.set_page_config(page_title='Guia de Configuração', layout='wide', page_icon='📖')
st_check_session()
try:
    allowed_roles = servico.get_allowed_roles_for_page(Path(__file__).name)
    check_access(allowed_roles)
except Exception as e:
    st.error(f'Erro ao verificar permissões: {e}')
    st.stop()
st.header('📖 Guia de Configuração')
st.markdown('---')
st.info('\n    Esta aplicação oferece flexibilidade através de flags de configuração no arquivo `config.py`.\n    Essas flags permitem ajustar o comportamento do sistema para diferentes ambientes,\n    como desenvolvimento, testes ou produção.\n')
st.success('\n    **Sistema de Validação Integrado!**\n    Ao iniciar, a aplicação verifica automaticamente (`Home.py`) se as flags em `config.py`\n    formam uma combinação lógica. Combinações inválidas (ex: exigir login sem banco de dados)\n    impedirão a inicialização, exibindo uma mensagem de erro clara.\n')
with st.expander('📚 1. Detalhamento das Flags de Configuração (`config.py`)', expanded=True):
    st.markdown('\n        Para alterar o modo de operação, edite o arquivo `config.py` na raiz do projeto\n        e **reinicie o servidor Streamlit**.\n    ')
    st.subheader('`DATABASE_ENABLED` (Boolean)')
    st.markdown('\n        * **Propósito:** Controla **toda** a comunicação com o banco de dados.\n        * **`True` (Recomendado para Produção/Backend Dev):** A aplicação tentará se conectar ao banco de dados definido no `banco.ini`. Funcionalidades que dependem de dados (CRUDs, login real) estarão ativas.\n        * **`False` (Modo Offline / Frontend Dev):** A aplicação **não** tentará estabelecer conexão com o banco. Útil para desenvolver a interface gráfica (UI) sem depender de um banco ativo. Páginas que requerem dados exibirão um aviso.\n    ')

    st.subheader('`INITIALIZE_DATABASE_ON_STARTUP` (Boolean)')
    st.markdown('\n        * **Propósito:** Controla a criação/inicialização automática do schema do banco de dados **apenas para SQLite**.\n        * **`True` (Útil para Setup Inicial/Testes Locais):** Se o arquivo do banco de dados SQLite (definido em `banco.ini`) não existir ou estiver vazio, a aplicação tentará criá-lo e executar o script `persistencia/sql_schema_SQLLite.sql` para definir as tabelas e inserir dados iniciais. **Requer `DATABASE_ENABLED = True`**. *Cuidado: Não use `True` em produção com um banco já existente!*\n        * **`False` (Padrão Seguro / Produção):** A aplicação assume que o banco de dados (SQLite ou outro) já existe e está corretamente configurado. Essencial para ambientes de produção ou quando o banco é gerenciado externamente.\n    ')
    st.subheader('`REDIRECT_CONSOLE_TO_LOG` (Boolean)')
    st.markdown('\n        * **Propósito:** Define para onde as saídas padrão do console (`print`, erros, logs de bibliotecas) serão direcionadas.\n        * **`True` (Recomendado para Produção/Debugging Centralizado):** Todas as saídas do console são redirecionadas para os arquivos de log rotativos na pasta `logs/` (`app.log`, `login.log`). Isso centraliza o rastreamento e evita poluir o terminal onde o Streamlit foi iniciado.\n        * **`False` (Útil para Debugging Rápido):** As saídas (`print`, `logging`, erros) aparecem diretamente no terminal onde você executou `streamlit run Home.py`. Facilita a visualização imediata durante o desenvolvimento ativo.\n    ')
st.header('💡 2. Cenários Comuns e Combinações de Flags')
st.markdown('\n    A combinação correta das flags permite adaptar a aplicação às suas necessidades.\n    Veja os cenários válidos e como as flags interagem:\n')
st.subheader('✅ Cenários Válidos e Recomendados')
with st.container(border=True):
    st.markdown('#### 🌎 Modo Produção / Demonstração Real')
    st.markdown('Configuração ideal para o ambiente final ou para demonstrar o sistema completo com segurança e dados persistentes.')
    st.code('\nDATABASE_ENABLED = True\nINITIALIZE_DATABASE_ON_STARTUP = False  # Assume que o BD já existe\nREDIRECT_CONSOLE_TO_LOG = True        # Centraliza logs em arquivos\n    ', language='python')
    st.markdown('**Comportamento:** Exige login, conecta ao banco de dados configurado (`banco.ini`), aplica permissões de acesso e registra atividades em arquivos de log. Máxima segurança e funcionalidade.')


st.subheader('❌ Cenários Inválidos (Bloqueados Automaticamente)')
st.markdown('\n    As combinações a seguir são ilógicas e **serão bloqueadas** pelo validador\n    no `Home.py` ao iniciar a aplicação. Uma mensagem de erro específica será exibida.\n')

with st.container(border=True):
    st.error('#### Inválido 2: Inicializar Banco de Dados Desativado')
    st.code('\nDATABASE_ENABLED = False\nINITIALIZE_DATABASE_ON_STARTUP = True\n# ... (outras flags)\n    ', language='python')
    st.markdown('**Motivo:** Não faz sentido tentar criar tabelas (`INITIALIZE_DATABASE_ON_STARTUP = True`) se a conexão com o banco de dados está completamente desabilitada (`DATABASE_ENABLED = False`).')
st.markdown('---')
st.caption('Consulte este guia para configurar o ambiente ideal para sua necessidade.')