from pydantic import BaseModel, Field
from models.pyobjectid import PyObjectId

class Category(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    description: str = None

    class Config:
        allow_population_by_field_name = True
        json_encoders = {PyObjectId: str}
