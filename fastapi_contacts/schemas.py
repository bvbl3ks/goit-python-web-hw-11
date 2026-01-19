from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

# ---------------- USERS ----------------
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserRead(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True  # Pydantic v2 вместо orm_mode

# ---------------- CONTACTS ----------------
class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    birthday: Optional[date] = None
    extra: Optional[str] = None

class ContactCreate(ContactBase):
    pass

class ContactRead(ContactBase):
    id: int

    class Config:
        from_attributes = True

class ContactUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr]
    phone: Optional[str]
    birthday: Optional[date]
    extra: Optional[str]
