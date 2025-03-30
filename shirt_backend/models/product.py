from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from models.pyobjectid import PyObjectId

class Product(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    category_id: PyObjectId = Field(..., description="ID ของ Category ที่สินค้านี้สังกัด")
    name: str
    description: str
    price: float
    stock: int
    images: List[str] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        json_encoders = {PyObjectId: str}
