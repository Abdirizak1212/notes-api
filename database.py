from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import registry

from dotenv import dotenv_values

values = dotenv_values(".env")
DATABASE_URL = values["DATABASE_URL"]

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata = MetaData()

notes = Table(
    "notes",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("title", String, nullable=False),
    Column("content", String, nullable=False),
    Column("created_at", DateTime, server_default=func.now(), nullable=False),
)

metadata.create_all(engine)

mapper_registry = registry()

class Note:
    pass

mapper_registry.map_imperatively(Note, notes)
