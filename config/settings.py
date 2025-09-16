# config/settings.py
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # API Keys
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    PINECONE_API_KEY: str = os.getenv("PINECONE_API_KEY", "")

    # Pinecone
    INDEX_NAME: str = os.getenv("PINECONE_INDEX_NAME", "bizbot-products")
    DIMENSION: int = 1536  # Default for text-embedding-ada-002

    # LLM
    LLM_MODEL: str = os.getenv("LLM_MODEL", "gpt-4-turbo")
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "text-embedding-ada-002")
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", 0.2))

    # Memory
    SESSION_MEMORY_WINDOW: int = int(os.getenv("SESSION_MEMORY_WINDOW", 5))

    # Validation
    def validate(self):
        if not self.OPENAI_API_KEY:
            raise ValueError("❌ OPENAI_API_KEY is missing in .env")
        if not self.PINECONE_API_KEY:
            raise ValueError("❌ PINECONE_API_KEY is missing in .env")

settings = Settings()
settings.validate()