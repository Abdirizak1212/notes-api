from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from typing import List
from sqlalchemy import select, update
from sqlalchemy.orm import Session
from datetime import datetime

from dotenv import dotenv_values

from database import engine, notes
from models import NoteCreate, NoteResponse
from auth import get_current_user
from users import router as users_router

values = dotenv_values('.env')

app = FastAPI(title="Notes API")

@app.on_event("startup")
def startup_event():
    pass

@app.get("/", response_model=dict)
def root():
    return {"status": "ok"}

@app.get("/notes", response_model=List[NoteResponse])
def get_notes(current_user: dict = Depends(get_current_user)):
    with Session(bind=engine) as session:
        stmt = select(notes)
        result = session.execute(stmt).all()
        return [NoteResponse.model_validate(dict(row._mapping)) for row in result]

@app.get("/notes/{note_id}", response_model=NoteResponse)
def get_note(note_id: int, current_user: dict = Depends(get_current_user)):
    with Session(bind=engine) as session:
        stmt = select(notes).where(notes.c.id == note_id)
        row = session.execute(stmt).first()
        if not row:
            raise HTTPException(status_code=404, detail="Note not found")
        return NoteResponse.model_validate(dict(row._mapping))

@app.post("/notes", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
def create_note(note: NoteCreate, current_user: dict = Depends(get_current_user)):
    with Session(bind=engine) as session:
        ins = notes.insert().values(title=note.title, content=note.content)
        result = session.execute(ins)
        session.commit()
        note_id = result.inserted_primary_key[0]
        stmt = select(notes).where(notes.c.id == note_id)
        row = session.execute(stmt).first()
        return NoteResponse.model_validate(dict(row._mapping))

@app.put("/notes/{note_id}", response_model=NoteResponse)
def update_note(note_id: int, payload: NoteCreate, current_user: dict = Depends(get_current_user)):
    with Session(bind=engine) as session:
        stmt = select(notes).where(notes.c.id == note_id)
        row = session.execute(stmt).first()
        if not row:
            raise HTTPException(status_code=404, detail="Note not found")
        upd = (
            notes.update()
            .where(notes.c.id == note_id)
            .values(title=payload.title, content=payload.content)
        )
        session.execute(upd)
        session.commit()
        stmt = select(notes).where(notes.c.id == note_id)
        row = session.execute(stmt).first()
        return NoteResponse.model_validate(dict(row._mapping))

@app.delete("/notes/{note_id}")
def delete_note(note_id: int, current_user: dict = Depends(get_current_user)):
    with Session(bind=engine) as session:
        stmt = select(notes).where(notes.c.id == note_id)
        row = session.execute(stmt).first()
        if not row:
            raise HTTPException(status_code=404, detail="Note not found")
        session.execute(notes.delete().where(notes.c.id == note_id))
        session.commit()
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)


app.include_router(users_router)
