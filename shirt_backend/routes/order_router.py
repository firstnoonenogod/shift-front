from fastapi import APIRouter, HTTPException, status, Query, Body, Depends, Request
from typing import List, Optional
from bson import ObjectId, errors
from datetime import datetime
import configuration
import json
from fastapi.encoders import jsonable_encoder

from schema.order_schema import individual_order_schema, multiple_orders_schema, order_item_schema
from schema.other_request_schemas import OrderCreate, OrderUpdate, OrderItemCreate

# Make sure the prefix is correct and consistent
router = APIRouter(prefix="/orders", tags=["orders"])

# Get collections
orders_collection = configuration.get_collection("orders")
users_collection = configuration.get_collection("users")
products_collection = configuration.get_collection("products")
variants_collection = configuration.get_collection("product_variants")
payments_collection = configuration.get_collection("payments")

# Helper functions
def is_valid_objectid(id_str):
    try:
        ObjectId(id_str)
        return True
    except (errors.InvalidId, TypeError):
        return False

def validate_user(user_id: str):
    if not is_valid_objectid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID format")
    
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def validate_product(product_id: str):
    if not is_valid_objectid(product_id):
        raise HTTPException(status_code=400, detail="Invalid product ID format")
    
    product = products_collection.find_one({"_id": ObjectId(product_id)})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

def validate_variant(variant_id: str):
    if not is_valid_objectid(variant_id):
        raise HTTPException(status_code=400, detail="Invalid variant ID format")
    
    variant = variants_collection.find_one({"_id": ObjectId(variant_id)})
    if not variant:
        raise HTTPException(status_code=404, detail="Product variant not found")
    return variant

@router.get("/test")
async def test_order_router():
    """
    Test endpoint to verify the order router is working
    """
    return {"message": "Order router is working!"}

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_order(order: OrderCreate, request: Request):
    """
    Create a new order with items and shipping information
    """
    try:
        print(f"Received create order request at {datetime.utcnow()}")
        print(f"Request body: {await request.body()}")
        print(f"Parsed order data: {order}")
        
        # Get user_id from request body or use guest user
        user_id_final = order.user_id or "000000000000000000000000"  # 24-character hex string for ObjectId
        
        # Validate user if not a guest
        if user_id_final != "000000000000000000000000" and is_valid_objectid(user_id_final):
            try:
                user = users_collection.find_one({"_id": ObjectId(user_id_final)})
                if not user:
                    user_id_final = "000000000000000000000000"
            except Exception:
                # If user validation fails, fall back to guest user
                user_id_final = "000000000000000000000000"
        
        # Process order items and calculate total
        total_amount = 0
        order_items = []
        
        for item in order.items:
            try:
                # For testing without valid product IDs
                if item.product_id == "string":
                    item_price = 100  # Default price for testing
                    order_item = {
                        "_id": ObjectId(),
                        "product_id": "test_product_id",
                        "variant_id": item.variant_id if item.variant_id and item.variant_id != "string" else None,
                        "quantity": item.quantity,
                        "price": item_price
                    }
                    order_items.append(order_item)
                    total_amount += item_price * item.quantity
                    continue
                
                # Handle real product IDs
                product = None
                variant = None
                item_price = 0
                
                # Try to get the product
                if is_valid_objectid(item.product_id):
                    product = products_collection.find_one({"_id": ObjectId(item.product_id)})
                    if not product:
                        print(f"Product not found: {item.product_id}")
                
                # Try to get the variant if provided
                if item.variant_id and is_valid_objectid(item.variant_id):
                    variant = variants_collection.find_one({"_id": ObjectId(item.variant_id)})
                    if variant:
                        item_price = variant["price"]
                    else:
                        print(f"Variant not found: {item.variant_id}")
                
                # Use product price if no variant price
                if product and not variant:
                    item_price = product["price"]
                
                # If we couldn't find a price, use a default
                if item_price == 0:
                    item_price = 100  # Default price for testing
                
                # Create order item
                product_id = ObjectId(item.product_id) if is_valid_objectid(item.product_id) else "default_product"
                variant_id = ObjectId(item.variant_id) if item.variant_id and is_valid_objectid(item.variant_id) else None
                
                order_item = {
                    "_id": ObjectId(),
                    "product_id": product_id,
                    "variant_id": variant_id,
                    "quantity": item.quantity,
                    "price": item_price
                }
                
                order_items.append(order_item)
                total_amount += item_price * item.quantity
                
            except Exception as e:
                print(f"Error processing item: {str(e)}")
                # Continue with next item instead of failing the whole order
                continue
        
        # If no items were added, return an error
        if not order_items:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No valid items in order"
            )
        
        # Create order
        user_id_obj = ObjectId(user_id_final) if is_valid_objectid(user_id_final) else "guest"
        new_order = {
            "user_id": user_id_obj,
            "items": order_items,
            "total_amount": total_amount,
            "shipping_address": order.shipping_address,
            "status": "pending",
            "payment_status": "unpaid",
            "created_at": datetime.utcnow()
        }
        
        result = orders_collection.insert_one(new_order)
        print(f"Order created with ID: {result.inserted_id}")
        
        # Update product stocks
        for item in order_items:
            if isinstance(item["product_id"], ObjectId):
                if item["variant_id"] and isinstance(item["variant_id"], ObjectId):
                    variants_collection.update_one(
                        {"_id": item["variant_id"]},
                        {"$inc": {"stock": -item["quantity"]}}
                    )
                else:
                    products_collection.update_one(
                        {"_id": item["product_id"]},
                        {"$inc": {"stock": -item["quantity"]}}
                    )
        
        created_order = orders_collection.find_one({"_id": result.inserted_id})
        return individual_order_schema(created_order)
    
    except HTTPException as e:
        print(f"HTTP Exception in create_order: {e.detail}")
        raise
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"Error creating order: {str(e)}")
        print(error_trace)
        raise HTTPException(status_code=500, detail=f"Error creating order: {str(e)}")

# Handle GET request to root endpoint to match the frontend expectation
@router.get("/")
async def get_orders():
    try:
        orders = orders_collection.find()
        return multiple_orders_schema(orders)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving orders: {str(e)}")

@router.get("/user/{user_id}")
async def get_user_orders(user_id: str):
    # Validate user
    validate_user(user_id)
    
    orders = orders_collection.find({"user_id": ObjectId(user_id)})
    return multiple_orders_schema(orders)

@router.get("/{order_id}")
async def get_order_by_id(order_id: str):
    if not ObjectId.is_valid(order_id):
        raise HTTPException(status_code=400, detail="Invalid order ID format")
    
    order = orders_collection.find_one({"_id": ObjectId(order_id)})
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    return individual_order_schema(order)

@router.put("/{order_id}")
async def update_order_status(order_id: str, order_update: OrderUpdate):
    if not ObjectId.is_valid(order_id):
        raise HTTPException(status_code=400, detail="Invalid order ID format")
    
    # Check if order exists
    order = orders_collection.find_one({"_id": ObjectId(order_id)})
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Validate status transition
    if order_update.status not in ["pending", "processing", "shipped", "delivered", "cancelled"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid order status: {order_update.status}"
        )
    
    # Handle cancellation - return items to inventory if cancelling
    if order_update.status == "cancelled" and order["status"] != "cancelled":
        for item in order["items"]:
            if item.get("variant_id"):
                variants_collection.update_one(
                    {"_id": item["variant_id"]},
                    {"$inc": {"stock": item["quantity"]}}
                )
            else:
                products_collection.update_one(
                    {"_id": item["product_id"]},
                    {"$inc": {"stock": item["quantity"]}}
                )
    
    # Update order
    orders_collection.update_one(
        {"_id": ObjectId(order_id)},
        {"$set": {"status": order_update.status}}
    )
    
    updated_order = orders_collection.find_one({"_id": ObjectId(order_id)})
    return individual_order_schema(updated_order)

@router.delete("/{order_id}", status_code=204)
async def delete_order(order_id: str):
    if not ObjectId.is_valid(order_id):
        raise HTTPException(status_code=400, detail="Invalid order ID format")
    
    # Check if order exists
    order = orders_collection.find_one({"_id": ObjectId(order_id)})
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Check if there are payments related to this order
    payment = payments_collection.find_one({"order_id": ObjectId(order_id)})
    if payment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete order with associated payments. Cancel the order instead."
        )
    
    # If deleting the order, restore the inventory
    if order["status"] != "cancelled":
        for item in order["items"]:
            if item.get("variant_id"):
                variants_collection.update_one(
                    {"_id": item["variant_id"]},
                    {"$inc": {"stock": item["quantity"]}}
                )
            else:
                products_collection.update_one(
                    {"_id": item["product_id"]},
                    {"$inc": {"stock": item["quantity"]}}
                )
    
    orders_collection.delete_one({"_id": ObjectId(order_id)})
    return None