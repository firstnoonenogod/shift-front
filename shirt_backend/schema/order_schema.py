from bson import ObjectId

def order_item_schema(item):
    return {
        "id": str(item["_id"]),
        "product_id": str(item["product_id"]),
        "variant_id": str(item["variant_id"]) if item.get("variant_id") else None,
        "quantity": item["quantity"],
        "price": item["price"]
    }

def individual_order_schema(order):
    return {
        "id": str(order["_id"]),
        "user_id": str(order["user_id"]),
        "items": [order_item_schema(item) for item in order["items"]],
        "total_amount": order["total_amount"],
        "shipping_address": order["shipping_address"],
        "status": order["status"],
        "created_at": order["created_at"]
    }

def multiple_orders_schema(orders):
    return [individual_order_schema(order) for order in orders]
