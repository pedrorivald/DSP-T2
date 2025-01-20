# from sqlalchemy.orm import Session
# from models.models import Cliente

# def create_cliente(session: Session, cliente_data: dict):
#   cliente = Cliente(**cliente_data)
#   session.add(cliente)
#   session.commit()
#   session.refresh(cliente)
#   return cliente
 
# def get_clientes(session: Session):
#   return session.query(Cliente).all()
