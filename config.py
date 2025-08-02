# Chunk size for text processing (in words)
MAX_CHUNK_SIZE = 6000

#FInal Summary length (in words)
FINAL_SUMMARY_LENGTH = 6000

# Summary length (in words)
SUMMARY_LENGTH = 1000

# File paths
PDF_DIR = "pdfs/"
SUMMARIES_DIR = "summaries/"
CSV_FILE = "data/pdf_list.csv"

# Output JSON fields
JSON_FIELDS = {
    "file_name": "",
    "title": "",
    "description": "",
    "summary": "",
    "base_models": [],
    "model_numbers": [],
    "languages": [],
}

# Prompt templates
SUMMARY_PROMPT = """Write a concise summary (maximum {summary_length} words) of the following content. Focus on preserving technical details, specifications, and key insights:

{text}"""

FINAL_SUMMARY_PROMPT = """Generate a comprehensive, technically accurate summary from the following set of summaries. Keep it within {summary_length} words and ensure all critical information is retained:

{summaries}"""

METADATA_PROMPT = """You are an expert technical document analyst.

Extract the following metadata from the provided content and return a valid JSON object. Follow these instructions precisely:

- Return only the JSON (no explanations, no Markdown).
- Use exact field names as defined.
- Do not guess or fabricate information.
- If information is missing, leave arrays empty.
- Clearly distinguish "base models" (e.g., PJ2-2B) from "model numbers" (e.g., PJ2-2B-100).
- Do **not** include the words "model" or "language" in any of the values.
- For "languages", detect any explicitly or implicitly mentioned human languages — e.g., file names ending in `_es.pdf` imply Spanish, or if a document is multilingual, infer accordingly.
- Include all language names in English (e.g., English, Spanish, French).

Return the result in this exact JSON format:

{{
  "title": "<concise title, max 100 characters>",
  "description": "<detailed, professional summary in the provided style>",
  "base_models": ["<base model names like PJ2-2B>"],
  "model_numbers": ["<full model numbers like PJ2-2B-WH>"],
  "languages": ["<language names like English, French>"]
}}

Style examples for description:
{style_examples}

Content:
{content}

If you are unable to detect languages from the content, use your best judgment to infer the primary language based on the document text itself.
"""