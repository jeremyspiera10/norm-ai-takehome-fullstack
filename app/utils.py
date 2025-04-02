from pydantic import BaseModel, validator
import qdrant_client
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.core.schema import Document
from llama_index.core import VectorStoreIndex, ServiceContext, Settings
from llama_index.core.query_engine import CitationQueryEngine
from dataclasses import dataclass
from dotenv import load_dotenv
import os
import re
from pdfminer.high_level import extract_text
import pdfplumber
import openai

load_dotenv()
key = os.environ['OPENAI_API_KEY']

@dataclass
class Input:
    query: str
    file_path: str

@dataclass
class Citation:
    source: str
    text: str
    
class Output(BaseModel):
    query: str
    response: str
    citations: list[Citation]

class DocumentService:

    """
    Update this service to load the pdf and extract its contents.
    The example code below will help with the data structured required
    when using the QdrantService.load() method below. Note: for this
    exercise, ignore the subtle difference between llama-index's 
    Document and Node classes (i.e, treat them as interchangeable).

    # example code
    def create_documents() -> list[Document]:

        docs = [
            Document(
                metadata={"Section": "Law 1"},
                text="Theft is punishable by hanging",
            ),
            Document(
                metadata={"Section": "Law 2"},
                text="Tax evasion is punishable by banishment.",
            ),
        ]

        return docs

     """
     
    def create_documents(self, file_path: str = "docs/laws.pdf") -> list[Document]:
        documents = []
        current_title = []
        current_content = []
        
        law_start_re = re.compile(r"^(\d+)\.\s+(.*)")
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                lines = page.extract_text().split("\n")
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue

                    match = law_start_re.match(line)
                    if match:
                        # Save previous law as a document
                        if current_title and current_content:
                            documents.append(
                                Document(
                                    text="\n".join(current_content).strip(),
                                    metadata={"title": current_title}
                                )
                            )
                        current_title = f"{match.group(1)}. {match.group(2).strip()}"
                        current_content = [line]
                    else:
                        current_content.append(line)

        # Don't forget to save the last one
        if current_title and current_content:
            documents.append(
                Document(
                    text="\n".join(current_content).strip(),
                    metadata={"title": current_title}
                )
            )

        print(f"Parsed {len(documents)} laws from the PDF.")
        return documents
        

class QdrantService:
    def __init__(self, k: int = 2):
        self.index = None
        self.k = k
        self.vector_store = None
        self.service_context = None
    
    def connect(self) -> None:
        client = qdrant_client.QdrantClient(location=":memory:")
                
        vstore = QdrantVectorStore(client=client, collection_name='temp')

        
        Settings.llm = OpenAI(api_key=key, model="gpt-4o")
        Settings.embed_model=OpenAIEmbedding()

        self.index = VectorStoreIndex.from_vector_store(
            vector_store=vstore,
        )

    def load(self, docs = list[Document]):
        self.index.insert_nodes(docs)
    
    def query(self, query_str: str) -> Output:

        """
        This method needs to initialize the query engine, run the query, and return
        the result as a pydantic Output class. This is what will be returned as
        JSON via the FastAPI endpount. Fee free to do this however you'd like, but
        a its worth noting that the llama-index package has a CitationQueryEngine...

        Also, be sure to make use of self.k (the number of vectors to return based
        on semantic similarity).

        # Example output object
        citations = [
            Citation(source="Law 1", text="Theft is punishable by hanging"),
            Citation(source="Law 2", text="Tax evasion is punishable by banishment."),
        ]

        output = Output(
            query=query_str, 
            response=response_text, 
            citations=citations
            )
        
        return output

        """
        if not self.index:
            raise ValueError("Index not initialized. Call connect() first.")

        query_engine = CitationQueryEngine.from_args(
            self.index,
            similarity_top_k=self.k
        )

        response = query_engine.query(query_str)

        citations = [
            Citation(
                source=node.metadata.get("title"),
                text=node.node.text
            )
            for node in response.source_nodes
        ]

        return Output(
            query=query_str,
            response=str(response),
            citations=citations
        )
       

if __name__ == "__main__":
    # Example workflow
    doc_serivce = DocumentService() # implemented
    docs = doc_serivce.create_documents() # NOT implemented

    index = QdrantService() # implemented
    index.connect() # implemented
    index.load(docs) # implemented
    output = index.query("what happens if I steal?") # NOT implemented
    print(output)





