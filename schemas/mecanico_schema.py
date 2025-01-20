from typing import List
from pydantic import BaseModel
from schemas.util import Pagination

class MecanicoCreate(BaseModel):
  nome: str
  sobrenome: str
  telefone: str
  email: str

class MecanicoUpdate(BaseModel):
  nome: str
  sobrenome: str
  telefone: str
  email: str

class MecanicoResponse(MecanicoCreate):
  id: int

  class Config:
    orm_mode = True
    
class MecanicoPaginatedResponse(BaseModel):
  pagination: Pagination
  mecanicos: List[MecanicoResponse]

  class Config:
    orm_mode = True
