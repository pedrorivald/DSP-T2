from typing import List
from pydantic import BaseModel
from schemas.util import Pagination

class ClienteCreate(BaseModel):
  nome: str
  sobrenome: str
  endereco: str
  telefone: str

class ClienteUpdate(BaseModel):
  nome: str
  sobrenome: str
  endereco: str
  telefone: str

class ClienteResponse(ClienteCreate):
  id: int

  class Config:
    orm_mode = True
    
class ClientePaginatedResponse(BaseModel):
  pagination: Pagination
  clientes: List[ClienteResponse]

  class Config:
    orm_mode = True
