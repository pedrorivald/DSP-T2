from fastapi import FastAPI
from controllers import mecanico_controller

app = FastAPI(title="Oficina Mecânica")

app.include_router(mecanico_controller.router)

@app.get("/")
def root():
  return {"message": "API funcionando corretamente!"}
