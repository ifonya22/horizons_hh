from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from data_processing.models import Base


DATABASE_URL = "postgresql://hhuser:Pwod7r734834@postgres/hh"


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()