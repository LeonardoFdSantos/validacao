from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool
from app.llm import get_llm
from app.vectorstore import get_vectorstore


@tool
def search_documents(query: str) -> str:
    """Busca documentos na base de conhecimento local."""
    vectorstore = get_vectorstore()
    docs = vectorstore.similarity_search(query, k=3)
    if not docs:
        return "Nenhum documento encontrado."
    return "\n\n".join(doc.page_content for doc in docs)


def get_tools():
    return [
        DuckDuckGoSearchRun(),
        search_documents,
    ]


def run_agent(task: str, provider: str | None = None, model: str | None = None) -> tuple[str, list[str]]:
    llm = get_llm(provider, model)
    tools = get_tools()

    prompt = ChatPromptTemplate.from_messages([
        ("system", "Você é um agente que resolve tarefas usando as ferramentas disponíveis. Seja objetivo."),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    agent = create_tool_calling_agent(llm, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools, verbose=False, return_intermediate_steps=True)

    result = executor.invoke({"input": task})

    steps = []
    for step in result.get("intermediate_steps", []):
        action, observation = step
        steps.append(f"{action.tool}: {observation[:200]}")

    return result["output"], steps
