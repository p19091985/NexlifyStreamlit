import streamlit as st
from utils.st_utils import st_check_session

st.set_page_config(
    page_title="Guia de Configuração",
    layout="wide",
    page_icon="⚙️"
)

st_check_session()

st.header("⚙️ Guia de Configuração e Modos de Operação")
st.markdown("---")

st.info("""
    Esta aplicação oferece flexibilidade através de flags de configuração no arquivo `config.py`.
    Essas flags permitem ajustar o comportamento do sistema para diferentes ambientes,
    como desenvolvimento, testes ou produção.
""")
st.success("""
    **Sistema de Validação Integrado!**
    Ao iniciar, a aplicação verifica automaticamente (`Home.py`) se as flags em `config.py`
    formam uma combinação lógica. Combinações inválidas (ex: exigir login sem banco de dados)
    impedirão a inicialização, exibindo uma mensagem de erro clara.
""")

with st.expander("📚 1. Detalhamento das Flags de Configuração (`config.py`)", expanded=True):
    st.markdown("""
        Para alterar o modo de operação, edite o arquivo `config.py` na raiz do projeto
        e **reinicie o servidor Streamlit**.
    """)

    st.subheader("`DATABASE_ENABLED` (Boolean)")
    st.markdown("""
        * **Propósito:** Controla **toda** a comunicação com o banco de dados.
        * **`True` (Recomendado para Produção/Backend Dev):** A aplicação tentará se conectar ao banco de dados definido no `banco.ini`. Funcionalidades que dependem de dados (CRUDs, login real) estarão ativas.
        * **`False` (Modo Offline / Frontend Dev):** A aplicação **não** tentará estabelecer conexão com o banco. Útil para desenvolver a interface gráfica (UI) sem depender de um banco ativo. Páginas que requerem dados exibirão um aviso.
    """)

    st.subheader("`USE_LOGIN` (Boolean)")
    st.markdown("""
        * **Propósito:** Habilita ou desabilita a tela/sistema de autenticação de usuários.
        * **`True` (Recomendado para Produção):** Exige que o usuário faça login através da tela inicial (`Home.py`). As permissões de acesso definidas no banco de dados (`check_access`) serão aplicadas. **Requer `DATABASE_ENABLED = True`**.
        * **`False` (Modo de Desenvolvimento Rápido):** Pula completamente a tela de login. Um usuário *mock* (simulado) com permissões de Administrador Global é criado automaticamente na sessão. Ideal para testar rapidamente funcionalidades internas sem precisar logar repetidamente.
    """)

    st.subheader("`INITIALIZE_DATABASE_ON_STARTUP` (Boolean)")
    st.markdown("""
        * **Propósito:** Controla a criação/inicialização automática do schema do banco de dados **apenas para SQLite**.
        * **`True` (Útil para Setup Inicial/Testes Locais):** Se o arquivo do banco de dados SQLite (definido em `banco.ini`) não existir ou estiver vazio, a aplicação tentará criá-lo e executar o script `persistencia/sql_schema_SQLLite.sql` para definir as tabelas e inserir dados iniciais. **Requer `DATABASE_ENABLED = True`**. *Cuidado: Não use `True` em produção com um banco já existente!*
        * **`False` (Padrão Seguro / Produção):** A aplicação assume que o banco de dados (SQLite ou outro) já existe e está corretamente configurado. Essencial para ambientes de produção ou quando o banco é gerenciado externamente.
    """)

    st.subheader("`REDIRECT_CONSOLE_TO_LOG` (Boolean)")
    st.markdown("""
        * **Propósito:** Define para onde as saídas padrão do console (`print`, erros, logs de bibliotecas) serão direcionadas.
        * **`True` (Recomendado para Produção/Debugging Centralizado):** Todas as saídas do console são redirecionadas para os arquivos de log rotativos na pasta `logs/` (`app.log`, `login.log`). Isso centraliza o rastreamento e evita poluir o terminal onde o Streamlit foi iniciado.
        * **`False` (Útil para Debugging Rápido):** As saídas (`print`, `logging`, erros) aparecem diretamente no terminal onde você executou `streamlit run Home.py`. Facilita a visualização imediata durante o desenvolvimento ativo.
    """)

st.header("💡 2. Cenários Comuns e Combinações de Flags")
st.markdown("""
    A combinação correta das flags permite adaptar a aplicação às suas necessidades.
    Veja os cenários válidos e como as flags interagem:
""")

st.subheader("✅ Cenários Válidos e Recomendados")

with st.container(border=True):
    st.markdown("#### 🌎 Modo Produção / Demonstração Real")
    st.markdown(
        "Configuração ideal para o ambiente final ou para demonstrar o sistema completo com segurança e dados persistentes.")
    st.code("""
DATABASE_ENABLED = True
USE_LOGIN = True
INITIALIZE_DATABASE_ON_STARTUP = False  # Assume que o BD já existe
REDIRECT_CONSOLE_TO_LOG = True        # Centraliza logs em arquivos
    """, language="python")
    st.markdown(
        "**Comportamento:** Exige login, conecta ao banco de dados configurado (`banco.ini`), aplica permissões de acesso e registra atividades em arquivos de log. Máxima segurança e funcionalidade.")

with st.container(border=True):
    st.markdown("#### 🛠️ Modo Desenvolvimento Back-end (Com Banco)")
    st.markdown(
        "Ideal para desenvolvedores trabalhando na lógica de acesso a dados, serviços ou regras de negócio, permitindo testes rápidos sem a barreira do login.")
    st.code("""
DATABASE_ENABLED = True
USE_LOGIN = False                       # Pula o login, usa usuário mock Admin
INITIALIZE_DATABASE_ON_STARTUP = True   # Útil com SQLite para resetar o BD facilmente
REDIRECT_CONSOLE_TO_LOG = False       # Vê logs/prints direto no terminal
    """, language="python")
    st.markdown(
        "**Comportamento:** Conecta ao banco e permite usar todas as funcionalidades de dados, mas sem a necessidade de autenticação. `INITIALIZE_DATABASE_ON_STARTUP = True` (com SQLite) permite recriar um ambiente limpo a cada reinício, ótimo para testes.")

with st.container(border=True):
    st.markdown("#### 🎨 Modo Desenvolvimento Front-end (Offline)")
    st.markdown(
        "Perfeito para focar no design visual e na experiência do usuário (UI/UX) sem depender de um banco de dados ativo ou conexão de rede.")
    st.code("""
DATABASE_ENABLED = False              # Desativa completamente o banco
USE_LOGIN = False                     # Pula o login
INITIALIZE_DATABASE_ON_STARTUP = False  # Obrigatório ser False se DB está desativado
REDIRECT_CONSOLE_TO_LOG = False       # Vê prints/erros de UI no terminal
    """, language="python")
    st.markdown(
        "**Comportamento:** A aplicação funciona sem banco de dados. O login é pulado. Páginas que dependem de dados exibirão um aviso de 'Funcionalidade Indisponível', mas a navegação entre páginas e a interação com widgets visuais funcionarão normally.")

st.subheader("❌ Cenários Inválidos (Bloqueados Automaticamente)")
st.markdown("""
    As combinações a seguir são ilógicas e **serão bloqueadas** pelo validador
    no `Home.py` ao iniciar a aplicação. Uma mensagem de erro específica será exibida.
""")

with st.container(border=True):
    st.error("#### Inválido 1: Exigir Login Sem Banco de Dados")
    st.code("""
DATABASE_ENABLED = False
USE_LOGIN = True
# ... (outras flags)
    """, language="python")
    st.markdown(
        "**Motivo:** Impossível verificar credenciais de usuário (`USE_LOGIN = True`) sem acesso ao banco onde elas estão armazenadas (`DATABASE_ENABLED = False`).")

with st.container(border=True):
    st.error("#### Inválido 2: Inicializar Banco de Dados Desativado")
    st.code("""
DATABASE_ENABLED = False
INITIALIZE_DATABASE_ON_STARTUP = True
# ... (outras flags)
    """, language="python")
    st.markdown(
        "**Motivo:** Não faz sentido tentar criar tabelas (`INITIALIZE_DATABASE_ON_STARTUP = True`) se a conexão com o banco de dados está completamente desabilitada (`DATABASE_ENABLED = False`).")

st.markdown("---")
st.caption("Consulte este guia para configurar o ambiente ideal para sua necessidade.")