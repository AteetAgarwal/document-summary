import os
from openai import AzureOpenAI
import json
from typing import List, Dict, Any
import pandas as pd
from config import *
from pdf_utils import extract_text_from_pdf, create_chunks, extract_metadata

class PDFSummarizer:
    def __init__(self):
        self.client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
        )
        self.deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    
    def summarize_chunk(self, text: str) -> str:
        """Summarize a single chunk of text using Azure OpenAI."""
        prompt = SUMMARY_PROMPT.format(
            summary_length=SUMMARY_LENGTH,
            text=text
        )
        
        response = self.client.chat.completions.create(
            model=self.deployment_name,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.choices[0].message.content
    
    def create_final_summary(self, summaries: List[str]) -> str:
        """Create final summary from individual chunk summaries."""
        prompt = FINAL_SUMMARY_PROMPT.format(
            summary_length=FINAL_SUMMARY_LENGTH,
            summaries="\n\n".join(summaries)
        )
        
        response = self.client.chat.completions.create(
            model=self.deployment_name,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.choices[0].message.content
    
    def extract_document_metadata(self, text: str, style_examples: str) -> Dict[str, Any]:
        """Extract title, description, and other metadata."""
        prompt = METADATA_PROMPT.format(
            style_examples=style_examples,
            content=text
        )
        
        response = self.client.chat.completions.create(
            model=self.deployment_name,
            messages=[{"role": "user", "content": prompt}]
        )
        
        # Try parsing as JSON directly
        result = response.choices[0].message.content.strip()

        # Remove surrounding ```json or ``` if present
        if result.startswith("```"):
            result = result.strip("`")            # Remove all backticks
            result = result.split("\n", 1)[1]     # Remove the first line (e.g., ```json)
            if result.endswith("```"):
                result = result.rsplit("\n", 1)[0]

        try:
            metadata = json.loads(result)
            return metadata
        except json.JSONDecodeError:
            raise ValueError("Failed to parse metadata response as JSON:\n" + result)
        
    def process_pdf(self, pdf_path: str, style_examples: str) -> Dict[str, Any]:
        """Process a single PDF file."""
        # Extract text from PDF
        text = extract_text_from_pdf(pdf_path)
        
        # Create chunks
        chunks = create_chunks(text, MAX_CHUNK_SIZE)
        
        # Summarize each chunk
        chunk_summaries = [self.summarize_chunk(chunk) for chunk in chunks]
        
        # Create final summary
        final_summary = self.create_final_summary(chunk_summaries)
        
        # Extract metadata
        metadata = self.extract_document_metadata(text, style_examples)
        
        return {
            "file_name": os.path.basename(pdf_path),
            "summary": final_summary,
            **metadata
        }