import pandas as pd
import os
import json
from ai_summary import PDFSummarizer
from config import *
from dotenv import load_dotenv 
from upload_files_to_storage import upload_summary_to_blob_storage, check_summary_exists_in_blob # type: ignore
from pdf_utils import download_pdf

def main():
    # Load environment variables from .env file
    load_dotenv()

    # Read key from environment variable
    connection_string = os.getenv("STORAGE_CONNECTION_STRING")
    container_name = os.getenv("STORAGE_CONTAINER_NAME")
    api_key = os.environ.get("AZURE_OPENAI_API_KEY")
    if not api_key:
        raise ValueError("AZURE_OPENAI_API_KEY environment variable not set")
    
    # Initialize summarizer
    summarizer = PDFSummarizer()
    
    # Read CSV file
    df = pd.read_csv(CSV_FILE)
    
    # Style examples for metadata extraction
    style_examples = [
        "This article provides tips and resources when installing a Maestro LED+ dimmer in a 3-way with a mechanical switch or in a 3-way or 4-way with Maestro companion dimmers.",
        "This article will provide information related to Maestro Pro Dimmer (Model: MA-PRO) regarding installation and wiring instructions.",
        "Explore our online installation guide and specification submittals for the Legacy Panel Interface for Athena."
        "This is a new QS circuit selector for Athena (UA-CS-LX).",
        "It support base models like MSCL-OP153M, MSCL-OP153M-WH, and MSCL-OP153M-BL.",
        "It supports model numbers like MSCL-OP153M, MSCL-OP153M-WH, and MSCL-OP153M-BL.",
        "Languages supported include English, Spanish, French, and German."
    ]
    
    # Process each PDF
    for _, row in df.iterrows():
        pdf_url = row['URL']
        pdf_path = os.path.join(PDF_DIR, os.path.basename(pdf_url))  # Save with the original filename

        if not pdf_url.endswith('.pdf'):
            print(f"Skipping non-PDF URL: {pdf_url}")
            continue
        
        # Ensure the directory exists
        os.makedirs(PDF_DIR, exist_ok=True)

        #Extract pdf file name from the URL and create file name in the format {file_name_including_extension}.json. 
        #Check if the file already exist in the blob storage then skip the download and processing.
        file_name = os.path.basename(pdf_url)
        if check_summary_exists_in_blob(file_name, connection_string, container_name):
            print(f"Summary for {file_name} already exists in blob storage. Skipping download and processing.")
            continue
        else:
            print(f"Summary for {file_name} does not exist in blob storage. Proceeding with download and processing.")
        
        # Check if the PDF already exists locally
        if os.path.exists(pdf_path):
            print(f"PDF already exists: {pdf_path}")
        else:
            print(f"PDF does not exist, downloading: {pdf_url}")
            if not download_pdf(pdf_url, pdf_path):
                continue
        
        try:
            # Process PDF
            result = summarizer.process_pdf(pdf_path, "\n".join(style_examples))
            
            # Save result
            output_path = os.path.join(SUMMARIES_DIR, f"{result['file_name']}.json")
            with open(output_path, 'w') as f:
                json.dump(result, f, indent=2)
            
            print(f"Successfully processed: {pdf_path}")

            # Upload to Azure Blob Storage if connection details are provided
            if connection_string and container_name:
                upload_success = upload_summary_to_blob_storage(file_name, connection_string, container_name)
                return upload_success
            
        except Exception as e:
            print(f"Error processing {pdf_path}: {str(e)}")

if __name__ == "__main__":
    main()