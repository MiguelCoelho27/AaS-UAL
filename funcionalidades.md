
# Funcionalidades 1, 2 e 3 — Projeto de Arquitetura Avançada de Sistemas

## ✅ Funcionalidade 1: Tecnologias de Implementação de Sistemas Distribuídos

O sistema segue uma arquitetura de **microserviços**, onde cada componente (como `Events`, `User`, `Payments`, etc.) funciona de forma independente, comunicando através de chamadas HTTP usando a framework **Flask** em Python.

### Comunicação:
- Realizada via **REST + JSON**
- O cliente (`interface.py`) comunica com os serviços usando a biblioteca `requests`.

### Justificação:
- Flask é leve, simples e ideal para serviços independentes.
- REST permite interoperabilidade com outros sistemas.
- A divisão em serviços facilita manutenção, testes e escalabilidade.

---

## 🚀 Funcionalidade 2: Implementação de Cluster de Computadores

O sistema é orquestrado com **Docker Compose**, simulando um cluster local com serviços distribuídos.

### Características:
- Cada microserviço corre num container separado.
- A comunicação entre serviços é feita através de redes internas do Docker.
- Suporte para escalar serviços dinamicamente com:
```bash
docker-compose up --scale events=2
```

### Justificação:
- Docker permite isolamento leve por serviço.
- Compose facilita a gestão de múltiplos serviços em cluster simulado.
- Prepara a base para deploy futuro em Kubernetes.

---

## 🧱 Funcionalidade 3: Virtualização de Computadores

Cada componente é virtualizado com um **Dockerfile** próprio. O ambiente de cada serviço é independente, com as suas dependências e configuração.

### Detalhes:
- Cada serviço inclui:
  - `Dockerfile` com base Python 3.11
  - `requirements.txt` com dependências
  - Porta própria exposta
- Total isolamento entre serviços

### Justificação:
- Docker garante consistência entre ambientes de desenvolvimento e produção.
- Facilita testes, CI/CD e portabilidade entre máquinas.

---

## 📦 Estrutura Recomendada do Projeto

```
Sistema-Gestao-de-Eventos-main/
├── Events/
│   ├── Dockerfile
│   ├── app.py
│   ├── controller.py
│   └── ...
├── Interface/
│   ├── Dockerfile
│   └── interface.py
├── Payments/
├── Orders/
├── Tygkets/   # ⚠️ Corrigir para Tickets
├── User/
├── docker-compose.yml
├── .gitignore
├── README.md
└── Kubernetes/
```

---

Este documento pode ser incluído em `docs/funcionalidades.md` no GitHub.
