"""
Mercil Backend - Main Application
FastAPI server for AI-powered disaster relief search
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
from dotenv import load_dotenv

# Import routers
from api.search import router as search_router
from api.images import router as images_router

# Load environment variables
load_dotenv()

# Initialize FastAPI
app = FastAPI(
    title="Mercil Backend API",
    description="AI-powered search system for disaster relief locations",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ใน production ควรระบุ domain ที่แน่นอน
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (for serving images)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Include routers
app.include_router(search_router)
app.include_router(images_router)


@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "name": "Mercil Backend API",
        "version": "2.0.0",
        "status": "running",
        "features": [
            "Intelligent semantic search",
            "Location-based search",
            "Image upload & tagging",
            "Image similarity search",
            "Multi-language support (Thai/English)"
        ],
        "endpoints": {
            "docs": "/docs",
            "search": "/api/search",
            "images": "/api/images"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "database": "connected",  # TODO: Add actual DB check
        "ai_models": "loaded"
    }


@app.get("/api/stats")
async def get_stats():
    """
    ดูสถิติของระบบ
    """
    import psycopg2
    from psycopg2.extras import RealDictCursor
    
    try:
        conn = psycopg2.connect(os.getenv('DATABASE_URL'))
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        # Total assets
        cur.execute("SELECT COUNT(*) as total FROM assets")
        total_assets = cur.fetchone()['total']
        
        # Assets by type
        cur.execute("""
            SELECT location_type, COUNT(*) as count
            FROM assets
            GROUP BY location_type
            ORDER BY count DESC
        """)
        by_type = cur.fetchall()
        
        # Assets with images
        cur.execute("""
            SELECT COUNT(*) as total
            FROM assets
            WHERE images IS NOT NULL AND jsonb_array_length(images) > 0
        """)
        with_images = cur.fetchone()['total']
        
        # Total tags
        cur.execute("""
            SELECT COUNT(DISTINCT unnest(tags)) as total
            FROM assets
            WHERE tags IS NOT NULL
        """)
        total_tags = cur.fetchone()['total']
        
        cur.close()
        conn.close()
        
        return {
            "total_assets": total_assets,
            "assets_by_type": [dict(row) for row in by_type],
            "assets_with_images": with_images,
            "total_unique_tags": total_tags
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return {
        "error": "Not Found",
        "message": "The requested resource was not found",
        "path": str(request.url)
    }


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return {
        "error": "Internal Server Error",
        "message": "An unexpected error occurred",
        "detail": str(exc)
    }


if __name__ == "__main__":
    # Run server
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload on code changes
        log_level="info"
    )
