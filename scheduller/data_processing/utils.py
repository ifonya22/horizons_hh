from data_processing.models import GenTable, ScheduleTable
from data_processing.crud import CRUDBase
# from connect import Session
from functools import wraps
from sqlalchemy.orm import Session
from sqlalchemy import text
import pandas as pd
from sqlalchemy.exc import SQLAlchemyError

crud_gen_table = CRUDBase(GenTable)
crud_schedule_table = CRUDBase(ScheduleTable)

# def session_scope(func):
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         session = Session()
#         try:
#             result = func(session, *args, **kwargs)
#             session.commit()
#             return result
#         except Exception as e:
#             session.rollback()
#             raise e
#         finally:
#             session.close()
#     return wrapper



def add_schedule_to_db(db, uuid, req_str, experience, last_search_date, next_search_date, csv):
    vrc = crud_schedule_table.create(
        db,
        {
            "uuid": uuid,
            "req_str" : req_str,
            "experience" : experience,
            "last_search_date" : last_search_date,
            "next_search_date" : next_search_date,
            "csv" : csv,
        },
    )
    return vrc

from sqlalchemy import select

def get_data_by_uuid(db: Session, uuid: str):
    # Создаем запрос для выборки всех записей, где uuid соответствует указанному
    query = select(GenTable).where(GenTable.uuid == uuid)
    
    # Выполняем запрос и получаем результат
    result = db.execute(query).scalars().all()
    
    # Преобразуем результат в DataFrame
    df = pd.DataFrame([item.__dict__ for item in result])
    
    # Удаляем метаданные SQLAlchemy
    df = df.drop('_sa_instance_state', axis=1, errors='ignore')
    
    return df

def save_dataframe(db: Session, df: pd.DataFrame, model):
    """
    Save a DataFrame to the database using SQLAlchemy ORM.

    Args:
        db (Session): The SQLAlchemy session.
        df (pd.DataFrame): The DataFrame to save.
        model: The SQLAlchemy model class.
    """
    try:
        # Преобразуем DataFrame в список словарей
        records = df.to_dict(orient='records')
        
        # Создаем экземпляры модели на основе данных
        objects = [model(**record) for record in records]
        
        # Добавляем все объекты в сессию
        db.bulk_save_objects(objects)
        
        # Коммитим транзакцию
        db.commit()
    except SQLAlchemyError as e:
        # Откатываем транзакцию в случае ошибки
        db.rollback()
        print(f"Error occurred: {e}")