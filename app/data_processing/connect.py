from data_processing.models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///database/mydatabase.db?check_same_thread=False')

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)