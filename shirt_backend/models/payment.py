from pydantic import BaseModel, Field
from datetime import datetime
from models.pyobjectid import PyObjectId

class Payment(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    order_id: PyObjectId = Field(..., description="อ้างอิงไปยัง Order")
    user_id: PyObjectId = Field(..., description="อ้างอิงไปยัง User")
    amount: float = Field(..., description="จำนวนเงินที่ชำระ")
    payment_method: str = Field(..., description="วิธีการชำระเงิน เช่น credit_card, paypal, bank_transfer")
    status: str = Field(default="pending", description="สถานะการชำระเงิน: pending, completed, failed")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        json_encoders = {PyObjectId: str}
