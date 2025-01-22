from typing import List, Optional
from pydantic import BaseModel
from schemas.cliente_schema import ClienteResponse
from schemas.mecanico_schema import MecanicoResponse
from schemas.util import Pagination
from datetime import datetime

class OrdemServicoPecaCreate(BaseModel):
  quantidade: int
  peca_id: int
  
class OrdemServicoCreate(BaseModel):
  cliente_id: int
  mecanico_id: int
  servicos: List[int]
  pecas: List[OrdemServicoPecaCreate]

class OrdemServicoUpdate(BaseModel):
  cliente_id: int
  mecanico_id: int

class OrdemServicoResponse(BaseModel):
  id: int
  cliente_id: int
  mecanico_id: int
  data_abertura: datetime
  data_conclusao: Optional[datetime] = None
  situacao: str
  valor: float

  class Config:
    orm_mode = True
    
class OrdemServicoPaginatedResponse(BaseModel):
  pagination: Pagination
  ordens_servicos: List[OrdemServicoResponse]

  class Config:
    orm_mode = True
    
class OrdemServicoServicoResponse(BaseModel):
  id: int
  nome: str
  valor: float
  categoria: str
  
class OrdemServicoPecaResponse(BaseModel):
  id: int
  nome: str
  marca: str
  modelo: str
  valor: float
  quantidade: int
    
class OrdemServicoFullResponse(BaseModel):
  id: int
  data_abertura: datetime
  data_conclusao: Optional[datetime] = None
  situacao: str
  valor: float
  
  cliente: ClienteResponse
  mecanico: MecanicoResponse
  
  servicos: List[OrdemServicoServicoResponse]
  pecas: List[OrdemServicoPecaResponse]

  class Config:
    orm_mode = True

