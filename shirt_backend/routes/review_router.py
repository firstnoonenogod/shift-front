from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional
from bson import ObjectId
from datetime import datetime
import configuration

from schema.review_schema import individual_review_schema, multiple_reviews_schema
from schema.other_request_schemas import ReviewCreate, ReviewUpdate

router = APIRouter(prefix="/reviews", tags=["reviews"])

# Get collections
reviews_collection = configuration.get_collection("reviews")
users_collection = configuration.get_collection("users")
products_collection = configuration.get_collection("products")

# Helper functions
def validate_user(user_id: str):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID format")
    
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return True

def validate_product(product_id: str):
    if not ObjectId.is_valid(product_id):
        raise HTTPException(status_code=400, detail="Invalid product ID format")
    
    product = products_collection.find_one({"_id": ObjectId(product_id)})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return True

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_review(review: ReviewCreate, user_id: str):
    # Validate user and product
    validate_user(user_id)
    validate_product(review.product_id)
    
    # Check if user already reviewed this product
    existing_review = reviews_collection.find_one({
        "user_id": ObjectId(user_id),
        "product_id": ObjectId(review.product_id)
    })
    
    if existing_review:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already reviewed this product"
        )
    
    # Create review
    review_dict = review.dict()
    review_dict["user_id"] = ObjectId(user_id)
    review_dict["product_id"] = ObjectId(review.product_id)
    review_dict["created_at"] = datetime.utcnow()
    
    result = reviews_collection.insert_one(review_dict)
    created_review = reviews_collection.find_one({"_id": result.inserted_id})
    
    # Update product average rating (you might implement this in a separate function)
    
    return individual_review_schema(created_review)

@router.get("/")
async def get_reviews():
    return {"message": "This endpoint will return reviews"}

@router.get("/all")
async def get_all_reviews(
    product_id: Optional[str] = None,
    user_id: Optional[str] = None,
    min_rating: Optional[int] = Query(None, ge=1, le=5),
    max_rating: Optional[int] = Query(None, ge=1, le=5),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100)
):
    # Build query filter
    query = {}
    
    if product_id:
        if not ObjectId.is_valid(product_id):
            raise HTTPException(status_code=400, detail="Invalid product ID format")
        query["product_id"] = ObjectId(product_id)
    
    if user_id:
        if not ObjectId.is_valid(user_id):
            raise HTTPException(status_code=400, detail="Invalid user ID format")
        query["user_id"] = ObjectId(user_id)
    
    # Rating range filter
    rating_filter = {}
    if min_rating is not None:
        rating_filter["$gte"] = min_rating
    if max_rating is not None:
        rating_filter["$lte"] = max_rating
    if rating_filter:
        query["rating"] = rating_filter
    
    # Execute query with pagination
    reviews = reviews_collection.find(query).skip(skip).limit(limit)
    return multiple_reviews_schema(reviews)

@router.get("/product/{product_id}")
async def get_reviews_by_product(
    product_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100)
):
    if not ObjectId.is_valid(product_id):
        raise HTTPException(status_code=400, detail="Invalid product ID format")
    
    # Validate product exists
    validate_product(product_id)
    
    reviews = reviews_collection.find({"product_id": ObjectId(product_id)}).skip(skip).limit(limit)
    return multiple_reviews_schema(reviews)

@router.get("/{review_id}")
async def get_review_by_id(review_id: str):
    if not ObjectId.is_valid(review_id):
        raise HTTPException(status_code=400, detail="Invalid review ID format")
    
    review = reviews_collection.find_one({"_id": ObjectId(review_id)})
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    return individual_review_schema(review)

@router.put("/{review_id}")
async def update_review(review_id: str, review_update: ReviewUpdate, user_id: str):
    if not ObjectId.is_valid(review_id):
        raise HTTPException(status_code=400, detail="Invalid review ID format")
    
    # Check if review exists
    review = reviews_collection.find_one({"_id": ObjectId(review_id)})
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    # Check if review belongs to user
    if str(review["user_id"]) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own reviews"
        )
    
    # Update only provided fields
    update_data = {k: v for k, v in review_update.dict().items() if v is not None}
    if not update_data:
        return individual_review_schema(review)
    
    reviews_collection.update_one({"_id": ObjectId(review_id)}, {"$set": update_data})
    updated_review = reviews_collection.find_one({"_id": ObjectId(review_id)})
    
    return individual_review_schema(updated_review)

@router.delete("/{review_id}", status_code=204)
async def delete_review(review_id: str, user_id: str):
    if not ObjectId.is_valid(review_id):
        raise HTTPException(status_code=400, detail="Invalid review ID format")
    
    # Check if review exists
    review = reviews_collection.find_one({"_id": ObjectId(review_id)})
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    # Check if review belongs to user
    if str(review["user_id"]) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own reviews"
        )
    
    reviews_collection.delete_one({"_id": ObjectId(review_id)})
    return None
