from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Using standard SQLite for maximum portability during hackathon evaluation
SQLALCHEMY_DATABASE_URL = "sqlite:///./recruit_iq.db"

# check_same_thread is False to allow FastAPI's async workers to share the connection
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()