#!/bin/bash
echo "🚀 Setting up BizBot Demo..."

# Step 1: Ingest Data
echo "📥 Ingesting product data..."
python scripts/ingest_data.py

# Step 2: Launch UI
echo "🖥️  Launching Gradio UI at http://localhost:7860"
python app/gradio_ui.py