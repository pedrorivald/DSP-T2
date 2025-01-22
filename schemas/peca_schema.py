from typing import List
from pydantic import BaseModel
from schemas.util import Pagination

class PecaCreate(BaseModel):
  nome: str
  marca: str
  modelo: str
  valor: float

class PecaUpdate(BaseModel):
  nome: str
  marca: str
  modelo: str
  valor: float

class PecaResponse(PecaCreate):
  id: int

  class Config:
    orm_mode = True
    
class PecaPaginatedResponse(BaseModel):
  pagination: Pagination
  pecas: List[PecaResponse]

  class Config:
    orm_mode = True
