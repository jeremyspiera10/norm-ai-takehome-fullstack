from typing import List
from fastapi import FastAPI, Query
from app.schemas import PydanticDocument
from app.utils import DocumentService, Output, QdrantService

app = FastAPI()

document_service = DocumentService()
docs = document_service.create_documents()

qdrant = QdrantService()
qdrant.connect()
qdrant.load(docs)

@app.get("/test-docs", response_model=List[PydanticDocument])
def test_docs():
    docs = DocumentService().create_documents()
    return [PydanticDocument.from_llama(doc) for doc in docs]

"""
Please create an endpoint that accepts a query string, e.g., "what happens if I steal 
from the Sept?" and returns a JSON response serialized from the Pydantic Output class.
"""

@app.get("/query", response_model = Output)
def request_query(query: str = Query(..., description="Sample Question")):
    resp = qdrant.query(query)
    return resp
