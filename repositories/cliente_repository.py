from sqlalchemy.orm import Session
from exceptions.exceptions import BadRequestException, NotFoundException
from models.models import Cliente, OrdemServico

def create(session: Session, cliente_data: dict):
  cliente = Cliente(**cliente_data)
  session.add(cliente)
  session.flush()
  session.refresh(cliente)
  return cliente
 
def list(session: Session, skip: int = 0, limit: int = 5):
  return session.query(Cliente).offset(skip).limit(limit).all()

def get(session: Session, cliente_id: int):
  cliente = session.query(Cliente).filter(Cliente.id == cliente_id).first()
  if not cliente:
    raise NotFoundException(f"Cliente com id {cliente_id} não encontrado.")
      
  return cliente

def update(session: Session, cliente_id: int, cliente_data: dict):
  cliente = session.query(Cliente).filter(Cliente.id == cliente_id).first()
  if cliente:
    for key, value in cliente_data.items():
      setattr(cliente, key, value)
    session.flush()
    session.refresh(cliente)
    return cliente
  else:
    raise NotFoundException(f"Cliente com id {cliente_id} não encontrado.")

def delete(session: Session, cliente_id: int):
  cliente = session.query(Cliente).filter(Cliente.id == cliente_id).first()
  if not cliente:
    raise NotFoundException(f"Cliente com id {cliente_id} não encontrado.")
    
  cliente_is_related = session.query(OrdemServico).filter(OrdemServico.cliente_id == cliente_id).first()
  if cliente_is_related:
    raise BadRequestException(f"Cliente com id {cliente_id} está relacionado a uma ordem de serviço.")  
  
  session.delete(cliente)
  session.flush()
  return cliente