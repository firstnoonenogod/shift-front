from pydantic import BaseModel, Field
from datetime import datetime
from models.pyobjectid import PyObjectId

class ProductVariant(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    product_id: PyObjectId = Field(..., description="อ้างอิงไปยัง Product หลัก")
    size: str   # เช่น S, M, L, XL
    color: str  # เช่น แดง, น้ำเงิน, เขียว
    stock: int
    price: float
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        json_encoders = {PyObjectId: str}
