
# Sistema de Gestão de Eventos

Projeto desenvolvido no âmbito da cadeira de **Arquitetura Avançada de Sistemas** (UAL), com base em microserviços distribuídos.

## 📦 Funcionalidades Implementadas

- Comunicação entre componentes distribuídos (Flask + REST)
- Cluster de computadores (simulado com Docker Compose)
- Virtualização de cada serviço com Docker
- Interface CLI com pedidos via HTTP
- Preparado para deploy em ambientes Cloud ou Kubernetes

## 🧱 Tecnologias Usadas

- Python 3.11
- Flask
- Docker
- Docker Compose
- Kubernetes (YAML)

## 🗂 Estrutura do Projeto

```
Sistema-Gestao-de-Eventos-main/
│
├── Events/           # Microserviço para eventos
├── Interface/        # Interface CLI (cliente)
├── Orders/           # Microserviço para encomendas
├── Payments/         # Microserviço para pagamentos
├── Tygkets/          # Microserviço para bilhetes (erro no nome)
├── User/             # Microserviço para utilizadores
│
├── docker-compose.yml    # Orquestração dos serviços
├── README.md             # Descrição do projeto
└── Kubernetes/           # Ficheiros de deploy em cluster Kubernetes
```

> ⚠️ Corrigir o nome da pasta `Tygkets` para `Tickets` caso necessário.

## ▶️ Como correr o projeto

### 1. Pré-requisitos:
- Python 3.11
- Docker + Docker Compose

### 2. Correr localmente com Docker Compose:
```bash
docker-compose up --build
```

### 3. Interagir com o sistema:
```bash
cd Interface
python interface.py
```

## ☁️ Kubernetes (opcional)
Descreve os serviços com ficheiros YAML prontos para deploy em cluster Kubernetes (pasta `Kubernetes/`).

---

## 👥 Autores

- Miguel Coelho (30013673)
- [Inserir os restantes colegas do grupo aqui]
