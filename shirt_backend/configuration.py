import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

# Get MongoDB URI from environment variables
uri = os.getenv("uri")

# Create a MongoDB client
client = MongoClient(uri)

# Get the database
db = client.shirt_shop_db

# Define collections
collections = {
    "users": db["users"],
    "products": db["products"],
    "categories": db["categories"],
    "product_variants": db["product_variants"],
    "reviews": db["reviews"],
    "orders": db["orders"],
    "order_items": db["order_items"],  # Add this if it doesn't exist
    "payments": db["payments"]
}

# Application settings
SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key_here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# Access collections
def get_collection(name):
    if name not in collections:
        raise ValueError(f"Collection {name} does not exist")
    return collections[name]
