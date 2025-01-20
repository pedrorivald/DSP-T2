from pydantic import BaseModel
from typing import Optional

class ClienteCreate(BaseModel):
  nome: str
  sobrenome: str
  endereco: str
  telefone: str

class MecanicoCreate(BaseModel):
  nome: str
  sobrenome: str
  telefone: str
  email: str

class ServicoCreate(BaseModel):
  nome: str
  valor: float
  ativo: bool
  categoria: str

class PecaCreate(BaseModel):
  nome: str
  marca: str
  modelo: str
  valor: float

class OrdemServicoCreate(BaseModel):
  cliente_id: int
  mecanico_id: int
  data_abertura: str
  situacao: str
  valor: Optional[float]
