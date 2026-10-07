"""
PDF Processing Module
Handles PDF extraction with password support
"""

import PyPDF2
import pdfplumber
import io
import os
from typing import Optional
import logging


class PDFProcessor:
    """Extract text from PDF files"""
    
    def __init__(self, file_path: str, password: Optional[str] = None):
        self.file_path = file_path
        self.password = password
        
    def extract_text(self) -> str:
        """
        Extract text from PDF using multiple methods
        Returns concatenated text from all pages
        """
        # Try pdfplumber first (better for tables)
        try:
            text = self._extract_with_pdfplumber()
            if text and len(text.strip()) > 100:
                return text
        except Exception as e:
            print(f"pdfplumber failed: {e}")
        
        # Fallback to PyPDF2
        try:
            text = self._extract_with_pypdf2()
            if text and len(text.strip()) > 100:
                return text
        except Exception as e:
            print(f"PyPDF2 failed: {e}")

        # Final fallback: try OCR (scanned/image PDFs)
        # OCR requires pdf2image (poppler) and pytesseract (Tesseract OCR) to be available.
        try:
            from pdf2image import convert_from_path
            import pytesseract
            from PIL import Image
        except Exception as e:
            logging.debug('OCR dependencies not available: %s', e)
            raise ValueError(
                "Could not extract text from PDF. The file may be scanned or image-only. "
                "Install optional OCR dependencies (pdf2image, pytesseract) and native binaries (Poppler + Tesseract) to enable OCR fallback."
            )

        # Allow users to set POPPLER_PATH and TESSERACT_CMD env vars on Windows to point to native binaries
        poppler_path = os.getenv('POPPLER_PATH')
        tesseract_cmd = os.getenv('TESSERACT_CMD')
        if tesseract_cmd:
            try:
                pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
            except Exception:
                logging.debug('Could not set pytesseract command via TESSERACT_CMD')

        try:
            if poppler_path:
                images = convert_from_path(self.file_path, dpi=300, userpw=self.password, poppler_path=poppler_path)
            else:
                images = convert_from_path(self.file_path, dpi=300, userpw=self.password)
        except Exception as e:
            logging.exception('pdf2image failed to convert PDF to images')
            raise ValueError(
                "OCR fallback failed: could not convert PDF to images. Ensure Poppler is installed and available in PATH, or set POPPLER_PATH env var. "
                f"(inner error: {e})"
            )

        text_parts = []
        try:
            for img in images:
                try:
                    page_text = pytesseract.image_to_string(img, lang='eng')
                    if page_text:
                        text_parts.append(page_text)
                except Exception as e:
                    logging.debug('pytesseract failed on a page: %s', e)

            combined = "\n".join(text_parts)
            if combined and len(combined.strip()) > 20:
                return combined
            else:
                raise ValueError("OCR ran but produced no meaningful text")
        except Exception as e:
            logging.exception('OCR extraction failed')
            raise ValueError(f'Could not extract text from PDF: {e}')
    
    def _extract_with_pdfplumber(self) -> str:
        """Extract using pdfplumber (better for structured data)"""
        text_parts = []
        
        with pdfplumber.open(self.file_path, password=self.password) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
                
                # Try to extract tables separately
                tables = page.extract_tables()
                for table in tables:
                    for row in table:
                        if row:
                            text_parts.append(" | ".join([str(cell) if cell else "" for cell in row]))
        
        return "\n".join(text_parts)
    
    def _extract_with_pypdf2(self) -> str:
        """Extract using PyPDF2 (fallback method)"""
        text_parts = []
        
        with open(self.file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            
            # Handle password-protected PDFs
            if reader.is_encrypted:
                if self.password:
                    reader.decrypt(self.password)
                else:
                    raise ValueError("PDF is encrypted but no password provided")
            
            # Extract text from all pages
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
        
        return "\n".join(text_parts)
    
    def get_metadata(self) -> dict:
        """Extract PDF metadata"""
        try:
            with open(self.file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                
                if reader.is_encrypted and self.password:
                    reader.decrypt(self.password)
                
                metadata = reader.metadata
                return {
                    'title': metadata.get('/Title', ''),
                    'author': metadata.get('/Author', ''),
                    'subject': metadata.get('/Subject', ''),
                    'creator': metadata.get('/Creator', ''),
                    'producer': metadata.get('/Producer', ''),
                    'num_pages': len(reader.pages)
                }
        except Exception as e:
            return {'error': str(e), 'num_pages': 0}


def extract_text_from_pdf(file_path: str, password: Optional[str] = None) -> str:
    """
    Convenience function to extract text from PDF
    
    Args:
        file_path: Path to PDF file
        password: Optional password for encrypted PDFs
        
    Returns:
        Extracted text as string
    """
    processor = PDFProcessor(file_path, password)
    return processor.extract_text()
