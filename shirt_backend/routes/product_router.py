from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional
from bson import ObjectId
from datetime import datetime
import sys
import os

# Add parent directory to path to allow absolute imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import configuration

from schema.product_schema import individual_product_schema, multiple_products_schema
from schema.product_request_schema import ProductCreate, ProductUpdate, ProductResponse

# Change from product_router to router to match what main.py expects
router = APIRouter(prefix="/products", tags=["products"])

# Get collections
products_collection = configuration.get_collection("products")
categories_collection = configuration.get_collection("categories")
order_items_collection = configuration.get_collection("order_items")
variants_collection = configuration.get_collection("product_variants")

# Helper function to check if category exists
def validate_category(category_id: str):
    if not ObjectId.is_valid(category_id):
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid category ID format. Must be a 24-character hex string (example: 67c030106caf535135048660)"
        )
    
    category = categories_collection.find_one({"_id": ObjectId(category_id)})
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return True

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate):
    # Validate category exists
    validate_category(product.category_id)
    
    product_dict = product.dict()
    product_dict["category_id"] = ObjectId(product.category_id)
    product_dict["created_at"] = datetime.utcnow()
    
    result = products_collection.insert_one(product_dict)
    created_product = products_collection.find_one({"_id": result.inserted_id})
    
    return individual_product_schema(created_product)

@router.get("/", response_model=List[ProductResponse])
async def get_all_products(
    category_id: Optional[str] = None,
    name: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    in_stock: Optional[bool] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100)
):
    # Build query filter
    query = {}
    
    if category_id:
        if not ObjectId.is_valid(category_id):
            raise HTTPException(status_code=400, detail="Invalid category ID format")
        query["category_id"] = ObjectId(category_id)
    
    if name:
        query["name"] = {"$regex": name, "$options": "i"}  # Case-insensitive search
    
    # Price range filter
    price_filter = {}
    if min_price is not None:
        price_filter["$gte"] = min_price
    if max_price is not None:
        price_filter["$lte"] = max_price
    if price_filter:
        query["price"] = price_filter
    
    # Stock filter
    if in_stock is not None:
        if in_stock:
            query["stock"] = {"$gt": 0}
        else:
            query["stock"] = 0
    
    # Execute query with pagination
    products = products_collection.find(query).skip(skip).limit(limit)
    return multiple_products_schema(products)

@router.get("/{product_id}", response_model=ProductResponse)
async def get_product_by_id(product_id: str):
    if not ObjectId.is_valid(product_id):
        raise HTTPException(status_code=400, detail="Invalid product ID format")
    
    product = products_collection.find_one({"_id": ObjectId(product_id)})
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return individual_product_schema(product)

@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(product_id: str, product_update: ProductUpdate):
    if not ObjectId.is_valid(product_id):
        raise HTTPException(status_code=400, detail="Invalid product ID format")
    
    # Check if product exists
    existing_product = products_collection.find_one({"_id": ObjectId(product_id)})
    if not existing_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Remove None values and prepare update data
    update_data = {k: v for k, v in product_update.dict().items() if v is not None}
    
    # Convert category_id to ObjectId if provided
    if "category_id" in update_data:
        validate_category(update_data["category_id"])
        update_data["category_id"] = ObjectId(update_data["category_id"])
    
    if not update_data:
        return individual_product_schema(existing_product)
    
    products_collection.update_one({"_id": ObjectId(product_id)}, {"$set": update_data})
    updated_product = products_collection.find_one({"_id": ObjectId(product_id)})
    
    return individual_product_schema(updated_product)

@router.delete("/{product_id}", status_code=204)
async def delete_product(product_id: str):
    if not ObjectId.is_valid(product_id):
        raise HTTPException(status_code=400, detail="Invalid product ID format")
    
    # Check if product exists
    product = products_collection.find_one({"_id": ObjectId(product_id)})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Check if product is referenced in any orders
    # Use the collection references defined at the top of the file
    order_items = order_items_collection.find_one({"product_id": ObjectId(product_id)})
    if order_items:
        raise HTTPException(status_code=400, detail="Cannot delete product that is referenced in orders")
    
    # Check if product has variants
    # Use the collection references defined at the top of the file
    product_variants = variants_collection.find_one({"product_id": ObjectId(product_id)})
    if product_variants:
        raise HTTPException(status_code=400, detail="Delete product variants first before deleting product")
    
    products_collection.delete_one({"_id": ObjectId(product_id)})
    return None
