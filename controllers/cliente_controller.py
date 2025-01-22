from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from db.database import SessionLocal
from schemas.cliente_schema import ClienteCreate, ClientePaginatedResponse, ClienteResponse, ClienteUpdate
import repositories.cliente_repository as cliente_repository

router = APIRouter(prefix="/clientes", tags=["Clientes"])

def get_session():
  session = SessionLocal()
  try:
    yield session
  finally:
    session.close()
    
@router.post("/", response_model=ClienteResponse)
async def create(cliente: ClienteCreate, session: Session = Depends(get_session)):
  return cliente_repository.create(session, cliente.dict())

@router.get("/", response_model=ClientePaginatedResponse)
def list(skip: int = Query(0, ge=0), limit: int = Query(5, le=100), session: Session = Depends(get_session)):
  clientes = cliente_repository.list(session, skip, limit)

  return {
    "clientes": clientes,
    "pagination": {
      "skip": skip,
      "limit": limit,
    }
  } 

@router.get("/{cliente_id}", response_model=ClienteResponse)
def get(cliente_id: int, session: Session = Depends(get_session)):
  return cliente_repository.get(session, cliente_id)
  
@router.put("/{cliente_id}", response_model=ClienteResponse)
async def update(cliente_id: int, cliente: ClienteUpdate, session: Session = Depends(get_session)):
  return cliente_repository.update(session, cliente_id, cliente.dict())
  
@router.delete("/{cliente_id}", response_model=ClienteResponse)
async def delete(cliente_id: int, session: Session = Depends(get_session)):
  return cliente_repository.delete(session, cliente_id)
