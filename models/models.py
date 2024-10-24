from sqlalchemy import Column, String, Integer, Numeric, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from persistence.database import Base

class Montadora(Base):
    __tablename__ = 'montadora'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  # Continua com UUID
    nome = Column(String, index=True)
    pais = Column(String)
    ano_fundacao = Column(Integer)

    modelos = relationship("Modelo", back_populates="montadora")


class Modelo(Base):
    __tablename__ = 'modelo'  # Nome correto da tabela (no singular)

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  # Continua com UUID
    nome = Column(String, nullable=False)
    montadora_id = Column(UUID(as_uuid=True), ForeignKey('montadora.id'), nullable=False)
    valor_referencia = Column(Numeric, nullable=False)
    motorizacao = Column(Numeric, nullable=False)
    turbo = Column(Boolean, default=False)
    automatico = Column(Boolean, default=False)

    montadora = relationship("Montadora", back_populates="modelos")
    
    veiculos = relationship("Veiculo", back_populates="modelo")


class Veiculo(Base):
    __tablename__ = 'veiculo'  # Nome no singular, para consistência
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  # Continua com UUID
    modelo_id = Column(UUID(as_uuid=True), ForeignKey('modelo.id'), nullable=False)  # Corrigido o nome da ForeignKey
    cor = Column(String, nullable=False)
    ano_fabricacao = Column(Integer, nullable=False)
    ano_modelo = Column(Integer, nullable=False)
    valor = Column(Numeric, nullable=False)
    placa = Column(String, nullable=False, unique=True)
    vendido = Column(Boolean, default=False)
    
    modelo = relationship("Modelo", back_populates='veiculos')