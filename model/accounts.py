from langchain.pydantic_v1 import BaseModel
from langchain.schema import Document


class Account(Document):
    accountId: int = 0
    name: str = ""
    address: str = ""
    notes: str = ""

    examples = [
        {"example": """"Account ID: 1, Name: Microsoft, Address: US, Notes: Testing note"""},
        {"example": """Account ID: 2, Name: Google, Address: UK, Notes: Another note"""},
        {"example": """Account ID: 3, Name: Apple, Address: US, Notes: dummy note"""},
        {"example": """Account ID: 4, Name: Meta, Address: France, Notes: temp note"""}
    ]
