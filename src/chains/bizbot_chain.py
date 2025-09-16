# src/chains/bizbot_chain.py
import os
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from config.settings import settings
from src.utils.prompt_utils import create_bizbot_prompt, format_docs
from src.memory.session_memory import get_session_history_window, get_session_history

# Set API key
os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY

# Initialize components
embeddings = OpenAIEmbeddings(model=settings.EMBEDDING_MODEL)
vectorstore = PineconeVectorStore(index_name=settings.INDEX_NAME, embedding=embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

llm = ChatOpenAI(model=settings.LLM_MODEL, temperature=settings.TEMPERATURE)
prompt = create_bizbot_prompt()

# Build RAG + Memory Chain
rag_chain = (
    {
        "context": retriever | format_docs,
        "question": RunnablePassthrough(),
        "history": lambda x: get_session_history_window(
            x.get("session_id", "default"),
            settings.SESSION_MEMORY_WINDOW
        )
    }
    | prompt
    | llm
    | StrOutputParser()
)

# Wrap with message history
conversational_rag_chain = RunnableWithMessageHistory(
    rag_chain,
    get_session_history,  # full history manager
    input_messages_key="question",
    history_messages_key="history"
)

def ask_bizbot(question: str, session_id: str = "default") -> str:
    """Ask BizBot a question in context of a session."""
    config = {"configurable": {"session_id": session_id}}
    return conversational_rag_chain.invoke({"question": question}, config=config)