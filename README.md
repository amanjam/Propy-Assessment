Bad Deed Validator
The Problem
Real estate data is messy. OCR (Optical Character Recognition) often produces "dirty" text with typos and, more dangerously, conflicting information. When moving these records onto a blockchain or into a database, we can't just trust an LLM to "figure it out". If an AI ignores a $50k discrepancy or an impossible date, the integrity of the transaction is compromised.

My Solution
I built a multi-stage Python pipeline that treats the LLM as a translator, not an authority. The AI extracts the data, but my code performs the "Sanity Checks" to ensure the document is logically sound.

High-Level Architecture
Strict Extraction (Gemini + Pydantic):

I used the Gemini 2.5-flash model with a native Pydantic response schema (DeedRecord).

This forces the AI to output structured, typed data (dates as date objects, amounts as floats) instead of raw strings, making it much harder for the AI to hallucinate formats.

Fuzzy Data Enrichment:

The OCR text says "S. Clara," but our database requires "Santa Clara" to pull the 0.012 tax rate.

I used rapidfuzz to map these messy names to our counties.json database.


The Guardrail: I set a 70% similarity threshold. If the AI provides a county that doesn't clearly match our database, the script kills the process rather than guessing.

Hard Logic Validation (The "Paranoid" Layer):

The Chronology Check: The script compares the signed date (Jan 15) against the recorded date (Jan 10). Since a document cannot be recorded before it exists, the code throws an error.

Financial Reconciliation: The input lists "$1,250,000.00" but the text says "One Million Two Hundred Thousand". My code compares the digits against the words and flags the mismatch.
