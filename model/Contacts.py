from langchain.pydantic_v1 import BaseModel


class Contact(BaseModel):
    contactId: int = 0
    name: str = ""
    address: str = ""
    examples = [
        {"example": """Contact Id: 1234, Name: Richard, Address: US"""},
        {"example": """Contact Id: 1235, Name: Sam, Address: UK"""},
        {"example": """Contact Id: 1236, Name: Matt, Address: France"""},
        {"example": """Contact Id: 1237, Name: Mike, Address: US"""},

    ]
