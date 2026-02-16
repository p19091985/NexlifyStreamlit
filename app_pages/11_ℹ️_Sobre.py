
import streamlit as st
from utils.st_utils import st_check_session, check_access
from pathlib import Path
from components import servicos_gerenciador as servico

st.set_page_config(page_title='Sobre NexlifyStreamlit', layout='wide', page_icon='ℹ️')
st_check_session()

try:
    allowed_roles = servico.get_allowed_roles_for_page(Path(__file__).name)
    check_access(allowed_roles)
except Exception as e:
    st.error(f'Acesso Negado: {e}')
    st.stop()

st.title('🚀 Sobre NexlifyStreamlit v3.0')
st.markdown('---')

st.subheader('Visão Geral e Arquitetura')
st.caption('Documentação técnica e visão geral do sistema.')

with st.expander('🎯 Propósito e Escopo', expanded=True):
    c1, c2 = st.columns([1, 5])
    with c1:
        st.write('<div style="font-size: 4rem; text-align: center;">🎯</div>', unsafe_allow_html=True)
    with c2:
        st.info('\n        **Framework Streamlit Enterprise-Grade**\n\n        Este sistema fornece uma base robusta para a construção de aplicações de dados escaláveis.\n        Substitui scripts ad-hoc por uma arquitetura estruturada, segura e testável.\n        ')
        st.markdown('\n        ### Principais Capacidades:\n        * **Clean Architecture:** Separação rigorosa de UI, Lógica e Dados.\n        * **Padrão Unit of Work:** Integridade transacional para todas as operações de banco de dados.\n        * **Controle de Acesso (RBAC):** Sistema de permissão granular por página e perfil de usuário.\n        * **Agnóstico de Banco:** Suporte contínuo para SQLite, PostgreSQL, MySQL e SQL Server.\n        ')

with st.expander('🛠️ Arquitetura Técnica', expanded=True):
    c1, c2 = st.columns([1, 5])
    with c1:
        st.write('<div style="font-size: 4rem; text-align: center;">🏗️</div>', unsafe_allow_html=True)
    with c2:
        st.subheader('Stack Tecnológica')
        st.markdown('\n        Construído sobre padrões modernos de Python, garantindo manutenibilidade e desempenho.\n\n        | Camada | Tecnologia | Função |\n        | :--- | :--- | :--- |\n        | **Apresentação** | Streamlit | UI Reativa, Dashboards Interativos. |\n        | **Lógica de Negócios** | Python 3.9+ | Serviços Principais, Lógica de Domínio. |\n        | **Acesso a Dados** | SQLAlchemy | Abstração ORM/Core, Padrão Repository. |\n        | **Segurança** | Bcrypt + Fernet | Hashing de Senha, Criptografia de Credenciais. |\n        ')
        st.divider()
        st.subheader('Módulos Principais (Backend)')
        st.markdown('\n        * **`UnitOfWork`**: O coração da consistência de dados. Gerencia o escopo de transações.\n        * **`Repositories`**: Encapsula toda a lógica SQL, mantendo as páginas limpas.\n        * **`Authentication`**: Gerenciamento seguro de sessão e fluxo de login.\n        ')

with st.expander('🔄 Padrão de Fluxo de Dados', expanded=True):
    st.markdown(f'\n    1. **Ação do Usuário:** Interação no Streamlit (Clique em Botão, Envio de Formulário).\n    2. **Chamada de Serviço:** A página chama um Serviço ou Repositório via `UnitOfWork`.\n    3. **Transação:** `UnitOfWork` abre um contexto de transação.\n    4. **Execução:** Repositório executa consultas SQL com segurança.\n    5. **Commit/Rollback:** `UnitOfWork` garante commit atômico no sucesso ou rollback no erro.\n    ')

st.markdown('---')
st.caption('Desenvolvido com NexlifyStreamlit Framework - 2026')