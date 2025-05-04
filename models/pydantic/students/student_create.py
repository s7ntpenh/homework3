from datetime import date
from pydantic import BaseModel

class StudentCreateModel(BaseModel):
    name: str
    birth_date: date
    course: str
    photo_url: str | None = None