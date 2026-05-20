from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from app.llm import get_llm

_conversations: dict[str, list] = {}


def chat(message: str, conversation_id: str, provider: str | None = None, model: str | None = None) -> str:
    llm = get_llm(provider, model)

    prompt = ChatPromptTemplate.from_messages([
        ("system", "Você é um assistente útil e conciso."),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ])

    history = _conversations.get(conversation_id, [])

    chain = prompt | llm
    response = chain.invoke({"input": message, "history": history})

    history.append(HumanMessage(content=message))
    history.append(AIMessage(content=response.content))
    _conversations[conversation_id] = history

    return response.content
