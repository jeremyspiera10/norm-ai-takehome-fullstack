from typing import List
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import PydanticDocument
from app.utils import DocumentService, Output, QdrantService

app = FastAPI()

# Add CORS middleware to allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

document_service = DocumentService()
docs = document_service.create_documents()

qdrant = QdrantService()
qdrant.connect()
qdrant.load(docs)

@app.get("/test-docs", response_model=List[PydanticDocument])
def test_docs():
    docs = DocumentService().create_documents()
    return [PydanticDocument.from_llama(doc) for doc in docs]

@app.get("/query", response_model = Output)
def request_query(query: str = Query(..., description="Sample Question")):
    resp = qdrant.query(query)
    return resp
