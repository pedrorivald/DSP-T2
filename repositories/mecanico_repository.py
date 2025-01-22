from sqlalchemy.orm import Session
from exceptions.exceptions import BadRequestException, NotFoundException
from models.models import Mecanico, OrdemServico

def create(session: Session, mecanico_data: dict):
  mecanico = Mecanico(**mecanico_data)
  session.add(mecanico)
  session.commit()
  session.refresh(mecanico)
  return mecanico
 
def list(session: Session, skip: int = 0, limit: int = 5):
  return session.query(Mecanico).offset(skip).limit(limit).all()

def get(session: Session, mecanico_id: int):
  mecanico = session.query(Mecanico).filter(Mecanico.id == mecanico_id).first()
  if not mecanico:
    raise NotFoundException(f"Mecânico com id {mecanico_id} não encontrado.")
    
  return mecanico

def update(session: Session, mecanico_id: int, mecanico_data: dict):
  mecanico = session.query(Mecanico).filter(Mecanico.id == mecanico_id).first()
  if mecanico:
    for key, value in mecanico_data.items():
      setattr(mecanico, key, value)
    session.commit()
    session.refresh(mecanico)
    return mecanico
  else:
    raise NotFoundException(f"Mecânico com id {mecanico_id} não encontrado.")

def delete(session: Session, mecanico_id: int):
  mecanico = session.query(Mecanico).filter(Mecanico.id == mecanico_id).first()
  if not mecanico:
    raise NotFoundException(f"Mecânico com id {mecanico_id} não encontrado.")
    
  mecanico_is_related = session.query(OrdemServico).filter(OrdemServico.mecanico_id == mecanico_id).first()
  if mecanico_is_related:
    raise BadRequestException(f"Mecânico com id {mecanico_id} está relacionado a uma ordem de serviço.")  
  
  session.delete(mecanico)
  session.commit()
  return mecanico
