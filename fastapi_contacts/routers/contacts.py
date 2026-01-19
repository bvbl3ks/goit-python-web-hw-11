from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date, timedelta

from database import get_db
from models import Contact
from schemas import ContactCreate, ContactRead

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.post("/", response_model=ContactRead)
def create_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    db_contact = Contact(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


@router.get("/", response_model=list[ContactRead])
def read_contacts(search: str | None = None, db: Session = Depends(get_db)):
    query = db.query(Contact)
    if search:
        query = query.filter(
            (Contact.first_name.ilike(f"%{search}%")) |
            (Contact.last_name.ilike(f"%{search}%")) |
            (Contact.email.ilike(f"%{search}%"))
        )
    return query.all()


@router.get("/{contact_id}", response_model=ContactRead)
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Not found")
    return contact


@router.put("/{contact_id}", response_model=ContactRead)
def update_contact(contact_id: int, contact: ContactCreate, db: Session = Depends(get_db)):
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not db_contact:
        raise HTTPException(status_code=404, detail="Not found")

    for key, value in contact.dict().items():
        setattr(db_contact, key, value)

    db.commit()
    db.refresh(db_contact)
    return db_contact


@router.delete("/{contact_id}")
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Not found")

    db.delete(contact)
    db.commit()
    return {"detail": "Deleted"}


@router.get("/birthdays/", response_model=list[ContactRead])
def upcoming_birthdays(db: Session = Depends(get_db)):
    today = date.today()
    next_week = today + timedelta(days=7)

    result = []
    for c in db.query(Contact).all():
        if c.birthday:
            bday = c.birthday.replace(year=today.year)
            if today <= bday <= next_week:
                result.append(c)

    return result
