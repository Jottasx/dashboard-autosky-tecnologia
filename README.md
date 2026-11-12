# 🖥️ Painel NOC — Monitoramento Skyone Autosky

Dashboard unificado para monitoramento em tempo real das instâncias dos grupos **AutoSky** e **Fortes** no portal Skyone Autosky, projetado para exibição contínua em telas de sala / TV (modo NOC).

## 📋 Funcionalidades

- **Coleta Automatizada em Segundo Plano (`coletor.py`):** Utiliza Selenium com Microsoft Edge para ler as métricas de CPU, Memória e Disco de duas contas distintas a cada 60 segundos.
- **Detecção Inteligente de Login/MFA:** Aguarda a autenticação inicial (e-mail, senha e Google Authenticator) e assume o controle automaticamente assim que o painel interno é carregado, minimizando o navegador para não roubar o foco da tela.
- **Dashboard Visual NOC (`painel.py`):** Interface escura construída em Streamlit com atualização automática a cada 15 segundos, barras de progresso dinâmicas e alertas visuais por faixa de uso de CPU:
  - 🟢 **Normal:** `< 70%`
  - 🟡 **Atenção:** `70% a 89%`
  - 🔴 **Crítico:** `≥ 90%`
- **Modos de Visualização:**
  - **Painel Único (Padrão):** Consolida todas as instâncias dos dois grupos ordenadas pelo maior consumo de CPU, exibindo etiquetas identificadoras (`AutoSky` / `Fortes`) e o nome técnico da instância ao passar o mouse (*hover*) sobre o ambiente.
  - **Lado a Lado:** Separa os dois grupos em duas colunas simultâneas na tela.
- **Inicializador Automático (`rodar_painel.bat`):** Verifica e instala dependências do sistema (Git e Python via `winget`), atualiza o código via `git pull`, instala os pacotes Python e inicia o coletor e o dashboard com um único duplo clique.

---

## 📁 Estrutura do Projeto

```text
├── coletor.py          # Script Selenium que coleta os dados das duas contas no Edge
├── painel.py           # Interface web Streamlit do dashboard NOC
├── rodar_painel.bat    # Inicializador automático (instala deps, faz git pull e sobe os serviços)
├── requirements.txt    # Dependências Python (selenium, streamlit, pandas)
├── .gitignore          # Ignora caches, perfil temporário do navegador e JSON gerado
└── README.md           # Documentação do projeto