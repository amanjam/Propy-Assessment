from pydantic import BaseModel, model_validator
from datetime import date
from word2number import w2n
print(w2n.word_to_num('two hundred and fifty six'))
class DeeRrecords(BaseModel):
    doc_id: str
    county_raw: str  # We call it raw because it will hold "S. Clara"
    state: str
    date_signed: date
    date_recorded: date
    grantor: str
    grantee: str
    amount_digits: float
    amount_words: str
    apn: str
    status: str