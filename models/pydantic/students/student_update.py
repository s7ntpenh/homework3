from datetime import date
from pydantic import BaseModel

class StudentUpdateModel(BaseModel):
    name: str | None = None
    birth_date: date | None = None