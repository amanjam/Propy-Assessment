import json
from rapidfuzz import process
from schemas import DeedRecord

def enrich_deed_data(deed_record: DeedRecord) -> dict:
    print("Starting Data Enrichment (Fuzzy Matching)...")
    
    # Dump pydantic to dict so we can inject the tax_rate and normalized name
    deed_dict = deed_record.model_dump()
    
    # Load official county reference list
    with open("counties.json", "r") as file:
        counties_db = json.load(file)
        
    official_names = [c["name"] for c in counties_db]
    messy_county = deed_dict["county_raw"] # e.g., "S. Clara"
    
    # Try to map the messy string to an official name
    best_match = process.extractOne(messy_county, official_names)
    
    if best_match:
        matched_name, score, index = best_match
        
        # 70% threshold to avoid garbage matches/false positives
        if score >= 70.0:
            print(f"Match: '{messy_county}' -> '{matched_name}' ({round(score)}%)")
            
            # Grab the rate from the DB and update the record
            for county in counties_db:
                if county["name"] == matched_name:
                    deed_dict["county_normalized"] = matched_name
                    deed_dict["tax_rate"] = county["tax_rate"]
                    break
        else:
            # Kill the process if we aren't confident in the match
            raise ValueError(f"Match quality too low for '{messy_county}'. Best guess: {matched_name} ({score}%)")
            
    return deed_dict

if __name__ == "__main__":
    from datetime import date
    
    # Mocking the extractor output for testing
    mock_data = DeedRecord(
        doc_id="TEST-01", county_raw="S. Clara", state="CA", 
        date_signed=date(2024, 1, 15), date_recorded=date(2024, 1, 10), 
        grantor="Bob", grantee="Alice", amount_digits=100.0, 
        amount_words="One Hundred", apn="123", status="PRELIMINARY"
    )
    
    enriched = enrich_deed_data(mock_data)
    
    print("\n--- Results ---")
    print(f"County: {enriched['county_normalized']}")
    print(f"Rate: {enriched['tax_rate']}")