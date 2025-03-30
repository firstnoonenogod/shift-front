from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# Review Schemas
class ReviewBase(BaseModel):
    product_id: str
    rating: int
    comment: Optional[str] = None

class ReviewCreate(ReviewBase):
    pass

class ReviewUpdate(BaseModel):
    rating: Optional[int] = None
    comment: Optional[str] = None

# Variant Schemas
class VariantBase(BaseModel):
    product_id: str = Field(..., description="Product ID")
    size: str = Field(..., description="Variant size")
    color: str = Field(..., description="Variant color")
    price: float = Field(..., ge=0, description="Variant price")
    stock: int = Field(..., ge=0, description="Variant stock")

class VariantCreate(VariantBase):
    pass

class VariantUpdate(BaseModel):
    size: Optional[str] = None
    color: Optional[str] = None
    price: Optional[float] = Field(None, ge=0)
    stock: Optional[int] = Field(None, ge=0)

# Category Schemas
class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

# Order Schemas
class OrderItemCreate(BaseModel):
    product_id: str
    variant_id: Optional[str] = None
    quantity: int

class OrderCreate(BaseModel):
    items: List[OrderItemCreate]
    shipping_address: str
    user_id: Optional[str] = None  # Make user_id optional in the request body

class OrderUpdate(BaseModel):
    status: str
    note: Optional[str] = None

# Payment Schemas
class PaymentBase(BaseModel):
    order_id: str
    amount: float
    payment_method: str
    status: str = "pending"

class PaymentCreate(BaseModel):
    order_id: str
    user_id: Optional[str] = None
    amount: float
    payment_method: str
    status: str = "pending"

class PaymentUpdate(BaseModel):
    status: str
    verified_by: Optional[str] = None
    verified_note: Optional[str] = None
