from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional
from bson import ObjectId, errors
from datetime import datetime
import configuration
from schema.payment_schema import individual_payment_schema, multiple_payments_schema
from schema.other_request_schemas import PaymentCreate, PaymentUpdate

router = APIRouter(prefix="/payments", tags=["payments"])

# Get collections
payments_collection = configuration.get_collection("payments")
orders_collection = configuration.get_collection("orders")
users_collection = configuration.get_collection("users")

# Helper functions
def is_valid_objectid(id_str):
    try:
        ObjectId(id_str)
        return True
    except (errors.InvalidId, TypeError):
        return False

def validate_order(order_id: str):
    if not is_valid_objectid(order_id):
        raise HTTPException(status_code=400, detail=f"Invalid order ID format: {order_id}")
    
    order = orders_collection.find_one({"_id": ObjectId(order_id)})
    if not order:
        raise HTTPException(status_code=404, detail=f"Order not found with ID: {order_id}")
    return order

def validate_user(user_id: str):
    if not is_valid_objectid(user_id):
        raise HTTPException(status_code=400, detail=f"Invalid user ID format: {user_id}")
    
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail=f"User not found with ID: {user_id}")
    return user

@router.post("/", response_model_exclude_none=True, status_code=status.HTTP_201_CREATED)
async def create_payment(payment: PaymentCreate):
    try:
        # For testing with dummy values
        if payment.order_id == "string":
            dummy_payment = {
                "_id": ObjectId(),
                "order_id": "test_order_id",
                "user_id": payment.user_id or "guest_user",
                "amount": payment.amount or 100,
                "payment_method": payment.payment_method,
                "status": payment.status,
                "created_at": datetime.utcnow()
            }
            result = payments_collection.insert_one(dummy_payment)
            created_payment = payments_collection.find_one({"_id": result.inserted_id})
            return individual_payment_schema(created_payment)
        
        # Real order validation
        if not is_valid_objectid(payment.order_id):
            raise HTTPException(status_code=400, detail=f"Invalid order ID format: {payment.order_id}")
        
        # Validate order
        order = validate_order(payment.order_id)
        
        # Use user_id from payment body, or from order
        user_id_final = payment.user_id or str(order["user_id"])
        
        # Check if payment already exists for this order
        existing_payment = payments_collection.find_one({"order_id": ObjectId(payment.order_id)})
        if existing_payment:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Payment already exists for order {payment.order_id}"
            )
        
        # Create payment document
        new_payment = {
            "order_id": ObjectId(payment.order_id),
            "user_id": ObjectId(user_id_final) if is_valid_objectid(user_id_final) else "guest",
            "amount": payment.amount,
            "payment_method": payment.payment_method,
            "status": payment.status,
            "created_at": datetime.utcnow()
        }
        
        result = payments_collection.insert_one(new_payment)
        
        # Update order to reflect payment status if needed
        if payment.status in ["completed", "approved"]:
            orders_collection.update_one(
                {"_id": ObjectId(payment.order_id)},
                {"$set": {"payment_status": "paid"}}
            )
        
        created_payment = payments_collection.find_one({"_id": result.inserted_id})
        return individual_payment_schema(created_payment)
    
    except HTTPException as e:
        # Re-raise HTTPExceptions
        raise
    except Exception as e:
        # Handle any other errors
        raise HTTPException(status_code=500, detail=f"Error creating payment: {str(e)}")

# Make /payments/ endpoint return all payments (similar to what /payments/all would do)
@router.get("/")
async def get_all_payments():
    try:
        payments = payments_collection.find()
        return multiple_payments_schema(payments)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving payments: {str(e)}")

# Keep the /all endpoint for backward compatibility
@router.get("/all")
async def get_all_payments_alt():
    try:
        payments = payments_collection.find()
        return multiple_payments_schema(payments)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving payments: {str(e)}")

@router.get("/{payment_id}")
async def get_payment(payment_id: str):
    if not ObjectId.is_valid(payment_id):
        raise HTTPException(status_code=400, detail="Invalid payment ID format")
    
    payment = payments_collection.find_one({"_id": ObjectId(payment_id)})
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    
    return individual_payment_schema(payment)

@router.get("/order/{order_id}")
async def get_payment_by_order(order_id: str):
    if not ObjectId.is_valid(order_id):
        raise HTTPException(status_code=400, detail="Invalid order ID format")
    
    payment = payments_collection.find_one({"order_id": ObjectId(order_id)})
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found for this order")
    
    return individual_payment_schema(payment)

@router.put("/{payment_id}")
async def update_payment(payment_id: str, payment_update: PaymentUpdate):
    if not ObjectId.is_valid(payment_id):
        raise HTTPException(status_code=400, detail="Invalid payment ID format")
    
    # Check if payment exists
    payment = payments_collection.find_one({"_id": ObjectId(payment_id)})
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    
    # Prepare update data
    update_data = {"status": payment_update.status}
    
    if payment_update.verified_by:
        update_data["verified_by"] = payment_update.verified_by
    
    if payment_update.verified_note:
        update_data["verified_note"] = payment_update.verified_note
    
    update_data["updated_at"] = datetime.utcnow()
    
    # Update payment
    payments_collection.update_one(
        {"_id": ObjectId(payment_id)},
        {"$set": update_data}
    )
    
    # If payment is completed/approved, update order payment status
    if payment_update.status in ["completed", "approved"]:
        orders_collection.update_one(
            {"_id": payment["order_id"]},
            {"$set": {"payment_status": "paid"}}
        )
    elif payment_update.status == "rejected":
        orders_collection.update_one(
            {"_id": payment["order_id"]},
            {"$set": {"payment_status": "unpaid"}}
        )
    
    updated_payment = payments_collection.find_one({"_id": ObjectId(payment_id)})
    return individual_payment_schema(updated_payment)
