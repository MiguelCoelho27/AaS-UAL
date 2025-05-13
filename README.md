# 🎬 UALFlix - Mini Sistema de Streaming

Projeto desenvolvido no âmbito da unidade curricular **Arquitetura Avançada de Sistemas** (UAL – 2024/2025).

O objetivo é criar uma aplicação distribuída de streaming de vídeos curtos, aplicando conceitos de clusters, cloud computing, virtualização e estratégias de replicação de dados e serviços.

---

## 📚 Descrição Geral

UALFlix é uma plataforma educativa de streaming com:
- Gestão de catálogo de vídeos
- Armazenamento e visualização de vídeos curtos (até 5 minutos)
- Interface web simples
- Painel administrativo básico

---

## 🧱 Arquitetura e Tecnologias

O sistema está dividido em microserviços, cada um isolado em containers Docker e comunicando entre si por APIs REST. São usados serviços PostgreSQL individuais por microserviço para garantir isolamento e escalabilidade.

### Tecnologias utilizadas:
- **Python + Flask**
- **Docker & Docker Compose**
- **PostgreSQL** (um por microserviço)
- **REST APIs**
- **Cluster com containers distribuídos**
- **Virtualização via Docker**
- **Preparado para cloud pública ou privada (simulada)**

---

## 🧩 Microserviços Atuais

| Serviço             | Função                                                                 |
|---------------------|------------------------------------------------------------------------|
| `catalog-service`   | Gestão dos metadados dos vídeos (título, descrição, duração)           |
| `streaming-service` | Entrega dos vídeos aos utilizadores                                    |
| `user-service`      | Registo e autenticação de utilizadores                                 |
| `payment-service`   | Simulação de pagamentos/subscrições (a definir)                        |
| `event-service`     | Registo e monitorização de eventos no sistema                          |
| `order-service`     | Base reaproveitada — poderá ser adaptada para lógica de visualizações  |
| `ticket-service`    | Base reaproveitada — poderá ser convertida em gestão de acessos        |

---

## ⚙️ Execução Local

### Pré-requisitos:
- Docker
- Docker Compose

### Comando para iniciar:
```bash
docker-compose up --build
```

📁 Estrutura do Projeto
```sql
Copy
Edit
UALFlix/
├── catalog-service/
├── streaming-service/
├── user-service/
├── payment-service/
├── event-service/
├── order-service/
├── ticket-service/
├── docker-compose.yml
└── README.md
```

☁️ Cloud & Cluster
O sistema está preparado para ser distribuído por vários nós (ex: em Docker Swarm ou em VMs).
Está planeada a simulação de um cluster com múltiplos nós e balanceamento de carga.
Possível futura execução em ambiente cloud gratuito (como Render, Railway, ou máquina virtual na Azure).

♻️ Estratégias de Replicação
A serem implementadas:
Replicação síncrona/assíncrona dos dados dos vídeos e utilizadores
Mecanismo de cache para vídeos mais visualizados
Replicação dos serviços principais para alta disponibilidade (com failover)

📊 Avaliação de Desempenho
Planned:
Coleta de métricas de latência, throughput e uso de CPU/RAM
Dashboard simples de monitorização (ex: com Flask ou Prometheus + Grafana)
Testes de carga com locust ou ab (Apache Bench)

📌 Funcionalidades por requisito (resumo)
Requisito	Implementação prevista
Sistemas distribuídos	Microserviços em Flask com REST API
Cluster de computadores	Docker containers distribuídos
Virtualização	Containers Docker
Execução em cloud	Preparação para deployment em cloud
Replicação de dados	Cache + estratégia master-slave (a definir)
Replicação de serviços	Load balancer + múltiplas instâncias por serviço
Avaliação de desempenho	Dashboard + testes de carga

👨‍🏫 Docente
Prof.ª Inês Almeida
UAL – Departamento de Engenharia e Ciências da Computação

