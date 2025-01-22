from fastapi import HTTPException

class NotFoundException(HTTPException):
  def __init__(self, detail: str = "Recurso não encontrado"):
    super().__init__(status_code=404, detail=detail)

class BadRequestException(HTTPException):
  def __init__(self, detail: str = "Requisição inválida"):
    super().__init__(status_code=400, detail=detail)

class InternalServerErrorException(HTTPException):
  def __init__(self, detail: str = "Erro interno do servidor"):
    super().__init__(status_code=500, detail=detail)
