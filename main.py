"""
This module defines a FastAPI app with routes for handling queries and getting the plugin configuration. 
The plugin configuration is returned in the JSON format. 

Functions:
- query(request: QueryRequest = Body(...)): A FastAPI POST route that handles incoming queries. It uses the QueryRequest 
    model to parse incoming JSON request bodies and the QueryResponse model to serialize query results into JSON responses. 
    It also catches and logs exceptions that occur during query processing.
- get_plugin(): A FastAPI GET route that returns the plugin configuration in the JSON format.
- custom_api(): A function that generates an OpenAPI schema with custom metadata (i.e., TITLE, VERSION, and DESCRIPTION)
    and attaches it to the FastAPI app. The function uses the get_openapi utility function from FastAPI's openapi.utils 
    module to generate the schema.
"""
import os
from fastapi import FastAPI, HTTPException, Body, Depends
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from services.example_service import get_data
from config import get_plugin_config, TITLE, VERSION, DESCRIPTION

# from dotenv import load_dotenv
# load_dotenv('.env')

from models.api import (
    QueryRequest,
    QueryResponse,
)

app = FastAPI()
bearer_scheme = HTTPBearer()
BEARER_TOKEN = os.environ.get("BEARER_TOKEN")
# assert BEARER_TOKEN is not None

def validate_token(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    if credentials.scheme != "Bearer" or credentials.credentials != BEARER_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid or missing token")
    return credentials

@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest = Body(...)):
    try:
        results = await get_data(request.queries)
        return QueryResponse(results=results)
    except Exception as e:
        print("Error:", e, e)
        raise HTTPException(status_code=500, detail="Internal Service Error")

# /query with auth
# @app.post("/query", response_model=QueryResponse)
# async def query(request: QueryRequest = Body(...), token: HTTPAuthorizationCredentials = Depends(validate_token),):
#     try:
#         results = await get_data(request.queries)
#         return QueryResponse(results=results)
#     except Exception as e:
#         print("Error:", e, e)
#         raise HTTPException(status_code=500, detail="Internal Service Error")


@app.get("/.well-known/ai-plugin.json")
def get_plugin():
    return JSONResponse(content=get_plugin_config())

def custom_api():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=TITLE,
        version=VERSION,
        description=DESCRIPTION,
        routes=app.routes
    )

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_api

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
