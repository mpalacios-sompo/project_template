from src.utils.document_processing_api import DocumentAPIClient
from src.utils.pdf_text_extractor import PDFTextExtractor

class DocumentOperations:
    def __init__(self, base_url: str, client: str, api_key: str):
        self.api = DocumentAPIClient(base_url, client, api_key)
        self.extractor = PDFTextExtractor()

    def upload_doc(self, file_path, **kwargs):
        return self.api.upload_document(file_path, **kwargs)
    
    def get_doc(self, id, **kwargs):
        return self.api.get_document(id, **kwargs)
    
    def semantic_search(self, query, document_ids, **kwargs):
        return self.api.semantic_search(query, document_ids, **kwargs)

    def extract_text(self, pdf_bytes):
        return self.extractor.extract_text(pdf_bytes)

    def extract_text_json(self, pdf_bytes):
        return self.extractor.extract_text_json(pdf_bytes)

