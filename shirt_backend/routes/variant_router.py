from fastapi import APIRouter, HTTPException, status, Query, Body, Depends
from typing import List, Optional
from bson import ObjectId, errors
from datetime import datetime
import configuration
from fastapi.encoders import jsonable_encoder

from schema.variant_schema import individual_variant_schema, multiple_variants_schema
from schema.other_request_schemas import VariantCreate, VariantUpdate

router = APIRouter(prefix="/variants", tags=["variants"])

# Get collections
variants_collection = configuration.get_collection("product_variants")
products_collection = configuration.get_collection("products")

# Helper functions
def is_valid_objectid(id_str):
    try:
        ObjectId(id_str)
        return True
    except (errors.InvalidId, TypeError):
        return False

# Helper function to validate product_id
def validate_product_id(product_id: str):
    if not is_valid_objectid(product_id):
        raise HTTPException(status_code=400, detail=f"Invalid product ID format: {product_id}")
    
    product = products_collection.find_one({"_id": ObjectId(product_id)})
    if not product:
        raise HTTPException(status_code=404, detail=f"Product not found with ID: {product_id}")
    
    return product

# Get all variants (GET /variants/)
@router.get("/", response_model_exclude_none=True)
async def get_all_variants(skip: int = 0, limit: int = 100):
    """
    Retrieve all product variants with pagination
    """
    try:
        variants = variants_collection.find().skip(skip).limit(limit)
        return multiple_variants_schema(variants)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving variants: {str(e)}")

# Get all variants for a specific product (GET /variants/product/{product_id})
@router.get("/product/{product_id}", response_model_exclude_none=True)
async def get_product_variants(product_id: str):
    """
    Retrieve all variants for a specific product
    """
    try:
        # Validate product_id format
        if not is_valid_objectid(product_id):
            raise HTTPException(status_code=400, detail=f"Invalid product ID format: {product_id}")
        
        # Find all variants for the product
        variants = variants_collection.find({"product_id": ObjectId(product_id)})
        return multiple_variants_schema(variants)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving variants: {str(e)}")

# Get a specific variant by ID (GET /variants/{variant_id})
@router.get("/{variant_id}", response_model_exclude_none=True)
async def get_variant(variant_id: str):
    """
    Retrieve a specific variant by ID
    """
    if not is_valid_objectid(variant_id):
        raise HTTPException(status_code=400, detail=f"Invalid variant ID format: {variant_id}")
    
    variant = variants_collection.find_one({"_id": ObjectId(variant_id)})
    if not variant:
        raise HTTPException(status_code=404, detail=f"Variant not found with ID: {variant_id}")
    
    return individual_variant_schema(variant)

# Create a new variant (POST /variants/)
@router.post("/", status_code=status.HTTP_201_CREATED, response_model_exclude_none=True)
async def create_variant(variant: VariantCreate):
    """
    Create a new product variant
    """
    try:
        print(f"Received variant data: {variant}")
        
        # Validate product_id format and existence
        product = validate_product_id(variant.product_id)
        
        # Create variant document
        new_variant = {
            "product_id": ObjectId(variant.product_id),
            "size": variant.size,
            "color": variant.color,
            "price": float(variant.price),
            "stock": int(variant.stock),
            "created_at": datetime.utcnow()
        }
        
        result = variants_collection.insert_one(new_variant)
        created_variant = variants_collection.find_one({"_id": result.inserted_id})
        
        # Recalculate product stock based on variants
        update_product_stock_from_variants(variant.product_id)
        
        return individual_variant_schema(created_variant)
    except HTTPException as e:
        raise e
    except ValueError as e:
        raise HTTPException(status_code=422, detail=f"Invalid data format: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating variant: {str(e)}")

# Update a variant (PUT /variants/{variant_id})
@router.put("/{variant_id}", response_model_exclude_none=True)
async def update_variant(variant_id: str, variant: VariantUpdate):
    """
    Update an existing product variant
    """
    try:
        # Validate variant_id format
        if not is_valid_objectid(variant_id):
            raise HTTPException(status_code=400, detail=f"Invalid variant ID format: {variant_id}")
        
        # Check if variant exists
        existing_variant = variants_collection.find_one({"_id": ObjectId(variant_id)})
        if not existing_variant:
            raise HTTPException(status_code=404, detail=f"Variant not found with ID: {variant_id}")
        
        # Prepare update data with only provided fields
        update_data = {}
        variant_dict = variant.dict(exclude_unset=True)
        
        for field, value in variant_dict.items():
            if value is not None:
                update_data[field] = value
        
        update_data["updated_at"] = datetime.utcnow()
        
        # Update variant
        variants_collection.update_one(
            {"_id": ObjectId(variant_id)},
            {"$set": update_data}
        )
        
        updated_variant = variants_collection.find_one({"_id": ObjectId(variant_id)})
        
        # Get product_id to update product stock
        product_id = str(updated_variant["product_id"])
        update_product_stock_from_variants(product_id)
        
        return individual_variant_schema(updated_variant)
    except HTTPException as e:
        raise e
    except ValueError as e:
        raise HTTPException(status_code=422, detail=f"Invalid data format: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating variant: {str(e)}")

# Delete a variant (DELETE /variants/{variant_id})
@router.delete("/{variant_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_variant(variant_id: str):
    """
    Delete a product variant
    """
    try:
        # Validate variant_id format
        if not is_valid_objectid(variant_id):
            raise HTTPException(status_code=400, detail=f"Invalid variant ID format: {variant_id}")
        
        # Check if variant exists
        existing_variant = variants_collection.find_one({"_id": ObjectId(variant_id)})
        if not existing_variant:
            raise HTTPException(status_code=404, detail=f"Variant not found with ID: {variant_id}")
        
        # Get product_id to update product stock after deletion
        product_id = str(existing_variant["product_id"])
        
        # Delete the variant
        result = variants_collection.delete_one({"_id": ObjectId(variant_id)})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=500, detail="Failed to delete variant")
            
        # Update the product stock
        update_product_stock_from_variants(product_id)
        
        return None
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting variant: {str(e)}")

# Helper function to update product stock based on variants
def update_product_stock_from_variants(product_id: str):
    """
    Calculate the total stock from all variants and update the product's stock
    """
    try:
        if not is_valid_objectid(product_id):
            return
        
        # Get all variants for the product
        variants = variants_collection.find({"product_id": ObjectId(product_id)})
        
        # Calculate total stock
        total_stock = sum(variant.get("stock", 0) for variant in variants)
        
        # Update product
        products_collection.update_one(
            {"_id": ObjectId(product_id)},
            {"$set": {"stock": total_stock}}
        )
        
        print(f"Product {product_id} stock recalculated: {total_stock}")
    except Exception as e:
        print(f"Error updating product stock: {str(e)}")
