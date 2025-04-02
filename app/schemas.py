from dataclasses import dataclass
from pydantic import BaseModel
from typing import Optional

class PydanticDocument(BaseModel):
    text: str
    title: Optional[str] = None

    @classmethod
    def from_llama(cls, doc):
        return cls(
            text=doc.text,
            title=doc.metadata.get("title") if doc.metadata else None,
        )