from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from db.database import SessionLocal
from schemas.servico_schema import ServicoCreate, ServicoPaginatedResponse, ServicoResponse, ServicoUpdate
import repositories.servico_repository as servico_repository

router = APIRouter(prefix="/servicos", tags=["Servicos"])

def get_session():
  session = SessionLocal()
  try:
    yield session
  finally:
    session.close()
    
@router.post("/", response_model=ServicoResponse)
async def create(servico: ServicoCreate, session: Session = Depends(get_session)):
  return servico_repository.create(session, servico.dict())

@router.get("/", response_model=ServicoPaginatedResponse)
def list(skip: int = Query(0, ge=0), limit: int = Query(5, le=100), session: Session = Depends(get_session)):
  servicos = servico_repository.list(session, skip, limit)

  return {
    "servicos": servicos,
    "pagination": {
      "skip": skip,
      "limit": limit,
    }
  } 

@router.get("/{servico_id}", response_model=ServicoResponse)
def get(servico_id: int, session: Session = Depends(get_session)):
  return servico_repository.get(session, servico_id)
  
@router.put("/{servico_id}", response_model=ServicoResponse)
async def update(servico_id: int, servico: ServicoUpdate, session: Session = Depends(get_session)):
  return servico_repository.update(session, servico_id, servico.dict())

@router.delete("/{servico_id}", response_model=ServicoResponse)
async def delete(servico_id: int, session: Session = Depends(get_session)):
  return servico_repository.delete(session, servico_id)