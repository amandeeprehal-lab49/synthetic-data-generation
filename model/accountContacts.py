from langchain.pydantic_v1 import BaseModel


class AccountContact(BaseModel):
    id: int = 0
    accountId: int = 0
    contactId: int = 0
    examples = [
        {"example": """Id: 1, Account Id: 1, Contact Id: 1234"""},
        {"example": """Id: 2, Account Id: 1, Contact Id: 1237"""},
        {"example": """Id: 3, Account Id: 2, Contact Id: 1235"""},
        {"example": """Id: 4, Account Id: 2, Contact Id: 1236"""},
        {"example": """Id: 5, Account Id: 3, Contact Id: 1237"""},
        {"example": """Id: 6, Account Id: 3, Contact Id: 1235"""},
        {"example": """Id: 7, Account Id: 4, Contact Id: 1235"""},
        {"example": """Id: 8, Account Id: 4, Contact Id: 1234"""},
    ]
