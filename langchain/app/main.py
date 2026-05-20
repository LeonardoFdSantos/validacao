from uuid import uuid4
from fastapi import FastAPI
from app.models import (
    ChatRequest, ChatResponse,
    RAGQueryRequest, RAGQueryResponse,
    RAGIngestRequest, RAGIngestResponse,
    AgentRequest, AgentResponse,
)
from app.chains.chat import chat
from app.chains.rag import rag_query, rag_ingest
from app.chains.agent import run_agent

app = FastAPI(title="LangChain API", version="1.0.0")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(req: ChatRequest):
    conversation_id = req.conversation_id or str(uuid4())
    response = chat(req.message, conversation_id, req.provider, req.model)
    return ChatResponse(response=response, conversation_id=conversation_id)


@app.post("/rag/query", response_model=RAGQueryResponse)
def rag_query_endpoint(req: RAGQueryRequest):
    answer, sources = rag_query(req.query, req.k, req.provider)
    return RAGQueryResponse(answer=answer, sources=sources)


@app.post("/rag/ingest", response_model=RAGIngestResponse)
def rag_ingest_endpoint(req: RAGIngestRequest):
    count = rag_ingest(req.texts, req.metadatas)
    return RAGIngestResponse(ingested=count)


@app.post("/agent/run", response_model=AgentResponse)
def agent_endpoint(req: AgentRequest):
    result, steps = run_agent(req.task, req.provider, req.model)
    return AgentResponse(result=result, steps=steps)
