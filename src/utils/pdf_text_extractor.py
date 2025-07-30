import json
from PyPDF2 import PdfReader
from io import BytesIO

class PDFTextExtractor:

    @staticmethod
    def extract_text(pdf_bytes: bytes) -> str:
        """
        Extract all plain text from a PDF byte stream.

        Args:
            pdf_bytes (bytes): Raw PDF content as bytes.

        Returns:
            str: Full extracted text from the PDF.

        Raises:
            ValueError: If no PDF bytes are provided or the PDF has no pages.
            RuntimeError: If text extraction fails on all pages or a critical error occurs.
        """
        if not pdf_bytes:
            raise ValueError("No PDF bytes provided.")

        try:
            pdf_stream = BytesIO(pdf_bytes)
            reader = PdfReader(pdf_stream)

            if not reader.pages:
                raise ValueError("No pages found in the PDF.")

            full_text = ""
            for i, page in enumerate(reader.pages, start=1):
                try:
                    text = page.extract_text() or ""
                    full_text += text.strip() + "\n"
                except Exception as page_error:
                    raise RuntimeError(f"Failed to extract text from page {i}: {page_error}") from page_error

            return full_text.strip()

        except Exception as e:
            raise RuntimeError(f"Failed to extract text from PDF: {e}") from e
        
    @staticmethod
    def extract_text_json(pdf_bytes: bytes) -> str:
        """
        Extract text from a PDF byte stream and return a JSON-formatted string containing
        a list of page dictionaries, each with 'page_number' and 'page_content'.

        Args:
            pdf_bytes (bytes): Raw PDF content as bytes.

        Returns:
            str: JSON string with page-wise extracted text.

        Raises:
            ValueError: If no PDF bytes are provided or the PDF has no pages.
            RuntimeError: If extraction fails on all pages or if critical processing errors occur.
        """
        if not pdf_bytes:
            raise ValueError("No PDF bytes provided.")

        try:
            pdf_stream = BytesIO(pdf_bytes)
            reader = PdfReader(pdf_stream)

            if not reader.pages:
                raise ValueError("No pages found in the PDF.")

            pages_list = []
            for i, page in enumerate(reader.pages, start=1):
                try:
                    text = page.extract_text() or ""
                    pages_list.append({
                        "page_number": i,
                        "page_content": text.strip()
                    })
                except Exception as page_error:
                    raise RuntimeError(f"Failed to extract text from page {i}: {page_error}") from page_error

            try:
                return json.dumps(pages_list, ensure_ascii=False, indent=2)
            except Exception as json_error:
                raise RuntimeError(f"Failed to serialize extracted text to JSON: {json_error}") from json_error

        except Exception as e:
            raise RuntimeError(f"Failed to extract paginated PDF text: {e}") from e
