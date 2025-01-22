from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from db.database import Base

class Cliente(Base):
  __tablename__ = "cliente"

  id = Column(Integer, primary_key=True, index=True)
  nome = Column(String, nullable=False)
  sobrenome = Column(String, nullable=False)
  endereco = Column(String, nullable=False)
  telefone = Column(String, nullable=False)

  ordens = relationship("OrdemServico", back_populates="cliente")

class Mecanico(Base):
  __tablename__ = "mecanico"

  id = Column(Integer, primary_key=True, index=True)
  nome = Column(String, nullable=False)
  sobrenome = Column(String, nullable=False)
  telefone = Column(String, nullable=False)
  email = Column(String, nullable=False)

  ordens = relationship("OrdemServico", back_populates="mecanico")

class Servico(Base):
  __tablename__ = "servico"

  id = Column(Integer, primary_key=True, index=True)
  nome = Column(String, nullable=False)
  valor = Column(Float, nullable=False)
  ativo = Column(Boolean, nullable=False)
  categoria = Column(String, nullable=False)

class Peca(Base):
  __tablename__ = "peca"

  id = Column(Integer, primary_key=True, index=True)
  nome = Column(String, nullable=False)
  marca = Column(String, nullable=False)
  modelo = Column(String, nullable=False)
  valor = Column(Float, nullable=False)

class OrdemServico(Base):
  __tablename__ = "ordem_servico"

  id = Column(Integer, primary_key=True, index=True)
  cliente_id = Column(Integer, ForeignKey("cliente.id"))
  mecanico_id = Column(Integer, ForeignKey("mecanico.id"))
  data_abertura = Column(DateTime, nullable=False)
  data_conclusao = Column(DateTime, nullable=True)
  situacao = Column(String, nullable=False)
  valor = Column(Float)

  cliente = relationship("Cliente", back_populates="ordens")
  mecanico = relationship("Mecanico", back_populates="ordens")
  
  pecas = relationship("OrdemServicoPeca", cascade="all, delete-orphan", back_populates="ordem_servico")
  servicos = relationship("OrdemServicoServico", cascade="all, delete-orphan", back_populates="ordem_servico")

class OrdemServicoServico(Base):
  __tablename__ = "ordem_servico_servico"

  ordem_servico_id = Column(Integer, ForeignKey("ordem_servico.id"), primary_key=True)
  servico_id = Column(Integer, ForeignKey("servico.id"), primary_key=True)
  
  ordem_servico = relationship("OrdemServico", back_populates="servicos")

class OrdemServicoPeca(Base):
  __tablename__ = "ordem_servico_peca"

  ordem_servico_id = Column(Integer, ForeignKey("ordem_servico.id"), primary_key=True)
  peca_id = Column(Integer, ForeignKey("peca.id"), primary_key=True)
  quantidade = Column(Integer, nullable=False)
  
  ordem_servico = relationship("OrdemServico", back_populates="pecas")
