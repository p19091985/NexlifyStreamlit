# Nexlify Streamlit Concept 🚀

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/release/python-3100/)

**Nexlify Streamlit** is a modern, serverless reference architecture for building data-intensive web applications using exclusively Python.

This project demonstrates how to decouple Business Logic, Data Persistence, and UI Presentation within a Streamlit environment, achieving professional-grade maintainability without the complexity of external backend frameworks (Django/FastAPI) or databases (PostgreSQL/MySQL).

---

## 🏗️ Architecture Overview

The system follows a clean layered architecture:

*   **Presentation Layer (`pages/*.py`)**: Pure View components. They handle UI rendering and user interaction, delegating all heavy lifting to the Service Layer.
*   **Service Layer (`services/*.py`)**: Encapsulates specific business domains (e.g., `IrisEngine`, `CovertypeEngine`). Handles data fetching, normalization, ML training, and chart generation.
*   **Persistence Layer (`persistencia/*.py`)**: A thread-safe JSON repository pattern using `filelock`. Ensures data integrity even with concurrent users writing to the default filesystem.

## ✨ Key Features

*   **Hybrid Visualization**: Seamless integration of **Plotly Express** (for 3D and high interactivity) and **Altair** (for statistical grammar of graphics).
*   **Serverless Data Science**: Computes Machine Learning benchmarks (Random Forest, KNN, etc.) directly in the application runtime.
*   **Self-Healing Data**: Intelligent services that detect corruption or missing columns in session states and auto-repair the data pipeline.
*   **Zero-Login (Open Access)**: Frictionless architecture designed for public demonstrations and internal tools where auth is managed by the network layer.
*   **Theme Editor**: A built-in TOML editor to customize the application look-and-feel in real-time.

## 🚀 Getting Started

### Prerequisites

*   Python 3.10 or higher
*   Git

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/StartVision/NexlifyStreamlit.git
    cd NexlifyStreamlit
    ```

2.  **Create a virtual environment (Recommended):**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Linux/Mac
    # .venv\Scripts\activate   # Windows
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application:**
    ```bash
    streamlit run Home.py
    ```

## 📂 Project Structure

```
├── Home.py                 # Application Entry Point
├── config.py               # Global Configuration
├── data/                   # JSON Storage (Auto-created)
├── logs/                   # Application Logs (Auto-created)
├── csv/                    # Dataset Cache (Auto-created)
├── pages/                  # Streamlit Pages (View Layer)
│   ├── 1_🏠_Pagina_Inicial.py
│   ├── 2_📋_Painel_Modelo.py
│   ├── 3_📈_Painel_Analise_Iris.py
│   ├── 4_📈_Painel_Analise_Covertype.py
│   ├── 5_🎨_Editor_de_Tema.py
│   └── 6_ℹ️_Sobre.py
├── services/               # Logic Layer (Engines)
│   ├── iris_engine.py      # Iris Dataset Logic
│   └── covertype_engine.py # ML Benchmark Logic
├── persistencia/           # Data Access Layer
│   ├── repository.py       # GenericRepository (CRUD)
│   └── logger.py           # Logging Configuration
└── utils/                  # Shared Utilities
```

## 🛡️ License

This project is licensed under the MIT License - see the LICENSE file for details.