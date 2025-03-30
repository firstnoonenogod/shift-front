from fastapi import HTTPException
from bson import ObjectId
import configuration

# Get collections
users_collection = configuration.get_collection("users")
products_collection = configuration.get_collection("products")
categories_collection = configuration.get_collection("categories")
variants_collection = configuration.get_collection("product_variants")

def validate_object_id(id_str: str, error_message: str = "Invalid ID format"):
    """Validate if a string is a valid ObjectId"""
    if not ObjectId.is_valid(id_str):
        raise HTTPException(status_code=400, detail=error_message)
    return ObjectId(id_str)

def validate_user(user_id: str):
    """Validate user exists and return user object"""
    obj_id = validate_object_id(user_id, "Invalid user ID format")
    user = users_collection.find_one({"_id": obj_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def validate_product(product_id: str):
    """Validate product exists and return product object"""
    obj_id = validate_object_id(product_id, "Invalid product ID format")
    product = products_collection.find_one({"_id": obj_id})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

def validate_category(category_id: str):
    """Validate category exists and return category object"""
    obj_id = validate_object_id(category_id, "Invalid category ID format")
    category = categories_collection.find_one({"_id": obj_id})
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

def validate_variant(variant_id: str):
    """Validate variant exists and return variant object"""
    obj_id = validate_object_id(variant_id, "Invalid variant ID format")
    variant = variants_collection.find_one({"_id": obj_id})
    if not variant:
        raise HTTPException(status_code=404, detail="Product variant not found")
    return variant
