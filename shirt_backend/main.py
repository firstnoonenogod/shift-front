from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from datetime import datetime

# Import routers explicitly to ensure they're loaded correctly
from routes.user_router import router as user_router
from routes.product_router import router as product_router
from routes.category_router import router as category_router
from routes.variant_router import router as variant_router
from routes.review_router import router as review_router
from routes.order_router import router as order_router
from routes.payment_router import router as payment_router

app = FastAPI(
    title="Shirt Shop API",
    description="API for t-shirt e-commerce application",
    version="1.0.0"
)

# Configure CORS
origins = [
    "http://localhost",
    "http://localhost:3000",  # For React/Nuxt frontend
    "http://localhost:8000",
    "*"  # Allow all origins in development
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
async def root():
    return {
        'message': 'Shirt Shop API',
        'documentation': '/docs',
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

# Include all routers explicitly
app.include_router(user_router)
app.include_router(product_router)
app.include_router(category_router)
app.include_router(variant_router)
app.include_router(review_router)
app.include_router(order_router)  # Make sure the order router is included
app.include_router(payment_router)

# Add a debugging endpoint to list all registered routes
@app.get("/routes", include_in_schema=False)
async def list_routes():
    routes = []
    for route in app.routes:
        routes.append({
            "path": route.path,
            "name": route.name,
            "methods": route.methods
        })
    return routes

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
