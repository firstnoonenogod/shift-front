from bson import ObjectId

def individual_product_schema(product):
    return {
        "id": str(product["_id"]),
        "name": product["name"],
        "description": product.get("description", ""),
        "price": product["price"],
        "stock": product["stock"],
        "category_id": str(product["category_id"]),
        "images": product.get("images", []),
        "created_at": product.get("created_at")
    }

def multiple_products_schema(products):
    return [individual_product_schema(product) for product in products]
