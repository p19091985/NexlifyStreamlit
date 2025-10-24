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
    **Sistema de Demonstração - Versão 2.1 (Streamlit Simplificado)**

    Esta aplicação representa a modernização de um sistema originalmente construído
    com Tkinter/ttkbootstrap. O objetivo principal foi migrar para uma interface
    web interativa usando **Streamlit**, preservando um back-end de dados robusto.

    *(Esta versão foi **recentemente refatorada** para simplificar a arquitetura,
    removendo as classes de Controller/View em favor de scripts de página únicos
    para fins didáticos.)*
""")

st.subheader("🏗️ Arquitetura Simplificada (Foco Didático)")
st.markdown("""
    A arquitetura original (baseada em Model-View-Controller) foi simplificada.
    Agora, cada funcionalidade (como "Gestão de Gatos" ou "Gestão de Usuários")
    é um **arquivo Python único e independente** localizado na pasta `pages/`.

    Esta abordagem torna o código mais fácil de entender para quem está começando:
    * **Sem Classes Complexas:** A lógica de UI e os *callbacks* (funções de botões)
        são gerenciados por funções simples.
    * **Tudo em um Só Lugar:** Você pode ler o arquivo da página de cima a baixo
        para entender tudo o que ela faz (veja o `2_📋_Painel_Modelo.py`).
    * **Reutilização do Back-end:** O acesso ao banco de dados ainda é centralizado,
        permitindo que a lógica de negócios permaneça limpa.

    **Componentes Chave do Back-end (Preservados):**
    * **Camada de Persistência (`persistencia/`):**
        * Utiliza `SQLAlchemy Core` para comunicação eficiente e padronizada com o banco de dados.
        * Inclui um **Repositório Genérico** (`repository.py`) que abstrai as operações CRUD (Criar, Ler, Atualizar, Deletar), tornando os scripts de página independentes dos detalhes do SQL.
        * Gerencia a conexão (`database.py`) de forma centralizada, lendo a configuração ativa do `banco.ini`.
        * Implementa segurança (`security.py`, `auth.py`) com criptografia para credenciais no `.ini` e hashing `bcrypt` para senhas de usuário no banco.
    * **Compatibilidade Multi-Banco:**
        * Graças ao `GenericRepository`, o sistema suporta nativamente **SQLite, PostgreSQL, MySQL/MariaDB e SQL Server**, bastando configurar o `banco.ini`.
""")

st.subheader("🖥️ Interface com Streamlit")
st.markdown("""
    A interface é construída utilizando os componentes nativos do Streamlit:
    * A navegação é gerenciada pelo sistema de `pages/` do Streamlit,
        proporcionando uma navegação fluida pela **barra lateral esquerda**.
    * Cada arquivo na pasta `pages/` (como `3_🐱_Gatos_CRUD.py`)
        corresponde a uma funcionalidade do sistema.
    * A interatividade é gerenciada pelo ciclo de execução do Streamlit,
        com o estado sendo mantido através do `st.session_state`.
""")

st.markdown("---")
st.caption("Desenvolvido como demonstração de arquitetura de software e migração de UI.")