from pydantic import BaseModel

class UserTextInput(BaseModel):
    text: str