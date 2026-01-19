from fastapi import FastAPI
from database import engine, Base
from routers import contacts

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(contacts.router)

@app.get("/")
def root():
    return {"message": "Contacts API"}
