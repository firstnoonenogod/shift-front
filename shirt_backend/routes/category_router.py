from fastapi import APIRouter, HTTPException, status
from typing import List
from bson import ObjectId
import configuration

from schema.category_schema import individual_category_schema, multiple_categories_schema
from schema.other_request_schemas import CategoryCreate, CategoryUpdate

router = APIRouter(prefix="/categories", tags=["categories"])

# Get collections
categories_collection = configuration.get_collection("categories")
products_collection = configuration.get_collection("products")

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_category(category: CategoryCreate):
    # Check if category name already exists (case-insensitive)
    existing = categories_collection.find_one({"name": {"$regex": f"^{category.name}$", "$options": "i"}})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category with this name already exists"
        )
    
    category_dict = category.dict()
    result = categories_collection.insert_one(category_dict)
    created_category = categories_collection.find_one({"_id": result.inserted_id})
    
    return individual_category_schema(created_category)

@router.get("/")
async def get_categories():
    # Replace message with actual categories retrieval
    categories = categories_collection.find()
    return multiple_categories_schema(categories)

@router.get("/{category_id}")
async def get_category_by_id(category_id: str):
    if not ObjectId.is_valid(category_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid category ID format"
        )
    
    category = categories_collection.find_one({"_id": ObjectId(category_id)})
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    return individual_category_schema(category)

@router.put("/{category_id}")
async def update_category(category_id: str, category_update: CategoryUpdate):
    if not ObjectId.is_valid(category_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid category ID format"
        )
    
    # Check if category exists
    category = categories_collection.find_one({"_id": ObjectId(category_id)})
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    # Update only provided fields
    update_data = {k: v for k, v in category_update.dict().items() if v is not None}
    if not update_data:
        return individual_category_schema(category)
    
    # If name is being updated, check for duplicates
    if "name" in update_data:
        existing = categories_collection.find_one({
            "name": {"$regex": f"^{update_data['name']}$", "$options": "i"},
            "_id": {"$ne": ObjectId(category_id)}
        })
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category with this name already exists"
            )
    
    categories_collection.update_one({"_id": ObjectId(category_id)}, {"$set": update_data})
    updated_category = categories_collection.find_one({"_id": ObjectId(category_id)})
    
    return individual_category_schema(updated_category)

@router.delete("/{category_id}", status_code=204)
async def delete_category(category_id: str, force: bool = False):
    if not ObjectId.is_valid(category_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid category ID format"
        )
    
    # Check if category exists
    category = categories_collection.find_one({"_id": ObjectId(category_id)})
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    
    # Check if any products are using this category
    products_count = products_collection.count_documents({"category_id": ObjectId(category_id)})
    if products_count > 0:
        if not force:
            # Return product IDs that are using this category
            products = products_collection.find({"category_id": ObjectId(category_id)})
            product_ids = [str(product["_id"]) for product in products]
            
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "message": f"Cannot delete category: {products_count} products are assigned to this category",
                    "product_count": products_count,
                    "product_ids": product_ids,
                    "help": "Either reassign these products to another category or use force=true parameter"
                }
            )
        # If force=true, reassign products to a default "uncategorized" category
        # or create one if it doesn't exist
        uncategorized = categories_collection.find_one({"name": "Uncategorized"})
        if not uncategorized:
            result = categories_collection.insert_one({
                "name": "Uncategorized", 
                "description": "Default category for products with no category"
            })
            uncategorized_id = result.inserted_id
        else:
            uncategorized_id = uncategorized["_id"]
        
        # Update all products to use the uncategorized category
        products_collection.update_many(
            {"category_id": ObjectId(category_id)},
            {"$set": {"category_id": uncategorized_id}}
        )
    
    # Now we can safely delete the category
    categories_collection.delete_one({"_id": ObjectId(category_id)})
    return None
