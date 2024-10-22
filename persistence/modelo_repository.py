# modelo_repository.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.models import Modelo

class ModeloRepository:
    def get_all(self, db: Session):
        return db.query(Modelo).all()

    def get_by_id(self, db: Session, id: str):
        return db.query(Modelo).filter(Modelo.id == id).first()

    def save(self, db: Session, modelo: Modelo): 
        try:
            db.add(modelo)  
            db.commit()
            db.refresh(modelo)  
            return modelo  
        except SQLAlchemyError as e:
            db.rollback() 
            raise e

    def update(self, db: Session, modelo: Modelo): 
        try:
            db.merge(modelo)  
            db.commit()
            return modelo  
        except SQLAlchemyError as e:
            db.rollback()
            raise e

    def delete(self, db: Session, id: str):
        modelo = self.get_by_id(db, id)
        if modelo:
            try:
                db.delete(modelo)  
                db.commit()
                return modelo  
            except SQLAlchemyError as e:
                db.rollback() 
                raise e 
        return None
