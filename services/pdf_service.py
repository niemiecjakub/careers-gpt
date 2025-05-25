import pdfplumber
import io

class PdfService:
    """Service to handle PDF file operations."""

    def extract_data_from_pdf_path(self, path: str) -> str:
        """Extracts text from a PDF file."""
        cv_data = []

        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    cv_data.append(text)
                    
        return '\n'.join(cv_data)
    
    def extract_data_from_pdf_file(self, file: bytes) -> str:
        """Extracts text from a PDF file."""
        cv_data = []
        pdf_file = io.BytesIO(file)

        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    cv_data.append(text)
                    
        return '\n'.join(cv_data)
