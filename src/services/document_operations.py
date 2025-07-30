from src.utils.document_processing_api import DocumentAPIClient
from src.utils.pdf_processor import PDFProcessor
from src.utils.excel_processor import ExcelProcessor


class DocumentOperations:
    def __init__(self, base_url: str, client: str, api_key: str):
        self.api = DocumentAPIClient(base_url, client, api_key)
        self.pdf = PDFProcessor()
        self.excel = ExcelProcessor()

    # Doc Management
    def upload_doc(self, file_path, **kwargs):
        return self.api.upload_document(file_path, **kwargs)
    
    def get_doc(self, id, **kwargs):
        return self.api.get_document(id, **kwargs)
    
    def semantic_search(self, query, document_ids, **kwargs):
        return self.api.semantic_search(query, document_ids, **kwargs)

    # PDF Operations
    def extract_text(self, pdf_bytes):
        return self.pdf.extract_text(pdf_bytes)

    def extract_text_json(self, pdf_bytes):
        return self.pdf.extract_text_json(pdf_bytes)

    def extract_tables(self, pdf_bytes):
        return self.pdf.extract_tables(pdf_bytes)
    
    # Excel Operations
    def load_workbook_from_bytes(self, excel_bytes):
        return self.excel.load_workbook_from_bytes(excel_bytes)
    
    def extract_sheet_names(self, workbook):
        return self.excel.extract_sheet_names(workbook)
    
    def get_sheet(self, workbook, sheet_name):
        return self.excel.get_sheet(workbook, sheet_name)
    
    def extract_sheet_data(self, sheet):
        return self.excel.extract_sheet_data(sheet)
    
    def convert_sheet_to_dataframe(self, sheet):
        return self.excel.convert_sheet_to_dataframe(sheet)




