from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import Contact
from schemas import ContactCreate, ContactRead, ContactUpdate
from routers.auth import get_current_user

router = APIRouter(prefix="/contacts", tags=["contacts"])

@router.post("/", response_model=ContactRead, status_code=status.HTTP_201_CREATED)
def create_contact(contact: ContactCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    db_contact = Contact(**contact.model_dump(), owner_id=user.id)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

@router.get("/", response_model=list[ContactRead])
def read_contacts(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(Contact).filter(Contact.owner_id == user.id).all()

@router.get("/{contact_id}", response_model=ContactRead)
def read_contact(contact_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    contact = db.query(Contact).filter(Contact.id == contact_id, Contact.owner_id == user.id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

@router.put("/{contact_id}", response_model=ContactRead)
def update_contact(contact_id: int, contact: ContactUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    db_contact = db.query(Contact).filter(Contact.id == contact_id, Contact.owner_id == user.id).first()
    if not db_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    for key, value in contact.model_dump(exclude_unset=True).items():
        setattr(db_contact, key, value)
    db.commit()
    db.refresh(db_contact)
    return db_contact

@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contact(contact_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    db_contact = db.query(Contact).filter(Contact.id == contact_id, Contact.owner_id == user.id).first()
    if not db_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    db.delete(db_contact)
    db.commit()
    return
