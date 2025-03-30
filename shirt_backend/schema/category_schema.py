from bson import ObjectId

def individual_category_schema(category):
    return {
        "id": str(category["_id"]),
        "name": category["name"],
        "description": category.get("description", "")
    }

def multiple_categories_schema(categories):
    return [individual_category_schema(category) for category in categories]
