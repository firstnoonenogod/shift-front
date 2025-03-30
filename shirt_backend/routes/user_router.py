from fastapi import APIRouter, HTTPException, status
from typing import List
from datetime import datetime
from bson import ObjectId
import sys
import os

# Add parent directory to path to allow absolute imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import configuration

from schema.user_schema import individual_user_schema, multiple_users_schema
from schema.user_request_schema import UserCreate, UserUpdate, UserResponse

router = APIRouter(prefix="/users", tags=["users"])

# Get collections
users_collection = configuration.get_collection("users")

# User endpoints
@router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate):
    # Check if user already exists
    if users_collection.find_one({"email": user.email}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create user without password hashing
    user_dict = user.dict()
    
    new_user = {
        "email": user_dict["email"],
        "address": user_dict.get("address"),
        "phone": user_dict.get("phone"),
        "role": "customer",  # Default role
        "created_at": datetime.utcnow()
    }
    
    result = users_collection.insert_one(new_user)
    created_user = users_collection.find_one({"_id": result.inserted_id})
    
    return individual_user_schema(created_user)

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )
    
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return individual_user_schema(user)

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: str, user_update: UserUpdate):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )
    
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Remove None values and prepare update data
    update_data = {k: v for k, v in user_update.dict().items() if v is not None}
    
    if not update_data:  # If no valid updates, return current user
        return individual_user_schema(user)
    
    users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})
    updated_user = users_collection.find_one({"_id": ObjectId(user_id)})
    return individual_user_schema(updated_user)

@router.get("/", response_model=List[UserResponse])
async def get_all_users():
    users = users_collection.find()
    return multiple_users_schema(users)

@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: str):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )
    
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    users_collection.delete_one({"_id": ObjectId(user_id)})
    return None
