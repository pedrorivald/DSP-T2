from sqlalchemy.orm import Session
from sqlalchemy import func
from exceptions.exceptions import BadRequestException, NotFoundException
from models.models import Cliente, Mecanico, OrdemServico, OrdemServicoPeca, OrdemServicoServico, Peca, Servico
from datetime import datetime, timezone

from schemas.cliente_schema import ClienteResponse
from schemas.mecanico_schema import MecanicoResponse
from schemas.ordem_servico_schema import OrdemServicoCreate, OrdemServicoFullResponse, OrdemServicoPecaResponse, OrdemServicoServicoResponse, OrdemServicoUpdate

class OrdemServicoRepository:
  
  def __init__(self, session: Session):
    self.session = session

  def create(self, data: OrdemServicoCreate):
    # Verificar se o cliente existe
    cliente = self.session.query(Cliente).filter(Cliente.id == data.cliente_id).first()
    if not cliente:
      raise NotFoundException(f"Cliente com id {data.cliente_id} não encontrado.")
    
    # Verificar se o mecanico existe
    mecanico = self.session.query(Mecanico).filter(Mecanico.id == data.mecanico_id).first()
    if not mecanico:
      raise NotFoundException(f"Mecânico com id {data.mecanico_id} não encontrado.")
          
    ordem_servico = OrdemServico(cliente_id=data.cliente_id, mecanico_id=data.mecanico_id)
    
    ordem_servico.data_abertura = datetime.now(timezone.utc)
    ordem_servico.situacao = "pendente"
    ordem_servico.data_conclusao = None
    
    self.session.add(ordem_servico)
    self.session.commit()
    self.session.refresh(ordem_servico)
    
    # Associar os serviços
    for servico_id in data.servicos:
      servico = self.session.query(Servico).filter(Servico.id == servico_id).first()
      if not servico:
        raise NotFoundException(f"Serviço com id {servico_id} não encontrado.")
      
      ordem_servico_servico = OrdemServicoServico(
        ordem_servico_id=ordem_servico.id,
        servico_id=servico_id
      )
      self.session.add(ordem_servico_servico)

    # Associar as peças
    for peca_item in data.pecas:
      peca = self.session.query(Peca).filter(Peca.id == peca_item.peca_id).first()
      if not peca:
        raise NotFoundException(f"Peça com id {peca_item.peca_id} não encontrada.")
      
      ordem_servico_peca = OrdemServicoPeca(
        ordem_servico_id=ordem_servico.id,
        peca_id=peca_item.peca_id,
        quantidade=peca_item.quantidade
      )
      self.session.add(ordem_servico_peca)

    # Atualizar o valor total da ordem de serviço
    ordem_servico = self.update_valor_total(ordem_servico.id)

    return ordem_servico
  
  def update_valor_total(self, ordem_servico_id: int):
    valor_servicos = self.session.query(func.sum(Servico.valor))\
      .join(OrdemServicoServico)\
      .filter(OrdemServicoServico.ordem_servico_id == ordem_servico_id)\
      .scalar() or 0

    valor_pecas = self.session.query(func.sum(Peca.valor * OrdemServicoPeca.quantidade))\
      .join(OrdemServicoPeca)\
      .filter(OrdemServicoPeca.ordem_servico_id == ordem_servico_id)\
      .scalar() or 0

    valor_total = valor_servicos + valor_pecas
    
    ordem_servico = self.session.query(OrdemServico).filter(OrdemServico.id == ordem_servico_id).first()
    ordem_servico.valor = valor_total
    self.session.commit()
    self.session.refresh(ordem_servico)
    return ordem_servico
  
  def list(self, skip: int = 0, limit: int = 5, filtros = []):
    return self.session.query(OrdemServico)\
      .join(Cliente)\
      .join(Mecanico)\
      .filter(*filtros)\
      .order_by(OrdemServico.data_abertura.desc())\
      .offset(skip).limit(limit).all()

  def get(self, ordem_servico_id: int):
    ordem_servico_data = self.session.query(OrdemServico, Cliente, Mecanico)\
      .join(Cliente, Cliente.id == OrdemServico.cliente_id)\
      .join(Mecanico, Mecanico.id == OrdemServico.mecanico_id)\
      .filter(OrdemServico.id == ordem_servico_id).first()
      
    if not ordem_servico_data:
      raise NotFoundException("Ordem de serviço não encontrada.")
      
    ordem_servico, cliente, mecanico = ordem_servico_data
    
    servicos = self.session.query(Servico).join(OrdemServicoServico)\
      .filter(OrdemServicoServico.ordem_servico_id == ordem_servico.id).all()
      
    pecas = self.session.query(Peca, OrdemServicoPeca.quantidade)\
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

  def update(self, ordem_servico_id: int, data: OrdemServicoUpdate):
    ordem_servico = self.session.query(OrdemServico).filter(OrdemServico.id == ordem_servico_id).first()
    if not ordem_servico:
      raise NotFoundException("Ordem de serviço não encontrada.")
    
    cliente = self.session.query(Cliente).filter(Cliente.id == data.cliente_id).first()
    if not cliente:
      raise NotFoundException("Cliente não encontrado.")
    
    mecanico = self.session.query(Mecanico).filter(Mecanico.id == data.mecanico_id).first()
    if not mecanico:
      raise NotFoundException("Mecânico não encontrado.")
    
    ordem_servico.cliente_id = data.cliente_id
    ordem_servico.mecanico_id = data.mecanico_id
    
    self.session.commit()
    self.session.refresh(ordem_servico)
    return ordem_servico
      

  def delete(self, ordem_servico_id: int):
    ordem_servico = self.session.query(OrdemServico).filter(OrdemServico.id == ordem_servico_id).first()
    if ordem_servico:
      self.session.delete(ordem_servico)
      self.session.commit()
      return ordem_servico
    else:
      raise NotFoundException("Ordem de serviço não encontrada.")

  def concluir(self, ordem_servico_id: int):
    ordem_servico: OrdemServico = self.session.query(OrdemServico).filter(OrdemServico.id == ordem_servico_id).first()
    
    if not ordem_servico:
      raise NotFoundException("Ordem de serviço não encontrada.")
    
    if ordem_servico.situacao == "finalizada":
      raise BadRequestException("Ordem de serviço já foi finalizada.")
    
    # Calcular o valor total dos serviços
    valor_total_servicos = self.session.query(func.sum(Servico.valor))\
      .join(OrdemServicoServico)\
      .filter(OrdemServicoServico.ordem_servico_id == ordem_servico_id)\
      .scalar()
      
    # Calcular o valor total das peças
    valor_total_pecas = self.session.query(func.sum(Peca.valor * OrdemServicoPeca.quantidade))\
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
    
    self.session.commit()
    self.session.refresh(ordem_servico)
    return ordem_servico

  def remove_servico(self, ordem_servico_id: int, servico_id: int):
    ordem_servico = self.session.query(OrdemServico).filter(OrdemServico.id == ordem_servico_id).first()
    if not ordem_servico:
      raise NotFoundException("Ordem de serviço não encontrada.")
    
    servico = self.session.query(Servico).filter(Servico.id == servico_id).first()
    if not servico:
      raise NotFoundException("Serviço não encontrado.")
    
    ordem_servico_servico = self.session.query(OrdemServicoServico)\
      .filter(OrdemServicoServico.ordem_servico_id == ordem_servico_id, OrdemServicoServico.servico_id == servico_id).first()
      
    if not ordem_servico_servico:
      raise BadRequestException("Serviço não está relacionado com essa ordem de serviço.")
    
    self.session.delete(ordem_servico_servico)
    self.session.commit()
    
    self.update_valor_total(ordem_servico.id)
    
    return ordem_servico_servico

  def add_servico(self, ordem_servico_id: int, servico_id):
    ordem_servico = self.session.query(OrdemServico).filter(OrdemServico.id == ordem_servico_id).first()
    if not ordem_servico:
      raise NotFoundException("Ordem de serviço não encontrada.")
    
    servico = self.session.query(Servico).filter(Servico.id == servico_id).first()
    if not servico:
      raise NotFoundException("Serviço não encontrado.")
    
    ordem_servico_servico = OrdemServicoServico(ordem_servico_id, servico_id)
    self.session.add(ordem_servico_servico)
    self.session.commit()
    self.session.refresh(ordem_servico_servico)
    
    self.update_valor_total(ordem_servico.id)
    
    return ordem_servico_servico
    
  def add_peca(self, ordem_servico_id: int, data: any):
    ordem_servico = self.session.query(OrdemServico).filter(OrdemServico.id == ordem_servico_id).first()
    if not ordem_servico:
      raise NotFoundException("Ordem de serviço não encontrada.")
    
    peca = self.session.query(Peca).filter(Peca.id == data.peca_id).first()
    if not peca:
      raise NotFoundException("Peça não encontrada.")
    
    ordem_servico_peca = self.session.query(OrdemServicoPeca)\
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
      self.session.add(nova_peca)

    self.session.commit()
    self.session.refresh(nova_peca)
    
    self.update_valor_total(ordem_servico.id)
    
    return nova_peca

  def remove_peca(self, ordem_servico_id: int, peca_id: int):
    ordem_servico = self.session.query(OrdemServico).filter(OrdemServico.id == ordem_servico_id).first()
    if not ordem_servico:
      raise NotFoundException("Ordem de serviço não encontrada.")
    
    peca = self.session.query(Peca).filter(Peca.id == peca_id).first()
    if not peca:
      raise NotFoundException("Peça não encontrada.")
    
    ordem_servico_peca = self.session.query(OrdemServicoPeca)\
      .filter(OrdemServicoPeca.ordem_servico_id == ordem_servico_id, OrdemServicoPeca.peca_id == peca_id).first()
    if not ordem_servico_peca:
      raise BadRequestException("Peça não está relacionada com essa ordem de serviço.")
    
    self.session.delete(ordem_servico_peca)
    self.session.commit()
    
    self.update_valor_total(ordem_servico.id)
    
    return ordem_servico_peca