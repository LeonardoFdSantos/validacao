from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_anthropic import ChatAnthropic
from app.config import get_settings


def get_llm(provider: str | None = None, model: str | None = None):
    settings = get_settings()
    provider = provider or settings.default_llm_provider
    model = model or settings.default_model

    if provider == "anthropic":
        return ChatAnthropic(
            model=model if model != "gpt-4o" else "claude-sonnet-4-20250514",
            api_key=settings.anthropic_api_key,
        )
    return ChatOpenAI(
        model=model,
        api_key=settings.openai_api_key,
    )


def get_embeddings():
    settings = get_settings()
    return OpenAIEmbeddings(api_key=settings.openai_api_key)
