# Desenvolvimento

python -m venv venv

venv\Scripts\activate

pip install sqlalchemy alembic fastapi uvicorn pydantic

alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
alembic downgrade -1

uvicorn main:app --reload --port 8000

