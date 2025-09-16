# scripts/ingest_data.py
"""
CLI script to load and index product data.
Run with: python scripts/ingest_data.py
"""

from src.ingestion.product_loader import load_and_index_products, ensure_pinecone_index_exists

if __name__ == "__main__":
    ensure_pinecone_index_exists()
    load_and_index_products("data/products.csv")
    print(" Product ingestion complete!")