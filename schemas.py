from pydantic import BaseModel

class CreateQuestionSchema(BaseModel):
    content: str
    id_test: int