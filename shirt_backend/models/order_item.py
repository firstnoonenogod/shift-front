from pydantic import BaseModel, Field
from typing import Optional
from models.pyobjectid import PyObjectId

class OrderItem(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    product_id: PyObjectId = Field(..., description="อ้างอิงไปยัง Product")
    variant_id: Optional[PyObjectId] = Field(None, description="อ้างอิงไปยัง ProductVariant ถ้ามี")
    quantity: int
    price: float  # ราคาต่อหน่วยในขณะสั่งซื้อ

    class Config:
        allow_population_by_field_name = True
        json_encoders = {PyObjectId: str}
