from sqlalchemy import Column, String, Integer, Numeric, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship 
import uuid
from persistence.database import Base


# Modelo da tabela Montadora
class Montadora(Base):
    __tablename__ = 'montadora'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = Column(String, index=True)
    pais = Column(String)
    ano_fundacao = Column(Integer)

    veiculos = relationship("Veiculo", back_populates="montadora")

# Modelo da tabela Veiculo
class Veiculo(Base):
    __tablename__ = 'veiculo'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = Column(String, nullable=False)
    montadora_id = Column(UUID(as_uuid=True), ForeignKey('montadora.id'), nullable=False)
    valor_referencia = Column(Numeric, nullable=False)
    motorizacao = Column(Numeric, nullable=False)
    turbo = Column(Boolean, default=False)
    automatico = Column(Boolean, default=False)

    montadora = relationship("Montadora", back_populates="veiculos")