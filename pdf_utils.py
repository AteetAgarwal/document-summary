import pytesseract
import fitz  # PyMuPDF
import re
from typing import List, Dict, Any
import os
from PIL import Image
from io import BytesIO
import requests


def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from PDF and perform OCR only on embedded images."""
    doc = fitz.open(pdf_path)
    text = []
    
    for page_number in range(len(doc)):
        page = doc[page_number]
        page_text = page.get_text()
        images = page.get_images(full=True)
        
        if page_text.strip():
            text.append(page_text.strip())
        else:
            print(f"No text found on page {page_number + 1}, performing OCR on images.")

        # If no text found, perform OCR on the entire page
        if not page_text.strip() and images:
            print(f"Performing OCR on page {page_number + 1}...")
            # Ensure the page is rendered as an image
            # This is necessary for OCR to work on the visual content of the page
            # Render the page as an image
            pix = page.get_pixmap(dpi=300)
            img_bytes = pix.tobytes("png")
            img = Image.open(BytesIO(img_bytes))

            # Optional: convert to grayscale
            img = img.convert("L")

            # OCR using Tesseract
            img_text = pytesseract.image_to_string(img, config='--psm 3')
            print(f"--- OCR text from page {page_number} ---")
            text.append(img_text.strip())
    doc.close()
    
    return " ".join(text)

def create_chunks(text: str, max_words: int = 6000) -> List[str]:
    """Split text into chunks of specified maximum word count."""
    words = text.split()
    chunks = []
    current_chunk = []
    current_count = 0
    
    for word in words:
        if current_count + 1 > max_words:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            current_count = 0
        
        current_chunk.append(word)
        current_count += 1
    
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    
    return chunks

def extract_metadata(text: str) -> Dict[str, Any]:
    """Extract metadata like model numbers and languages."""
    # Simple regex patterns for demonstration
    model_pattern = r'[A-Z]+-[A-Z0-9]+'
    language_pattern = r'(English|Spanish|French|German|Chinese|Japanese)'
    
    metadata = {
        "model_numbers": list(set(re.findall(model_pattern, text))),
        "languages": list(set(re.findall(language_pattern, text, re.IGNORECASE))),
        "base_models": []  # This would need more specific patterns based on your needs
    }
    
    return metadata

def download_pdf(url, save_path):
    """Download a PDF from a URL and save it locally."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded: {url}")
    except Exception as e:
        print(f"Failed to download {url}: {str(e)}")
        return False
    return True