from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker, declarative_base, Session



SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

Base.metadata.create_all(bind=engine)

db = SessionLocal()

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

