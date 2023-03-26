from pydantic import BaseModel
from typing import List, Optional

from models.models import (
    Query,
    QueryResult
)

class QueryRequest(BaseModel):
    queries: List[Query]


class QueryResponse(BaseModel):
    results: List[QueryResult]
