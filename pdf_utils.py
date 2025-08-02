import pytesseract
import fitz  # PyMuPDF
import re
from typing import List, Dict, Any
import os
from PIL import Image
from io import BytesIO

import requests

# Set the tesseract_cmd to the full path of the tesseract executable
#pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'  # Windows example
# For Linux/Mac, use the path where tesseract is installed, e.g. 'C:\Program Files\Tesseract-OCR\tesseract.exe /usr/bin/tesseract'

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from PDF and perform OCR only on embedded images."""
    doc = fitz.open(pdf_path)
    text = []
    
    for page in doc:
        # Extract text directly from PDF
        text.append(page.get_text())
        
        # Process only actual images in the PDF
        for img in enumerate(page.get_images(full=True)):
            try:
                # Extract image data
                xref = img[1][0]
                base_image = doc.extract_image(xref)
                
                if base_image:
                    image_bytes = base_image["image"]
                    image = Image.open(BytesIO(image_bytes))
                    img_text = pytesseract.image_to_string(image, config='--psm 6')
                    print(f"OCR text from image on page {page.number}: {img_text}")
                    if img_text.strip():  # Only add if text was found
                        text.append(img_text)
                        
            except Exception as e:
                print(f"Error processing image on page {page.number}: {str(e)}")
    
    return "\n".join(text)

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