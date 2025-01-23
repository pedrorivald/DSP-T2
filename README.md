# Desenvolvimento

python -m venv venv

venv\Scripts\activate

pip install sqlalchemy alembic fastapi uvicorn pydantic

alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
alembic downgrade -1

uvicorn main:app --reload --port 8000

# Rodar no Docker
`docker build -t dsp-t2 .`
`docker run -d -p 8000:8000 dsp-t2`
Acessar em http://localhost:8000