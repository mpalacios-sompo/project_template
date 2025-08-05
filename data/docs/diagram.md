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
      + generate_response(system_prompt, user_prompt)
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
    class AgentClient {
      <<Utility>>
      - base_url : str
      - api_key : str
      - client: str
      + create_agent(agent_name, description, instructions, agent_kind, prompt_template)
      + list_agents()
      + update_agent(agent_name, description, instructions, agent_kind, prompt_template)
      + delete_agent(agent_name, agent_kind)
      + create_agent_group(agent_group_name, orchestrator_instructions, selection_instructions, result_quality_control_instruction, agents)
      + list_agent_groups()
      + update_agent_group(agent_group_name, orchestrator_instruction, selection_instructions, result_quality_control_instruction, agents)
      + delete_agent_group(agent_group_name)
      + execute_agent(handler_name, user_message, agent_kind)
    }
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
      - base_url: str
      - api_key: str
      - client: str
      + upload_document(file_path, document_id, document_path, ttl)
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
  }

  %% Independent Classes
  class APIClient {
      <<Utility>>
        - base_url: str
        - headers: dict
        + get(path, params, headers)
        + post(path, data, json, files, headers)
        - _full_url(path)
        - _handle_response(response)
    }

  %% AI Dependencies
  AIProcessor --> GPTClient : uses
  AIProcessor --> EmbeddingClient : uses
  AIProcessor --> AgentClient : uses
  AgentClient --> APIClient : uses

  %% Document dependencies
  DocumentOperations --> DocumentAPIClient : uses
  DocumentOperations --> PDFProcessor : uses
  DocumentOperations --> ExcelProcessor : uses
  DocumentAPIClient --> APIClient : uses

  %% Notes for Core Classes
  note for AIProcessor "Orchestrates AI model interactions"
  note for DocumentOperations "Coordinates all document ingest and extraction"

