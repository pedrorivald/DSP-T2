from typing import List
from pydantic import BaseModel
from schemas.util import Pagination

class ServicoCreate(BaseModel):
  nome: str
  valor: float
  categoria: str

class ServicoUpdate(BaseModel):
  nome: str
  valor: float
  ativo: bool
  categoria: str

class ServicoResponse(ServicoCreate):
  id: int
  ativo: bool

  class Config:
    orm_mode = True
    
class ServicoPaginatedResponse(BaseModel):
  pagination: Pagination
  servicos: List[ServicoResponse]

  class Config:
    orm_mode = True
