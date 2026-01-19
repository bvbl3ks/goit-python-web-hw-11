from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional

class ContactCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    birthday: date
    extra: Optional[str] = None

class ContactRead(ContactCreate):
    id: int

    class Config:
        from_attributes = True 
