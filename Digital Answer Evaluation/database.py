from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///autoeval.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

Base = declarative_base()

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)

from sqlalchemy import text

with engine.connect() as conn:
    conn.execute(text("PRAGMA journal_mode=WAL;"))
    conn.commit()