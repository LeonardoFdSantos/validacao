from langchain_postgres import PGVector
from app.config import get_settings
from app.llm import get_embeddings

_vectorstore = None


def get_vectorstore() -> PGVector:
    global _vectorstore
    if _vectorstore is None:
        settings = get_settings()
        _vectorstore = PGVector(
            embeddings=get_embeddings(),
            connection=settings.database_url,
            collection_name="documents",
        )
    return _vectorstore
