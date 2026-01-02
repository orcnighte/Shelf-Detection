"""
FastAPI main application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import images, analytics, recommendations, products

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Inventory Management API",
    description="API for shelf image analysis and product inventory management",
    version="1.0.0"
)

# CORS middleware for Android app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your Android app's domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(images.router, prefix="/api/v1", tags=["images"])
app.include_router(analytics.router, prefix="/api/v1", tags=["analytics"])
app.include_router(recommendations.router, prefix="/api/v1", tags=["recommendations"])
app.include_router(products.router, prefix="/api/v1", tags=["products"])


@app.get("/")
async def root():
    return {"message": "Inventory Management API", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}




