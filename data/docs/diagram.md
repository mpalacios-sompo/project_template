---
config:
  theme: default
  look: neo
  layout: dagre
---
classDiagram
    class AIProcessor {
        -GPTClient gpt
        -EmbeddingClient embedder
        +generate_completion(*args, **kwargs)
        +generate_embeddings(*args, **kwargs)
    }
    class DocumentOperations {
        -DocumentAPIClient api
        -PDFProcessor pdf
        -ExcelProcessor excel
        +upload_doc(file_path, **kwargs)
        +get_doc(id, **kwargs)
        +semantic_search(query, document_ids, **kwargs)
        +extract_text(pdf_bytes)
        +extract_text_json(pdf_bytes)
        +extract_tables(pdf_bytes)
        +load_workbook_from_bytes(excel_bytes)
        +extract_sheet_names(workbook)
        +get_sheet(workbook, sheet_name)
        +extract_sheet_data(sheet)
        +convert_sheet_to_dataframe(sheet)
    }
    class GPTClient {
        -str base_url
        -str api_key
        -str client
        +generate_response(...)
        +_build_prompt(pydantic_schema)
        +_get_llm_client(...)
    }
    class EmbeddingClient {
        -str base_url
        -str api_key
        -str client
        +get_embeddings(input_text, model, dimensions)
        +_get_embedding_client()
    }
    class AzureChatOpenAI
    class AzureOpenAIEmbeddings
    class PydanticOutputParser
    class ChatPromptTemplate
    class DocumentAPIClient {
        -base_url
        -client
        -api_key
        -headers
        +upload_document(...)
        +get_document(document_id)
        +semantic_search(query, document_ids, ...)
    }
    class PDFProcessor {
        +extract_text(pdf_bytes)
        +extract_text_json(pdf_bytes)
        +extract_tables(pdf_bytes)
    }
    class ExcelProcessor {
        +load_workbook_from_bytes(excel_bytes)
        +extract_sheet_names(workbook)
        +get_sheet(workbook, sheet_name)
        +extract_sheet_data(sheet)
        +convert_sheet_to_dataframe(sheet)
    }
    class Workbook
    class Worksheet
    class pd.DataFrame
    AIProcessor --> GPTClient : uses
    AIProcessor --> EmbeddingClient : uses
    GPTClient --> AzureChatOpenAI : initializes
    GPTClient --> PydanticOutputParser : uses
    GPTClient --> ChatPromptTemplate : builds
    EmbeddingClient --> AzureOpenAIEmbeddings : initializes
    DocumentOperations --> DocumentAPIClient : uses
    DocumentOperations --> PDFProcessor : uses
    DocumentOperations --> ExcelProcessor : uses
    ExcelProcessor --> Workbook : returns
    ExcelProcessor --> Worksheet : returns
    ExcelProcessor --> pd.DataFrame : returns
