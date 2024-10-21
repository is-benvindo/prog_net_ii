# veiculo_repository.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.models import Veiculo

class VeiculoRepository:
    def get_all(self, db: Session):
        return db.query(Veiculo).all()

    def get_by_id(self, db: Session, id: str):
        return db.query(Veiculo).filter(Veiculo.id == id).first()

    def save(self, db: Session, veiculo: Veiculo):
        try:
            db.add(veiculo)
            db.commit()
            db.refresh(veiculo) 
            return veiculo
        except SQLAlchemyError as e:
            db.rollback() 
            raise e

    def update(self, db: Session, veiculo: Veiculo):
        try:
            db.merge(veiculo) 
            db.commit()
            return veiculo
        except SQLAlchemyError as e:
            db.rollback()
            raise e

    def delete(self, db: Session, id: str):
        veiculo = self.get_by_id(db, id)
        if veiculo:
            try:
                db.delete(veiculo)
                db.commit()
                return veiculo
            except SQLAlchemyError as e:
                db.rollback() 
                raise e 
        return None