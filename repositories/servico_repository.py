from sqlalchemy.orm import Session
from exceptions.exceptions import BadRequestException, NotFoundException
from models.models import OrdemServicoServico, Servico

def create(session: Session, servico_data: dict):
  servico = Servico(**servico_data)
  servico.ativo = True
  
  session.add(servico)
  session.commit()
  session.refresh(servico)
  return servico
 
def list(session: Session, skip: int = 0, limit: int = 5):
  return session.query(Servico).offset(skip).limit(limit).all()

def get(session: Session, servico_id: int):
  servico =  session.query(Servico).filter(Servico.id == servico_id).first()
  if not servico:
    raise NotFoundException(f"Serviço com id {servico_id} não encontrado.")
      
  return servico

def update(session: Session, servico_id: int, servico_data: dict):
  servico = session.query(Servico).filter(Servico.id == servico_id).first()
  
  if servico:
    for key, value in servico_data.items():
      setattr(servico, key, value)
    session.commit()
    session.refresh(servico)
    return servico
  else:
    raise NotFoundException(f"Serviço com id {servico_id} não encontrado.")

def delete(session: Session, servico_id: int):
  servico = session.query(Servico).filter(Servico.id == servico_id).first()
  if not servico:
    raise NotFoundException(f"Serviço com id {servico_id} não encontrado.")
    
  servico_is_related = session.query(OrdemServicoServico).filter(OrdemServicoServico.servico_id == servico_id).first()
  if servico_is_related:
    raise BadRequestException(f"Serviço com id {servico_id} está relacionado a uma ordem de serviço.")
    
  session.delete(servico)
  session.commit()
  return servico
