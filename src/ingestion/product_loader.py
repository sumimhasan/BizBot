# src/ingestion/product_loader.py
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
from config.settings import settings
import os

os.environ["PINECONE_API_KEY"] = settings.PINECONE_API_KEY

def ensure_pinecone_index_exists():
    """Create Pinecone index if it doesn't exist."""
    pc = Pinecone(api_key=settings.PINECONE_API_KEY)
    if settings.INDEX_NAME not in pc.list_indexes().names():
        print(f"🆕 Creating Pinecone index: {settings.INDEX_NAME}")
        pc.create_index(
            name=settings.INDEX_NAME,
            dimension=settings.DIMENSION,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1")
        )
        print(f"✅ Index '{settings.INDEX_NAME}' created.")
    else:
        print(f"✅ Index '{settings.INDEX_NAME}' already exists.")

def load_and_index_products(csv_path: str = "data/products.csv"):
    """Load products from CSV, split, embed, and store in Pinecone."""
    # Load
    loader = CSVLoader(file_path=csv_path)
    docs = loader.load()
    print(f"📄 Loaded {len(docs)} product records.")

    # Split
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    splits = splitter.split_documents(docs)
    print(f"✂️  Split into {len(splits)} chunks.")

    # Embed & Store
    embeddings = OpenAIEmbeddings(model=settings.EMBEDDING_MODEL)
    vectorstore = PineconeVectorStore.from_documents(
        documents=splits,
        embedding=embeddings,
        index_name=settings.INDEX_NAME
    )
    print(f"✅ Indexed {len(splits)} chunks into Pinecone.")
    return vectorstore

if __name__ == "__main__":
    ensure_pinecone_index_exists()
    load_and_index_products()