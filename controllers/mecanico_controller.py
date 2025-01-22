from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from db.database import SessionLocal
from schemas.mecanico_schema import MecanicoCreate, MecanicoPaginatedResponse, MecanicoResponse, MecanicoUpdate
import repositories.mecanico_repository as mecanico_repository

router = APIRouter(prefix="/mecanicos", tags=["Mecanicos"])

def get_session():
  session = SessionLocal()
  try:
    yield session
  finally:
    session.close()
    
@router.post("/", response_model=MecanicoResponse)
async def create(mecanico: MecanicoCreate, session: Session = Depends(get_session)):
  return mecanico_repository.create(session, mecanico.dict())

@router.get("/", response_model=MecanicoPaginatedResponse)
def list(skip: int = Query(0, ge=0), limit: int = Query(5, le=100), session: Session = Depends(get_session)):
  mecanicos = mecanico_repository.list(session, skip, limit)

  return {
    "mecanicos": mecanicos,
    "pagination": {
      "skip": skip,
      "limit": limit,
    }
  } 

@router.get("/{mecanico_id}", response_model=MecanicoResponse)
def get(mecanico_id: int, session: Session = Depends(get_session)):
  return mecanico_repository.get(session, mecanico_id)
  
@router.put("/{mecanico_id}", response_model=MecanicoResponse)
async def update(mecanico_id: int, mecanico: MecanicoUpdate, session: Session = Depends(get_session)):
  return mecanico_repository.update(session, mecanico_id, mecanico.dict())
  
@router.delete("/{mecanico_id}", response_model=MecanicoResponse)
async def delete(mecanico_id: int, session: Session = Depends(get_session)):
  return mecanico_repository.delete(session, mecanico_id)
