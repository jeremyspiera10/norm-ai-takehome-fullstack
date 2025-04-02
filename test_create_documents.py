from app.utils import DocumentService
from app.schemas import PydanticDocument

if __name__ == "__main__":
    service = DocumentService()
    raw_docs = service.create_documents()

    docs = [PydanticDocument.from_llama(doc) for doc in raw_docs]

    print(f"✅ Parsed {len(docs)} documents.\n")

    for i, doc in enumerate(docs[:3]):
        print(f"--- Document {i + 1} ---")
        print(f"Title: {doc.title}")
        print(f"Content preview:\n{doc.text[:300]}...\n")