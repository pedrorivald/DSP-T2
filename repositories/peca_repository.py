from sqlalchemy import func
from sqlalchemy.orm import Session
from exceptions.exceptions import BadRequestException, NotFoundException
from models.models import OrdemServicoPeca, Peca

def create(session: Session, peca_data: dict):
  peca = Peca(**peca_data)
  peca.ativo = True
  
  session.add(peca)
  session.flush()
  session.refresh(peca)
  return peca
 
def list(session: Session, skip: int = 0, limit: int = 5):
  return session.query(Peca).offset(skip).limit(limit).all()

def get(session: Session, peca_id: int):
  peca =  session.query(Peca).filter(Peca.id == peca_id).first()
  if not peca:
    raise NotFoundException(f"Peça com id {peca_id} não encontrada.")
      
  return peca

def count(session: Session):
  result = session.query(func.count(Peca.id)).scalar() or 0
  return { "quantidade": result }

def update(session: Session, peca_id: int, peca_data: dict):
  peca = session.query(Peca).filter(Peca.id == peca_id).first()
  if peca:
    for key, value in peca_data.items():
      setattr(peca, key, value)
    session.flush()
    session.refresh(peca)
    return peca
  else:
    raise NotFoundException(f"Peça com id {peca_id} não encontrada.")

def delete(session: Session, peca_id: int):
  peca = session.query(Peca).filter(Peca.id == peca_id).first()
  if not peca:
    raise NotFoundException(f"Peça com id {peca_id} não encontrada.")
    
  peca_is_related = session.query(OrdemServicoPeca).filter(OrdemServicoPeca.peca_id == peca_id).first()
  if peca_is_related:
    raise BadRequestException(f"Peça com id {peca_id} está relacionada a uma ordem de serviço.")
  
  session.delete(peca)
  session.flush()
  return peca