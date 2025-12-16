"""
Marketing IQ - FastAPI Application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Create FastAPI app
app = FastAPI(
    title="Marketing IQ API",
    version="1.0.0",
    description="Multi-tenant marketing analytics API",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Marketing IQ API", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


# TODO: Include routers
# from app.api import auth, tenants, dashboards, metrics
# app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
# app.include_router(tenants.router, prefix="/tenants", tags=["Tenants"])
# app.include_router(dashboards.router, prefix="/api/v1", tags=["Dashboards"])
# app.include_router(metrics.router, prefix="/api/v1", tags=["Metrics"])
