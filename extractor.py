import os
from openai import OpenAI
from schemas import DeedRecord

# Make sure you have your OpenAI API key set in your environment variables!
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_deed_data(file_path: str) -> DeedRecord:
    """
    Reads the messy OCR text and uses an LLM to extract structured data.
    """
    print(f"Reading messy OCR text from {file_path}...")
    
    with open(file_path, "r") as file:
        messy_text = file.read()

    print("Asking LLM to extract data into our Pydantic schema...")
    
    # We use OpenAI's 'parse' method to force Structured Outputs
    response = client.beta.chat.completions.parse(
        model="gpt-4o-mini", # Fast, cheap, and perfect for extraction
        messages=[
            {"role": "system", "content": "You are a precise data extraction assistant. Extract the real estate deed information from the OCR text."},
            {"role": "user", "content": messy_text}
        ],
        response_format=DeedRecord # THIS IS THE MAGIC LINE
    )

    # The LLM returns a perfectly clean Pydantic object!
    extracted_data = response.choices[0].message.parsed
    
    print(f"Extraction successful! Found County: {extracted_data.county_raw}")
    return extracted_data

# --- QUICK TEST ---
if __name__ == "__main__":
    # Make sure you created 'ocr_input.txt' in Step 1!
    data = extract_deed_data("ocr_input.txt")
    print("\n--- LLM Output ---")
    print(data.model_dump_json(indent=2))