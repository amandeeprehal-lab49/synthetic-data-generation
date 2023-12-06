from langchain.pydantic_v1 import BaseModel


class CallTranscript(BaseModel):
    id: int = 0
    accountContactId: int = 0
    transcript: str = ""
    examples = [
        {"example": """Id: 10001, Account Contact Id: 1, Transcript: This is a dummy transcript"""},
        {"example": """Id: 10002, Account Contact Id: 1, Transcript: Another dummy transcript"""},
        {"example": """Id: 10003, Account Contact Id: 2, Transcript: Testing transcript"""},

    ]
