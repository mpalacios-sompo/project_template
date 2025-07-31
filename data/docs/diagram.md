---
config:
  theme: default
  look: neo
  layout: dagre
---
classDiagram
  direction TB

  %% Namespaces for logical grouping
  namespace AI {
    class AIProcessor {
      <<Service>>
      - gpt : GPTClient
      - embedder : EmbeddingClient
      + generate_completion()
      + generate_embeddings()
    }
    class GPTClient {
      <<Utility>>
      - base_url : str
      - api_key : str
      + generate_response(...)
      + _build_prompt(pydantic_schema)
      + _get_llm_client()
    }
    class EmbeddingClient {
      <<Utility>>
      - base_url : str
      - api_key : str
      + get_embeddings(input_text, model, dimensions)
      + _get_embedding_client()
    }
    class AzureChatOpenAI
    class AzureOpenAIEmbeddings
    class PydanticOutputParser
    class ChatPromptTemplate
  }

  namespace Document {
    class DocumentOperations {
      <<Service>>
      - api : DocumentAPIClient
      - pdf : PDFProcessor
      - excel : ExcelProcessor
      + upload_doc(file_path)
      + get_doc(id)
      + semantic_search(query, document_ids)
      + extract_text(pdf_bytes)
      + extract_tables(pdf_bytes)
      + load_workbook_from_bytes(excel_bytes)
      + extract_sheet_names(workbook)
      + extract_sheet_data(sheet)
      + convert_sheet_to_dataframe(sheet)
    }
    class DocumentAPIClient {
      <<Utility>>
      - base_url
      - api_key
      + upload_document(...)
      + get_document(document_id)
      + semantic_search(query, document_ids)
    }
    class PDFProcessor {
      <<Utility>>
      + extract_text(pdf_bytes)
      + extract_text_json(pdf_bytes)
      + extract_tables(pdf_bytes)
    }
    class ExcelProcessor {
      <<Utility>>
      + load_workbook_from_bytes(excel_bytes)
      + extract_sheet_names(workbook)
      + get_sheet(workbook, sheet_name)
      + extract_sheet_data(sheet)
      + convert_sheet_to_dataframe(sheet)
    }
    class Workbook
    class Worksheet
    class pdDataFrame["pd.DataFrame"]
  }

  %% AI Dependencies
  AIProcessor --> GPTClient : uses
  AIProcessor --> EmbeddingClient : uses
  GPTClient --> AzureChatOpenAI : initializes
  GPTClient --> PydanticOutputParser : uses
  GPTClient --> ChatPromptTemplate : builds
  EmbeddingClient --> AzureOpenAIEmbeddings : initializes

  %% Document dependencies
  DocumentOperations --> DocumentAPIClient : uses
  DocumentOperations --> PDFProcessor : uses
  DocumentOperations --> ExcelProcessor : uses
  ExcelProcessor --> Workbook : returns
  ExcelProcessor --> Worksheet : returns
  ExcelProcessor --> pdDataFrame : returns

  %% Notes for Core Classes
  note for AIProcessor "Orchestrates GPT and Embedding model interactions"
  note for DocumentOperations "Coordinates all document ingest and extraction"
