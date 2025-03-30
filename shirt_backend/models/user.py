from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from models.pyobjectid import PyObjectId

class User(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    email: EmailStr
    hashed_password: str
    address: str = None
    phone: str = None
    role: str = Field(default="customer", description="customer หรือ admin")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        json_encoders = {PyObjectId: str}
