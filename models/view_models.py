from pydantic import BaseModel

class InputMontadora(BaseModel):
  nome: str
  pais: str
  ano: int
  
  
from typing import Optional

class InputModelo(BaseModel):
    nome: str
    montadora_id: str  # Presumindo que é um UUID em formato de string
    valor_referencia: float
    motorizacao: float
    turbo: Optional[bool] = False  # Opcional, com valor padrão
    automatico: Optional[bool] = False  # Opcional, com valor padrão

class ModeloResponse(BaseModel):
    id: str  # ID do modelo gerado
    nome: str
    montadora_id: str
    valor_referencia: float
    motorizacao: float
    turbo: bool
    automatico: bool

    class Config:
        orm_mode = True  # Permite usar o modelo com dados de ORM
        

class InputVeiculo(BaseModel):
    modelo_id: str  # Presumindo que é um UUID em formato de string
    cor: str
    ano_fabricacao: int
    ano_modelo: int
    valor: float
    placa: str  # Placa deve ser única
    vendido: Optional[bool] = False  # Opcional, com valor padrão

class VeiculoResponse(BaseModel):
    id: str  # ID do veículo gerado
    modelo_id: str
    cor: str
    ano_fabricacao: int
    ano_modelo: int
    valor: float
    placa: str
    vendido: bool

    class Config:
        orm_mode = True  # Permite usar o modelo com dados de ORM
