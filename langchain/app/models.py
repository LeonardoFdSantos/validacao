from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str
    conversation_id: str | None = None
    provider: str | None = None
    model: str | None = None


class ChatResponse(BaseModel):
    response: str
    conversation_id: str


class RAGQueryRequest(BaseModel):
    query: str
    k: int = 4
    provider: str | None = None


class RAGQueryResponse(BaseModel):
    answer: str
    sources: list[str]


class RAGIngestRequest(BaseModel):
    texts: list[str]
    metadatas: list[dict] | None = None


class RAGIngestResponse(BaseModel):
    ingested: int


class AgentRequest(BaseModel):
    task: str
    provider: str | None = None
    model: str | None = None


class AgentResponse(BaseModel):
    result: str
    steps: list[str]
