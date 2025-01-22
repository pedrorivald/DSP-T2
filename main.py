from fastapi import FastAPI, HTTPException
from controllers import mecanico_controller, cliente_controller, servico_controller, peca_controller, ordem_servico_controller
from exceptions.exceptions import BadRequestException, InternalServerErrorException, NotFoundException
from exceptions.global_exception_handler import bad_request_exception_handler, global_exception_handler, http_exception_handler, internal_server_error_exception_handler, not_found_exception_handler

app = FastAPI(title="Oficina Mecânica")

app.add_exception_handler(NotFoundException, not_found_exception_handler)
app.add_exception_handler(BadRequestException, bad_request_exception_handler)
app.add_exception_handler(InternalServerErrorException, internal_server_error_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)

app.include_router(mecanico_controller.router)
app.include_router(cliente_controller.router)
app.include_router(servico_controller.router)
app.include_router(peca_controller.router)
app.include_router(ordem_servico_controller.router)

@app.get("/")
def root():
  return {"message": "API funcionando corretamente!"}
