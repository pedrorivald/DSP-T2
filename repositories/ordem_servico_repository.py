from sqlalchemy.orm import Session
from sqlalchemy import func
from exceptions.exceptions import BadRequestException, NotFoundException
from models.models import Cliente, Mecanico, OrdemServico, OrdemServicoPeca, OrdemServicoServico, Peca, Servico
from datetime import datetime, timezone

from schemas.cliente_schema import ClienteResponse
from schemas.mecanico_schema import MecanicoResponse
from schemas.ordem_servico_schema import OrdemServicoCreate, OrdemServicoFullResponse, OrdemServicoPecaResponse, OrdemServicoServicoResponse, OrdemServicoUpdate

def create(session: Session, data: OrdemServicoCreate):
  # Verificar se o cliente existe
  cliente = session.query(Cliente).filter(Cliente.id == data.cliente_id).first()
  if not cliente:
    raise NotFoundException(f"Cliente com id {data.cliente_id} não encontrado.")
  
  # Verificar se o mecanico existe
  mecanico = session.query(Mecanico).filter(Mecanico.id == data.mecanico_id).first()
  if not mecanico:
    raise NotFoundException(f"Mecânico com id {data.mecanico_id} não encontrado.")
        
  ordem_servico = OrdemServico(
    cliente_id=data.cliente_id, 
    mecanico_id=data.mecanico_id,
    data_abertura = datetime.now(timezone.utc),
    situacao = "pendente",
    data_conclusao = None,
    valor = None
  )
  
  session.add(ordem_servico)
  session.flush()
  session.refresh(ordem_servico)

  return ordem_servico

def list(session: Session, skip: int = 0, limit: int = 5, filtros = []):
  return session.query(OrdemServico)\
    .join(Cliente)\
    .join(Mecanico)\
    .filter(*filtros)\
    .order_by(OrdemServico.data_abertura.desc())\
    .offset(skip).limit(limit).all()

def get(session: Session, ordem_servico_id: int):
  ordem_servico_data = session.query(OrdemServico, Cliente, Mecanico)\
    .join(Cliente, Cliente.id == OrdemServico.cliente_id)\
    .join(Mecanico, Mecanico.id == OrdemServico.mecanico_id)\
    .filter(OrdemServico.id == ordem_servico_id).first()
    
  if not ordem_servico_data:
    raise NotFoundException("Ordem de serviço não encontrada.")
    
  ordem_servico, cliente, mecanico = ordem_servico_data
  
  servicos = session.query(Servico).join(OrdemServicoServico)\
    .filter(OrdemServicoServico.ordem_servico_id == ordem_servico.id).all()
    
  pecas = session.query(Peca, OrdemServicoPeca.quantidade)\
    .join(OrdemServicoPeca).filter(OrdemServicoPeca.ordem_servico_id == ordem_servico.id).all()
    
      
  return OrdemServicoFullResponse(
    id=ordem_servico.id,
    data_abertura=ordem_servico.data_abertura,
    data_conclusao=ordem_servico.data_conclusao,
    situacao=ordem_servico.situacao,
    valor=ordem_servico.valor,
    cliente=ClienteResponse(
      id=cliente.id,
      nome=cliente.nome,
      sobrenome=cliente.sobrenome,
      endereco=cliente.endereco,
      telefone=cliente.telefone
    ),
    mecanico=MecanicoResponse(
      id=mecanico.id,
      nome=mecanico.nome,
      sobrenome=mecanico.sobrenome,
      telefone=mecanico.telefone,
      email=mecanico.email
    ),
    servicos=[OrdemServicoServicoResponse(
      id=servico.id,
      nome=servico.nome,
      valor=servico.valor,
      categoria=servico.categoria,
    ) for servico in servicos],
    pecas=[OrdemServicoPecaResponse(
      id=peca.id,
      nome=peca.nome,
      marca=peca.marca,
      modelo=peca.modelo,
      valor=peca.valor,
      quantidade=quantidade,
    ) for peca, quantidade in pecas]
  )

def update(session: Session, ordem_servico_id: int, data: OrdemServicoUpdate):
  ordem_servico = session.query(OrdemServico).filter(OrdemServico.id == ordem_servico_id).first()
  if not ordem_servico:
    raise NotFoundException("Ordem de serviço não encontrada.")
  
  if ordem_servico.situacao == "concluida":
    raise BadRequestException("Ordem de serviço já foi concluida.")
  
  cliente = session.query(Cliente).filter(Cliente.id == data.cliente_id).first()
  if not cliente:
    raise NotFoundException("Cliente não encontrado.")
  
  mecanico = session.query(Mecanico).filter(Mecanico.id == data.mecanico_id).first()
  if not mecanico:
    raise NotFoundException("Mecânico não encontrado.")
  
  ordem_servico.cliente_id = data.cliente_id
  ordem_servico.mecanico_id = data.mecanico_id
  
  session.flush()
  session.refresh(ordem_servico)
  return ordem_servico
    
def delete(session: Session, ordem_servico_id: int):
  ordem_servico = session.query(OrdemServico).filter(OrdemServico.id == ordem_servico_id).first()
  if ordem_servico:
    session.delete(ordem_servico)
    session.flush()
    
    return ordem_servico
  else:
    raise NotFoundException("Ordem de serviço não encontrada.")

def concluir(session: Session, ordem_servico_id: int):
  ordem_servico: OrdemServico = session.query(OrdemServico).filter(OrdemServico.id == ordem_servico_id).first()
  
  if not ordem_servico:
    raise NotFoundException("Ordem de serviço não encontrada.")
  
  if ordem_servico.situacao == "concluida":
    raise BadRequestException("Ordem de serviço já foi concluida.")
  
  # Calcular o valor total dos serviços
  valor_total_servicos = session.query(func.sum(Servico.valor))\
    .join(OrdemServicoServico)\
    .filter(OrdemServicoServico.ordem_servico_id == ordem_servico_id)\
    .scalar()
    
  # Calcular o valor total das peças
  valor_total_pecas = session.query(func.sum(Peca.valor * OrdemServicoPeca.quantidade))\
    .join(OrdemServicoPeca)\
    .filter(OrdemServicoPeca.ordem_servico_id == ordem_servico_id)\
    .scalar()
      
  # Caso não haja serviços ou peças, o valor será 0
  valor_total_servicos = valor_total_servicos if valor_total_servicos is not None else 0
  valor_total_pecas = valor_total_pecas if valor_total_pecas is not None else 0
  
  valor_total = valor_total_servicos + valor_total_pecas
  
  ordem_servico.valor = valor_total
  ordem_servico.situacao = "concluida"
  ordem_servico.data_conclusao = datetime.now(timezone.utc)
  
  session.flush()
  session.refresh(ordem_servico)
  return ordem_servico

def remove_servico(session: Session, ordem_servico_id: int, servico_id: int):
  ordem_servico = session.query(OrdemServico).filter(OrdemServico.id == ordem_servico_id).first()
  if not ordem_servico:
    raise NotFoundException("Ordem de serviço não encontrada.")
  
  if ordem_servico.situacao == "concluida":
    raise BadRequestException("Ordem de serviço já foi concluida.")
  
  servico = session.query(Servico).filter(Servico.id == servico_id).first()
  if not servico:
    raise NotFoundException("Serviço não encontrado.")
  
  ordem_servico_servico = session.query(OrdemServicoServico)\
    .filter(OrdemServicoServico.ordem_servico_id == ordem_servico_id, OrdemServicoServico.servico_id == servico_id).first()
    
  if not ordem_servico_servico:
    raise BadRequestException("Serviço não está relacionado com essa ordem de serviço.")
  
  session.delete(ordem_servico_servico)
  session.flush()
  
  return { "message": "Serviço removido da ordem de serviço." }

def add_servico(session: Session, ordem_servico_id: int, servico_id):
  ordem_servico = session.query(OrdemServico).filter(OrdemServico.id == ordem_servico_id).first()
  if not ordem_servico:
    raise NotFoundException("Ordem de serviço não encontrada.")
  
  if ordem_servico.situacao == "concluida":
    raise BadRequestException("Ordem de serviço já foi concluida.")
  
  servico = session.query(Servico).filter(Servico.id == servico_id).first()
  if not servico:
    raise NotFoundException("Serviço não encontrado.")
  
  ordem_servico_servico = OrdemServicoServico(ordem_servico_id=ordem_servico_id, servico_id=servico_id)
  session.add(ordem_servico_servico)
  session.flush()
  
  return { "message": "Serviço adicionado na ordem de serviço." }
  
def add_peca(session: Session, ordem_servico_id: int, data: any):
  ordem_servico = session.query(OrdemServico).filter(OrdemServico.id == ordem_servico_id).first()
  if not ordem_servico:
    raise NotFoundException("Ordem de serviço não encontrada.")
  
  if ordem_servico.situacao == "concluida":
    raise BadRequestException("Ordem de serviço já foi concluida.")
  
  peca = session.query(Peca).filter(Peca.id == data.peca_id).first()
  if not peca:
    raise NotFoundException("Peça não encontrada.")
  
  ordem_servico_peca = session.query(OrdemServicoPeca)\
    .filter(OrdemServicoPeca.ordem_servico_id == ordem_servico_id, OrdemServicoPeca.peca_id == data.peca_id).first()

  if ordem_servico_peca:
    # Atualiza a quantidade se a peça já estiver associada
    ordem_servico_peca.quantidade += data.quantidade
  else:
    # Adiciona nova peça à ordem
    nova_peca = OrdemServicoPeca(
      ordem_servico_id=ordem_servico_id,
      peca_id=data.peca_id,
      quantidade=data.quantidade
    )
    session.add(nova_peca)

  session.flush()
  
  return { "message": "Peça adicionada na ordem de serviço." }

def remove_peca(session: Session, ordem_servico_id: int, peca_id: int):
  ordem_servico = session.query(OrdemServico).filter(OrdemServico.id == ordem_servico_id).first()
  if not ordem_servico:
    raise NotFoundException("Ordem de serviço não encontrada.")
  
  if ordem_servico.situacao == "concluida":
    raise BadRequestException("Ordem de serviço já foi concluida.")
  
  peca = session.query(Peca).filter(Peca.id == peca_id).first()
  if not peca:
    raise NotFoundException("Peça não encontrada.")
  
  ordem_servico_peca = session.query(OrdemServicoPeca)\
    .filter(OrdemServicoPeca.ordem_servico_id == ordem_servico_id, OrdemServicoPeca.peca_id == peca_id).first()
  if not ordem_servico_peca:
    raise BadRequestException("Peça não está relacionada com essa ordem de serviço.")
  
  session.delete(ordem_servico_peca)
  session.flush()
  
  return { "message": "Peça removida da ordem de serviço." }