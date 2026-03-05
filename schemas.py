from pydantic import BaseModel
from datetime import date

class DeedRecord(BaseModel):
    """
    A Pydantic model representing a deed record with the following fields:
    """
    doc_id: str
    county_raw: str
    state: str
    date_signed: date
    date_recorded: date
    grantor: str
    grantee: str
    amount_digits: float
    amount_words: str
    apn: str
    status: str