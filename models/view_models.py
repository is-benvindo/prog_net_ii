from pydantic import BaseModel

class InputMontadora(BaseModel):
  nome: str
  pais: str
  ano: int
  
  
from typing import Optional

class InputModelo(BaseModel):
    nome: str
    montadora_id: str 
    valor_referencia: float
    motorizacao: float
    turbo: Optional[bool] = False 
    automatico: Optional[bool] = False  

class ModeloResponse(BaseModel):
    id: str 
    nome: str
    montadora_id: str
    valor_referencia: float
    motorizacao: float
    turbo: bool
    automatico: bool

    class Config:
        orm_mode = True  
        

class InputVeiculo(BaseModel):
    modelo_id: str 
    cor: str
    ano_fabricacao: int
    ano_modelo: int
    valor: float
    placa: str 
    vendido: Optional[bool] = False  

class VeiculoResponse(BaseModel):
    id: str  
    modelo_id: str
    cor: str
    ano_fabricacao: int
    ano_modelo: int
    valor: float
    placa: str
    vendido: bool

    class Config:
        orm_mode = True  
