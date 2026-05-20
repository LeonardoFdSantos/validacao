from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from app.llm import get_llm
from app.vectorstore import get_vectorstore


def rag_query(query: str, k: int = 4, provider: str | None = None) -> tuple[str, list[str]]:
    llm = get_llm(provider)
    vectorstore = get_vectorstore()
    retriever = vectorstore.as_retriever(search_kwargs={"k": k})

    prompt = ChatPromptTemplate.from_messages([
        ("system", "Responda a pergunta baseado no contexto fornecido. Se não souber, diga que não encontrou informação relevante.\n\nContexto:\n{context}"),
        ("human", "{question}"),
    ])

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    docs = retriever.invoke(query)
    answer = chain.invoke(query)
    sources = [doc.metadata.get("source", "unknown") for doc in docs]

    return answer, sources


def rag_ingest(texts: list[str], metadatas: list[dict] | None = None) -> int:
    vectorstore = get_vectorstore()
    metadatas = metadatas or [{}] * len(texts)
    vectorstore.add_texts(texts=texts, metadatas=metadatas)
    return len(texts)
