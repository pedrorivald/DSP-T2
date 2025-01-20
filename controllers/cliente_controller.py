# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from db.database import SessionLocal
# from schemas.mecanico_schema import 

# router = APIRouter(prefix="/clientes", tags=["Clientes"])

# def get_db():
#   db = SessionLocal()
#   try:
#     yield db
#   finally:
#     db.close()


# @router.post("/clientes/")
# def add_cliente(cliente: ClienteCreate, session: Session = Depends(get_session)):
#   return create_cliente(session, cliente.dict())

# @router.get("/clientes/")
# def list_clientes(session: Session = Depends(get_session)):
#   return get_clientes(session)