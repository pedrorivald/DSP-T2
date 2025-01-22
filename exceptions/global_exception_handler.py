import logging

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

from exceptions.exceptions import BadRequestException, InternalServerErrorException, NotFoundException

logger = logging.getLogger(__name__)

async def global_exception_handler(request: Request, exc: Exception):
  logger.error(f"Erro inesperado: {exc}")
  return JSONResponse(
    status_code=500,
    content={"message": "Ocorreu um erro interno no servidor"},
  )

async def http_exception_handler(request: Request, exc: HTTPException):
  return JSONResponse(
    status_code=exc.status_code,
    content={"message": exc.detail},
  )
  
async def not_found_exception_handler(request, exc: NotFoundException):
  return JSONResponse(
    status_code=404,
    content={"message": exc.detail},
  )

async def bad_request_exception_handler(request, exc: BadRequestException):
  return JSONResponse(
    status_code=400,
    content={"message": exc.detail},
  )
  
async def internal_server_error_exception_handler(request, exc: InternalServerErrorException):
  return JSONResponse(
    status_code=500,
    content={"message": exc.detail},
  )