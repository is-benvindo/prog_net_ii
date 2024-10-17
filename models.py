from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.postgresql import UUID
import uuid
from persistence.database import Base

# Modelo da tabela Montadora
class Montadora(Base):
    __tablename__ = 'montadora'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = Column(String, index=True)
    pais = Column(String)
    ano_fundacao = Column(Integer)