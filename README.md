# PDF Summary Generator

This project provides a tool to generate summaries from PDF documents.

## What it does (short)

This tool automates the process of extracting text from PDF files, summarizing their content, and managing the summaries.

## Setup Tesseract in Ubuntu

To set up Tesseract OCR on Ubuntu, follow these steps:

1.  **Install Tesseract and language packs:**
    ```bash
    sudo apt update
    sudo apt install tesseract-ocr
    ```
    (Replace `tesseract-ocr-{lang}` with other language packs if needed, e.g., `tesseract-ocr-deu` for German).

2.  **Verify installation:**
    ```bash
    tesseract --version
    ```
    This should display the installed Tesseract version.

## Install Requirements

To install Python and dependencies:

1. **Install pyenv:**
    ```bash
    curl https://pyenv.run | bash
    ```
    Follow the instructions to add pyenv to your shell configuration file (e.g., `.bashrc` or `.zshrc`).

2. **Install Python 3.13.5:**
    ```bash
    pyenv install 3.13.5
    pyenv global 3.13.5
    ```

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Set Connection Strings
Set the following environment variables:
    AZURE_OPENAI_API_KEY=<your-api-key>
    AZURE_OPENAI_ENDPOINT=<your-endpoint-url>
    AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o-mini
    AZURE_OPENAI_API_VERSION=2025-01-01-preview
    STORAGE_CONNECTION_STRING=<your-storage-connection-string>
    STORAGE_CONTAINER_NAME=<your-container-name>

## Run main.py

To run the main script:

1. Ensure all environment variables are set as described above.
2. Execute the script:
    ```bash
    python main.py
    ```
3. The script will process PDF files and generate summaries based on the configuration.
