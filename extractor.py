import os
from google import genai
from dotenv import load_dotenv
from schemas import DeedRecord

# 1. Load the secret API key from the .env file
load_dotenv()

# 2. Initialize the Gemini client (It automatically finds GEMINI_API_KEY in the env)
client = genai.Client()

def extract_deed_data(file_path: str) -> DeedRecord:
    """
    Reads the messy OCR text and uses Gemini to extract structured data.
    """
    print(f"Reading messy OCR text from {file_path}...")
    
    with open(file_path, "r") as file:
        messy_text = file.read()

    print("Asking Gemini to extract data into our Pydantic schema...")
    
    # 3. Call the Gemini API natively with the Pydantic schema
    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=[messy_text],
        config={
            "system_instruction": "You are a precise data extraction assistant. Extract the real estate deed information from the OCR text.",
            "response_mime_type": "application/json",
            "response_schema": DeedRecord,
            "temperature": 0.0
        }
    )

    # 4. The SDK automatically parses the JSON back into our Pydantic object
    extracted_data = response.parsed
    
    print(f"Extraction successful! Found County: {extracted_data.county_raw}")
    return extracted_data

# --- QUICK TEST ---
if __name__ == "__main__":
    data = extract_deed_data("ocr_input.txt")
    print("\n--- Gemini Output ---")
    print(data.model_dump_json(indent=2))