from bson import ObjectId

def individual_review_schema(review):
    return {
        "id": str(review["_id"]),
        "product_id": str(review["product_id"]),
        "user_id": str(review["user_id"]),
        "rating": review["rating"],
        "comment": review.get("comment", ""),
        "created_at": review.get("created_at")
    }

def multiple_reviews_schema(reviews):
    return [individual_review_schema(review) for review in reviews]
