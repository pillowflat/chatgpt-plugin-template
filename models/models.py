from pydantic import BaseModel

class Query(BaseModel):
    id: str
    query: str

class QueryResult(BaseModel):
    id: str
    result: str