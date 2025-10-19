import streamlit as st
from utils.st_utils import st_check_session

                        
st.set_page_config(
    page_title="Sobre o Sistema",
    layout="centered",                                                      
    page_icon="🚀"
)

                                                                
st_check_session()

                  
st.markdown("# 🚀 Sobre Este Sistema: Arquitetura e Propósito")
st.markdown("---")

                                
st.info("""
    **Sistema de Demonstração - Versão 2.0 (Streamlit)**

    Esta aplicação representa a modernização de um sistema originalmente construído
    com Tkinter/ttkbootstrap. O objetivo principal foi migrar para uma interface
    web interativa e acessível usando **Streamlit**, sem sacrificar a robustez
    do back-end.
""")

                      
st.subheader("🏗️ Arquitetura Preservada e Aprimorada")
st.markdown("""
    A lógica de negócios e o acesso aos dados foram cuidadosamente mantidos e
    organizados em camadas distintas, promovendo:
    * **Manutenibilidade:** Código mais fácil de entender e modificar.
    * **Testabilidade:** Componentes isolados facilitam testes unitários.
    * **Flexibilidade:** Adaptação a novas regras de negócio ou fontes de dados.

    **Componentes Chave do Back-end:**
    * **Camada de Persistência (`persistencia/`):**
        * Utiliza `SQLAlchemy Core` para comunicação eficiente e padronizada com o banco de dados.
        * Inclui um **Repositório Genérico** (`repository.py`) que abstrai as operações CRUD (Criar, Ler, Atualizar, Deletar), tornando os controladores independentes dos detalhes do SQL.
        * Gerencia a conexão (`database.py`) de forma centralizada, lendo a configuração ativa do `banco.ini`.
        * Implementa segurança (`security.py`, `auth.py`) com criptografia para credenciais no `.ini` e hashing `bcrypt` para senhas de usuário no banco.
    * **Camada de Serviço (`persistencia/data_service.py`):**
        * Orquestra operações que envolvem múltiplas tabelas ou lógicas complexas (ex: reclassificar vegetal e registrar no log de auditoria).
        * Garante a **atomicidade** das transações (ou tudo funciona, ou nada é alterado), mantendo a integridade dos dados.
    * **Compatibilidade Multi-Banco:**
        * Graças à padronização recente (nomes de tabelas/colunas em minúsculas e SQL mais genérico), o sistema agora suporta nativamente **SQLite, PostgreSQL, MySQL/MariaDB e SQL Server**, bastando configurar o `banco.ini`.
""")

                                
st.subheader("🖥️ Interface com Streamlit")
st.markdown("""
    A interface foi redesenhada utilizando os componentes nativos do Streamlit:
    * A estrutura de múltiplos painéis foi substituída pelo sistema de `pages/` do Streamlit, proporcionando uma navegação fluida pela **barra lateral esquerda**.
    * Cada arquivo na pasta `pages/` corresponde a uma funcionalidade do sistema.
    * A interatividade é gerenciada pelo ciclo de execução do Streamlit, com o estado sendo mantido através do `st.session_state`.
""")

st.markdown("---")
st.caption("Desenvolvido como demonstração de arquitetura de software e migração de UI.")