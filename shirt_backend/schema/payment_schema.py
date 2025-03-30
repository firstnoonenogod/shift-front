from bson import ObjectId

def individual_payment_schema(payment):
    return {
        "id": str(payment["_id"]),
        "order_id": str(payment["order_id"]),
        "user_id": str(payment["user_id"]),
        "amount": payment["amount"],
        "payment_method": payment["payment_method"],
        "status": payment["status"],
        "created_at": payment["created_at"]
    }

def multiple_payments_schema(payments):
    return [individual_payment_schema(payment) for payment in payments]
