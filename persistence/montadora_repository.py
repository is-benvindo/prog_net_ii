from sqlalchemy.orm import Session
from models.models import Montadora

class MontadoraRepository:
    
    def get_all(self, db: Session, nome: str = None, pais: str = None):
        query = db.query(Montadora)
        if nome:
            query = query.filter(Montadora.nome.ilike(f"%{nome}%"))
        if pais:
            query = query.filter(Montadora.pais.ilike(f"%{pais}%"))
        return query.all()

    def get_by_id(self, db: Session, id: str):
        print(f"Buscando montadora com ID: {id}")
        return db.query(Montadora).filter(Montadora.id == id).first()


    def save(self, db: Session, montadora: Montadora):
        db.add(montadora)
        db.commit()
        db.refresh(montadora)

    def update(self, db: Session, id: str, montadora_data: Montadora):
        montadora = db.query(Montadora).filter(Montadora.id == id).first()
        if not montadora:
            return None

        try:
            montadora.nome = montadora_data.nome
            montadora.pais = montadora_data.pais
            montadora.ano_fundacao = montadora_data.ano_fundacao
        
            db.commit()
            db.refresh(montadora)
            return montadora 
        except Exception as e:
            db.rollback()
            print(f"Erro ao atualizar montadora: {e}")
            return None


    def delete(self, db: Session, id: str):
        montadora = db.query(Montadora).filter(Montadora.id == id).first()
        if montadora:
            db.delete(montadora)
            db.commit()
            
            
