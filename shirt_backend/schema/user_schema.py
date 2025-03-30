from bson import ObjectId

def individual_user_schema(user):
    return {
        "id": str(user["_id"]),
        "email": user["email"],
        "username": user.get("username", ""),
        "full_name": user.get("full_name", ""),
        "is_active": user.get("is_active", True),
        "created_at": user.get("created_at"),
        "updated_at": user.get("updated_at")
    }

def multiple_users_schema(users):
    return [individual_user_schema(user) for user in users]
