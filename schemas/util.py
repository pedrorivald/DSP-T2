from pydantic import BaseModel

class Pagination(BaseModel):
  skip: int
  limit: int
