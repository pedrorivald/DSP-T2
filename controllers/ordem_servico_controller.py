from fastapi import APIRouter, Depends, Query
from sqlalchemy import and_
from sqlalchemy.orm import Session
from db.database import SessionLocal
from models.models import Cliente, Mecanico, OrdemServico
from schemas.ordem_servico_schema import OrdemServicoCreate, OrdemServicoFullResponse, OrdemServicoPaginatedResponse, OrdemServicoPecaCreate, OrdemServicoResponse, OrdemServicoUpdate
import repositories.ordem_servico_repository as ordem_servico_repository
from datetime import datetime

router = APIRouter(prefix="/ordens_servicos", tags=["Ordens de Serviços"])

def get_session():
  session = SessionLocal()
  try:
    yield session
  finally:
    session.close()
    
ordem_servico_repository = ordem_servico_repository.OrdemServicoRepository(session=next(get_session()))
    
@router.post("/", response_model=OrdemServicoResponse)
async def create(ordem_servico: OrdemServicoCreate, session: Session = Depends(get_session)):
  return ordem_servico_repository.create(data=ordem_servico)

@router.get("/", response_model=OrdemServicoPaginatedResponse)
def list(
  skip: int = Query(0, ge=0), 
  limit: int = Query(5, le=100), 
  mecanico_id: int = Query(None, alias="mecanico_id"),
  cliente_id: int = Query(None, alias="cliente_id"),
  nome_mecanico: str = Query(None, alias="nome_mecanico"),
  nome_cliente: str = Query(None, alias="nome_cliente"),
  data_abertura_inicio: datetime = Query(None, alias="data_abertura_inicio"),
  data_abertura_fim: datetime = Query(None, alias="data_abertura_fim"),
  session: Session = Depends(get_session)
):
  
  filtros = []
  if mecanico_id:
    filtros.append(OrdemServico.mecanico_id == mecanico_id)
  if cliente_id:
    filtros.append(OrdemServico.cliente_id == cliente_id)
  if nome_mecanico:
    filtros.append(Mecanico.nome.ilike(f"%{nome_mecanico}%"))
  if nome_cliente:
    filtros.append(Cliente.nome.ilike(f"%{nome_cliente}%"))
  if data_abertura_inicio and data_abertura_fim:
    filtros.append(and_(OrdemServico.data_abertura >= data_abertura_inicio, OrdemServico.data_abertura <= data_abertura_fim))
  
  ordens_servicos = ordem_servico_repository.list(session, skip, limit, filtros)
  
  resultado = []
  for ordem in ordens_servicos:
    resultado.append({
      "cliente": {
        "id": ordem.cliente.id,
        "nome": ordem.cliente.nome,
        "sobrenome": ordem.cliente.sobrenome,
        "endereco": ordem.cliente.endereco,
        "telefone": ordem.cliente.telefone
      },
      "mecanico": {
        "id": ordem.mecanico.id,
        "nome": ordem.mecanico.nome,
        "sobrenome": ordem.mecanico.sobrenome,
        "telefone": ordem.mecanico.telefone,
        "email": ordem.mecanico.email
      },
      "data_abertura": ordem.data_abertura,
      "data_conclusao": ordem.data_conclusao,
      "valor": ordem.valor,
      "situacao": ordem.situacao
    })

  return {
    "ordens_servicos": resultado,
    "pagination": {
      "skip": skip,
      "limit": limit,
    }
  } 

@router.get("/{ordem_servico_id}", response_model=OrdemServicoFullResponse)
def get(ordem_servico_id: int, session: Session = Depends(get_session)):
  return ordem_servico_repository.get(session, ordem_servico_id)
  
@router.put("/{ordem_servico_id}", response_model=OrdemServicoResponse)
async def update(ordem_servico_id: int, ordem_servico: OrdemServicoUpdate, session: Session = Depends(get_session)):
  return ordem_servico_repository.update(session, ordem_servico_id, ordem_servico.dict())

@router.delete("/{ordem_servico_id}", response_model=OrdemServicoResponse)
async def delete(ordem_servico_id: int, session: Session = Depends(get_session)):
  return ordem_servico_repository.delete(session, ordem_servico_id)
  
@router.patch("/{ordem_servico_id}/concluir", response_model=OrdemServicoResponse)
async def conclude(ordem_servico_id: int, session: Session = Depends(get_session)):
  return ordem_servico_repository.concluir(session, ordem_servico_id)

@router.delete("/{ordem_servico_id}/pecas/{peca_id}", response_model=OrdemServicoResponse)
async def remove_peca(ordem_servico_id: int, peca_id: int, session: Session = Depends(get_session)):
  return ordem_servico_repository.remove_peca(session, ordem_servico_id, peca_id)

@router.delete("/{ordem_servico_id}/servicos/{servico_id}", response_model=OrdemServicoResponse)
async def remove_servico(ordem_servico_id: int, servico_id: int, session: Session = Depends(get_session)):
  return ordem_servico_repository.remove_servico(session, ordem_servico_id, servico_id)

@router.post("/{ordem_servico_id}/pecas", response_model=OrdemServicoResponse)
async def add_peca(ordem_servico_id: int, peca: OrdemServicoPecaCreate, session: Session = Depends(get_session)):
  return ordem_servico_repository.add_peca(session, ordem_servico_id, peca)

@router.post("/{ordem_servico_id}/servicos", response_model=OrdemServicoResponse)
async def add_servico(ordem_servico_id: int, servico_id: int, session: Session = Depends(get_session)):
  return ordem_servico_repository.add_servico(session, ordem_servico_id, servico_id)