## Overview

This project serves as a template, providing tools and services for processing documents, extracting text, performing semantic search, and interacting with Azure OpenAI models for completions and embeddings. 

## Directory Structure

- `main.py` — Entry point for running the main script.
- `src/` — Core source code:
  - `services/` — Document and AI processing services.
  - `utils/` — Utility modules (logging, PDF extraction, API clients).
  - `config.py` — Configuration variables.
- `models/pydantic_classes.py` — Pydantic models for structured output.
- `notebooks/services/` — Example Jupyter notebooks for document and AI processing.
- `data/` — Input, output, logs, and docs folders for document storage.


## Setup

1. **Clone the repository** and navigate to the project root.
2. **Install dependencies**:
   ```sh
   pip install -r requirements.txt
   ```
3. **Configure environment variables in .env**:
   ```sh
    CLIENT_ID = your_client_id
    API_KEY = your_api_key
   ```

## Usage

### Jupyter Notebooks
See notebooks/services/ai_processor.ipynb and notebooks/services/document_operations.ipynb for example usage of document upload, extraction, semantic search, and AI completions.

### Document Operations
Upload PDF: Use DocumentOperations.upload_doc to upload a document.
Extract Text: Use DocumentOperations.extract_text for plain text or DocumentOperations.extract_text_json for paginated JSON.
Semantic Search: Use DocumentOperations.semantic_search to search for clauses or keywords.

### AI Processing
Generate Completion: Use AIProcessor.generate_completion for GPT model completions.
Generate Embeddings: Use AIProcessor.generate_embeddings for text embeddings.
Logging
Logs are saved in the directory specified by LOG_DIRERCTORY in src/config.py.

