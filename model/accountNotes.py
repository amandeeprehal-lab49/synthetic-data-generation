from langchain.pydantic_v1 import BaseModel


class AccountNote(BaseModel):
    id: int = 0
    accountContactId: int = 0
    notes: str = ""
    examples = [
        {"example": """Id: 10001, Account Contact Id: 1, Notes: This is a dummy note"""},
        {"example": """Id: 10002, Account Contact Id: 1, Notes: Another dummy note"""},
        {"example": """Id: 10003, Account Contact Id: 2, Notes: Testing note"""},

    ]
