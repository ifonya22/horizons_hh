from typing import Any
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import as_declarative, declared_attr
import pandas as pd

@as_declarative()
class Base:
    id: Any
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class CRUDBase:
    def __init__(self, model):
        self.model = model

    def create(self, db: Session, obj_in):
        db_obj = self.model(**obj_in)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get(self, db: Session, id: int):
        return db.query(self.model).filter(self.model.id == id).first()

    def update(self, db: Session, id: int, obj_in):
        db_obj = db.query(self.model).filter(self.model.id == id).first()
        if db_obj:
            for key, value in obj_in.items():
                setattr(db_obj, key, value)
            db.commit()
            db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, id: int):
        db_obj = db.query(self.model).filter(self.model.id == id).first()
        if db_obj:
            db.delete(db_obj)
            db.commit()
        return db_obj

    def get_all(self, db: Session):
        """
        Получает все записи из таблицы.

        Args:
            db (Session): Сессия базы данных SQLAlchemy.

        Returns:
            list: Список всех записей в таблице.
        """
        return db.query(self.model).all()

    def get_all_as_dataframe(self, db: Session) -> pd.DataFrame:
        records = self.get_all(db)
        # Преобразуем список записей в DataFrame
        df = pd.DataFrame([record.__dict__ for record in records])
        # Убираем колонку '_sa_instance_state', которая добавляется SQLAlchemy
        if '_sa_instance_state' in df.columns:
            df.drop(columns=['_sa_instance_state'], inplace=True)
        return df
    
    def save_dataframe(self, db: Session, df: pd.DataFrame, if_exists: str = 'append'):
        df.to_sql(self.model.__tablename__, con=db.connection(), if_exists=if_exists, index=False)

    