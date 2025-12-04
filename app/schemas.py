# app/schemas.py
from pydantic import BaseModel, Field
from typing import Optional

class ItemCreate(BaseModel):
    title: str = Field(..., example="Photoshoot - Outdoor")
    description: Optional[str] = Field(None, example="2-hour outdoor shoot")
    owner: Optional[str] = Field(None, example="sunil@example.com")

class ItemRead(BaseModel):
    id: int
    title: str
    description: Optional[str]
    owner: Optional[str]

    model_config = {"from_attributes": True}
