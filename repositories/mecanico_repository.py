from sqlalchemy.orm import Session
from models.models import Mecanico

def create_mecanico(session: Session, mecanico_data: dict):
  mecanico = Mecanico(**mecanico_data)
  session.add(mecanico)
  session.commit()
  session.refresh(mecanico)
  return mecanico
 
def get_mecanicos(session: Session, skip: int = 0, limit: int = 5):
  return session.query(Mecanico).offset(skip).limit(limit).all()

def get_mecanico(session: Session, mecanico_id: int):
  return session.query(Mecanico).filter(Mecanico.id == mecanico_id).first()

def update_mecanico(session: Session, mecanico_id: int, mecanico_data: dict):
  mecanico = session.query(Mecanico).filter(Mecanico.id == mecanico_id).first()
  if mecanico:
    for key, value in mecanico_data.items():
      setattr(mecanico, key, value)
    session.commit()
    session.refresh(mecanico)
    return mecanico
  return None
