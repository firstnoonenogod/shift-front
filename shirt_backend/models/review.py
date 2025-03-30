from pydantic import BaseModel, Field
from datetime import datetime
from models.pyobjectid import PyObjectId

class Review(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: PyObjectId = Field(..., description="อ้างอิงไปยัง User ที่ให้รีวิว")
    product_id: PyObjectId = Field(..., description="อ้างอิงไปยัง Product ที่รีวิว")
    rating: int = Field(..., ge=1, le=5, description="คะแนนรีวิว ระหว่าง 1 ถึง 5")
    comment: str = Field(None, description="ความคิดเห็นเพิ่มเติม")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        json_encoders = {PyObjectId: str}
