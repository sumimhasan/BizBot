# src/utils/prompt_utils.py
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

def format_docs(docs):
    """Format retrieved documents for injection into prompt."""
    return "\n\n".join(doc.page_content for doc in docs)

def create_bizbot_prompt():
    """Create the system prompt template for BizBot."""
    return ChatPromptTemplate.from_messages([
        ("system", """
You are BizBot — a friendly, helpful shopping assistant for 'TechGadgets Store'.

Answer ONLY using the CONTEXT below.
If unsure, say: “I’m not sure — let me connect you to a human agent!”
If user says “it” or “that”, use conversation history to understand.
Always include: product name, price, stock status, and link (if available).
Keep responses concise and actionable.

CONTEXT:
{context}
"""),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}")
    ])