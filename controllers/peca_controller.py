from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from db.database import SessionLocal
from schemas.peca_schema import PecaCreate, PecaPaginatedResponse, PecaResponse, PecaUpdate
import repositories.peca_repository as peca_repository

router = APIRouter(prefix="/pecas", tags=["Pecas"])

def get_session():
  session = SessionLocal()
  try:
    yield session
  finally:
    session.close()
    
@router.post("/", response_model=PecaResponse)
async def create(peca: PecaCreate, session: Session = Depends(get_session)):
  return peca_repository.create(session, peca.dict())

@router.get("/", response_model=PecaPaginatedResponse)
def list(skip: int = Query(0, ge=0), limit: int = Query(5, le=100), session: Session = Depends(get_session)):
  pecas = peca_repository.list(session, skip, limit)

  return {
    "pecas": pecas,
    "pagination": {
      "skip": skip,
      "limit": limit,
    }
  } 
    

@router.get("/{peca_id}", response_model=PecaResponse)
def get(peca_id: int, session: Session = Depends(get_session)):
  return peca_repository.get(session, peca_id)
  
@router.put("/{peca_id}", response_model=PecaResponse)
async def update(peca_id: int, peca: PecaUpdate, session: Session = Depends(get_session)):
  return peca_repository.update(session, peca_id, peca.dict())

@router.delete("/{peca_id}", response_model=PecaResponse)
async def delete(peca_id: int, session: Session = Depends(get_session)):
  return peca_repository.delete(session, peca_id)