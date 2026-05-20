# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Propósito

Servidor de validação EC2 (t3.xlarge+, 16GB+) rodando N8N + LangChain + Redis + Postgres (pgvector) + Nginx com SSL.

## Stack

- **N8N**: Automação de workflows (community self-hosted)
- **LangChain**: FastAPI com RAG, Agents, Chatbot — providers OpenAI + Anthropic
- **Postgres 16 + pgvector**: Banco N8N + vector store LangChain
- **Redis 7**: Cache e filas
- **Nginx + Certbot**: Reverse proxy com SSL automático

## Arquitetura

```
Internet → Nginx (443/SSL) → / → N8N (:5678)
                            → /api/* → LangChain API (:8000)

LangChain API ↔ Postgres (pgvector)
LangChain API ↔ Redis
N8N ↔ Postgres
N8N → LangChain API (via /api/*)
```

## Comandos

```bash
# Setup inicial no EC2
sudo bash scripts/setup.sh
cp .env.example .env  # editar com valores reais
chmod +x nginx/init-letsencrypt.sh
./nginx/init-letsencrypt.sh seudominio.com seu@email.com

# Subir tudo
docker compose up -d

# Rebuild LangChain após mudanças
docker compose up -d --build langchain

# Logs
docker compose logs -f n8n
docker compose logs -f langchain
docker compose logs -f nginx

# Parar
docker compose down

# Health check LangChain
curl https://seudominio.com/api/health
```

## Endpoints LangChain API (via /api/*)

- `POST /api/chat` — conversa com histórico
- `POST /api/rag/query` — busca semântica + resposta
- `POST /api/rag/ingest` — ingestão de documentos
- `POST /api/agent/run` — executa agent com tools (DuckDuckGo + busca local)
- `GET /api/health` — healthcheck

## Estrutura

```
├── docker-compose.yml
├── .env.example
├── langchain/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── main.py          # FastAPI endpoints
│       ├── config.py        # pydantic-settings
│       ├── models.py        # Request/Response schemas
│       ├── llm.py           # Factory LLM (OpenAI/Anthropic)
│       ├── vectorstore.py   # PGVector singleton
│       └── chains/
│           ├── chat.py      # Chat com histórico em memória
│           ├── rag.py       # RAG query + ingest
│           └── agent.py     # Agent com tools
├── nginx/
│   ├── nginx.conf
│   ├── conf.d/default.conf.template
│   └── init-letsencrypt.sh
└── scripts/
    └── setup.sh
```

## Notas

- `.env` nunca no git — usar `.env.example` como template
- N8N consome LangChain via HTTP Request node apontando para `http://langchain:8000` (rede interna Docker)
- Histórico de chat em memória (reinicia com container) — migrar para Redis se precisar persistência
- Certificado SSL renova automaticamente via container certbot
