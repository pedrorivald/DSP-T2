from fastapi import APIRouter, Depends, HTTPException, Query
from schemas.util import Pagination
from sqlalchemy.orm import Session
from db.database import SessionLocal
from models.models import Mecanico
from schemas.mecanico_schema import MecanicoCreate, MecanicoPaginatedResponse, MecanicoResponse, MecanicoUpdate
import repositories.mecanico_repository as repo

router = APIRouter(prefix="/mecanicos", tags=["Mecanicos"])

def get_session():
  session = SessionLocal()
  try:
    yield session
  finally:
    session.close()
    
@router.post("/", response_model=MecanicoResponse)
async def create_mecanico(mecanico: MecanicoCreate, session: Session = Depends(get_session)):
  try:
    return repo.create_mecanico(session, mecanico.dict())
  except Exception as e:
    raise HTTPException(status_code=400, detail="Erro ao criar mecânico: " + str(e))

@router.get("/", response_model=MecanicoPaginatedResponse)
def get_mecanicos(skip: int = Query(0, ge=0), limit: int = Query(5, le=100), session: Session = Depends(get_session)):
  try:
    mecanicos = repo.get_mecanicos(session, skip, limit)
  
    return {
      "mecanicos": mecanicos,
      "pagination": {
        "skip": skip,
        "limit": limit,
      }
    }
    
  except Exception as e:
    raise HTTPException(status_code=400, detail="Erro ao listar mecânico: " + str(e))

@router.get("/{mecanico_id}", response_model=MecanicoResponse)
def get_mecanico(mecanico_id: int, session: Session = Depends(get_session)):
  try:
    return repo.get_mecanico(session, mecanico_id)
  except Exception as e:
    raise HTTPException(status_code=400, detail="Erro ao obter mecânico: " + str(e))
  
@router.put("/{mecanico_id}", response_model=MecanicoResponse)
async def update_mecanico(mecanico_id: int, mecanico: MecanicoUpdate, session: Session = Depends(get_session)):
  try:
    return repo.update_mecanico(session, mecanico_id, mecanico.dict())
  except Exception as e:
    raise HTTPException(status_code=400, detail="Erro ao atualizar mecânico: " + str(e))
