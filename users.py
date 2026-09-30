from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from typing import Any
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.orm import registry
from sqlalchemy import insert, select
from database import metadata, engine
from auth import get_password_hash, verify_password, create_access_token
from dotenv import dotenv_values

values = dotenv_values('.env')

router = APIRouter()

# users table definition (simple, stored alongside notes)
users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("email", String, unique=True, nullable=False),
    Column("hashed_password", String, nullable=False),
)

metadata.create_all(engine)


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate):
    with engine.connect() as conn:
        # check existing
        stmt = select(users).where(users.c.email == user.email)
        existing = conn.execute(stmt).first()
        if existing:
            raise HTTPException(status_code=400, detail="User already exists")
        hashed = get_password_hash(user.password)
        ins = insert(users).values(email=user.email, hashed_password=hashed)
        result = conn.execute(ins)
        conn.commit()
        user_id = result.inserted_primary_key[0]
        return {"id": user_id, "email": user.email}


@router.post("/login")
def login(form_data: UserCreate):
    with engine.connect() as conn:
        stmt = select(users).where(users.c.email == form_data.email)
        row = conn.execute(stmt).first()
        if not row:
            raise HTTPException(status_code=400, detail="Incorrect email or password")
        record = row._mapping
        if not verify_password(form_data.password, record["hashed_password"]):
            raise HTTPException(status_code=400, detail="Incorrect email or password")
        access_token = create_access_token({"sub": str(record["id"]), "email": record["email"]})
        return {"access_token": access_token, "token_type": "bearer"}
