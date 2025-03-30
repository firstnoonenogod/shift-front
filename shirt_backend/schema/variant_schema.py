from bson import ObjectId

def individual_variant_schema(variant):
    return {
        "id": str(variant["_id"]),
        "product_id": str(variant["product_id"]),
        "size": variant["size"],
        "color": variant["color"],
        "price": variant["price"],
        "stock": variant["stock"],
        "created_at": variant["created_at"],
        "updated_at": variant.get("updated_at")
    }

def multiple_variants_schema(variants):
    return [individual_variant_schema(variant) for variant in variants]
