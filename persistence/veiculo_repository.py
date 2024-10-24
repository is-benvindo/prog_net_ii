from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.models import Veiculo

class VeiculoRepository:

    def get_all(self, db: Session, modelo_id: str = None, cor: str = None):
        query = db.query(Veiculo)
        if modelo_id:
            query = query.filter(Veiculo.modelo_id == modelo_id)
        if cor:  # Aqui você pode querer filtrar pela cor, se isso fizer sentido no seu modelo
            query = query.filter(Veiculo.cor.ilike(f"%{cor}%"))
        return query.all()

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
            # Utilizando db.merge para atualizar o veículo
            veiculo_atualizado = db.merge(veiculo)  
            db.commit()
            return veiculo_atualizado  
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