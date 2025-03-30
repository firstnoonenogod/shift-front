from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from models.pyobjectid import PyObjectId
from models.order_item import OrderItem

class Order(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: PyObjectId = Field(..., description="อ้างอิงไปยัง User ที่สั่งซื้อ")
    items: List[OrderItem] = Field(..., description="รายการสินค้าที่สั่งซื้อ")
    total_amount: float = Field(..., description="ยอดรวมของออร์เดอร์")
    shipping_address: str = Field(..., description="ที่อยู่สำหรับจัดส่งสินค้า")
    status: str = Field(default="pending", description="สถานะออร์เดอร์: pending, shipped, delivered")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        json_encoders = {PyObjectId: str}
