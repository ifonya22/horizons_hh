from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float, UUID, Date

Base = declarative_base()

class GenTable(Base):
    __tablename__ = 'gen_table'
    
    idgen_table = Column(Integer, primary_key=True, autoincrement=True)
    search_date = Column(DateTime, nullable=False)
    req_str = Column(String(300), nullable=True)
    sal_from = Column(Integer, nullable=True)
    sal_to = Column(Integer, nullable=True)
    currency = Column(String(4), nullable=True)
    city = Column(String(100), nullable=True)
    pub_date = Column(Date, nullable=True)
    employer = Column(String(150), nullable=True)
    job_title = Column(String(150), nullable=True)
    experience = Column(String(45), nullable=True)
    average_value = Column(Float, nullable=True)
    link = Column(String(200), nullable=True)
    uuid = Column(UUID, nullable=True)

class ScheduleTable(Base):
    __tablename__ = 'schedule_table'
    
    idschedule_table = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(UUID, nullable=True)
    req_str = Column(String(300), nullable=True)
    experience = Column(String(45), nullable=True)
    last_search_date = Column(DateTime, nullable=False)
    next_search_date = Column(DateTime, nullable=False)
    csv = Column(String(45), nullable=True)
