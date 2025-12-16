# Marketing IQ Backend API Implementation Guide

## Overview

This guide defines the standard architecture and patterns for implementing backend APIs in the Marketing IQ application. All new APIs must follow this **feature-based (vertical slice) architecture** to ensure consistency, maintainability, and testability.

---

## Running the Server

From the `backend/` directory, start the development server with:

1. Activate the virtual environment
```bash
./venv/Scripts/activate
```
2. Run the app
```bash
py -m uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000` with auto-reload enabled for development.

- **API Docs**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        FastAPI Application                       │
│                         (app/main.py)                           │
└─────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FEATURE MODULES                             │
│                   app/features/{platform}/                       │
│                                                                 │
│  - Each platform (google_ads, meta, etc.) is a feature module   │
│  - Contains sub-features as vertical slices                     │
│  - Exports combined router via __init__.py                      │
└─────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                    SUB-FEATURE (Vertical Slice)                  │
│              app/features/{platform}/{feature}/                  │
│                                                                 │
│  ┌─────────────┐   ┌─────────────┐   ┌──────────────┐          │
│  │  router.py  │ → │ service.py  │ → │ repository.py │          │
│  │ (Endpoints) │   │  (Logic)    │   │    (SQL)      │          │
│  └─────────────┘   └─────────────┘   └──────────────┘          │
│         │                                                       │
│         └──────────────── models.py (DTOs) ─────────────────────┤
└─────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                        DATABASE LAYER                            │
│                   app/core/database.py                          │
│                                                                 │
│  - execute_query(query, params) - Primary interface             │
│  - Snowflake connection management                              │
│  - Parameterized queries for SQL injection prevention           │
└─────────────────────────────────────────────────────────────────┘
```

---

## Folder Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                         # FastAPI app entry point
│   │
│   ├── core/                           # Core utilities
│   │   ├── __init__.py
│   │   ├── config.py                   # Settings management
│   │   ├── database.py                 # Database connection & execute_query()
│   │   └── exceptions.py               # Custom exceptions
│   │
│   └── features/                       # Feature modules
│       ├── __init__.py
│       │
│       └── google_ads/                 # Platform: Google Ads
│           ├── __init__.py             # Combines all sub-feature routers
│           │
│           ├── overview/               # Sub-feature: Overview
│           │   ├── __init__.py
│           │   ├── router.py           # API endpoints
│           │   ├── service.py          # Business logic
│           │   ├── repository.py       # SQL queries
│           │   └── models.py           # Pydantic DTOs
│           │
│           ├── campaigns/              # Sub-feature: Campaigns
│           │   ├── __init__.py
│           │   ├── router.py
│           │   ├── service.py
│           │   ├── repository.py
│           │   └── models.py
│           │
│           └── keywords/               # Sub-feature: Keywords
│               ├── __init__.py
│               ├── router.py
│               ├── service.py
│               ├── repository.py
│               └── models.py
│
└── tests/
    ├── __init__.py
    ├── conftest.py
    └── features/
        └── google_ads/
            ├── overview/
            ├── campaigns/
            └── keywords/
```

---

## Layer Implementation Templates

### 1. Models Layer (`{feature}/models.py`)

Models define request/response schemas using Pydantic.

**File: `app/features/google_ads/overview/models.py`**

```python
"""
Google Ads Overview - Pydantic models (DTOs).
"""
from typing import Optional
from pydantic import BaseModel, Field


class GoogleAdsOverviewResponse(BaseModel):
    """Response model for Google Ads overview metrics."""
    total_spend: float = Field(..., description="Total advertising spend")
    total_conversions: float = Field(..., description="Total number of conversions")
    total_revenue: float = Field(..., description="Total conversion value/revenue")
    roas: float = Field(..., description="Return on Ad Spend (Revenue/Spend)")
    ctr: float = Field(..., description="Click-Through Rate percentage")
    cpc: float = Field(..., description="Cost Per Click")
    avg_quality_score: Optional[float] = Field(None, description="Average Quality Score across keywords")

    class Config:
        from_attributes = True
```

**Common Model Patterns:**

```python
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


# Base model with shared fields
class CampaignBase(BaseModel):
    """Base campaign fields shared across models."""
    name: str = Field(..., min_length=1, max_length=255, description="Campaign name")
    platform: str = Field(..., description="Platform code")
    status: str = Field(default="active", description="Campaign status")


# Request model for creation
class CampaignCreate(CampaignBase):
    """Request model for creating a campaign."""
    budget: Optional[float] = Field(None, ge=0, description="Campaign budget")


# Request model for updates (all fields optional)
class CampaignUpdate(BaseModel):
    """Request model for updating a campaign."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    status: Optional[str] = None
    budget: Optional[float] = Field(None, ge=0)


# Response model
class CampaignResponse(CampaignBase):
    """Response model for a single campaign."""
    id: int
    budget: Optional[float] = None
    impressions: int = 0
    clicks: int = 0
    spend: float = 0.0
    created_at: datetime

    class Config:
        from_attributes = True


# Paginated list response
class CampaignListResponse(BaseModel):
    """Response model for paginated campaign list."""
    items: list[CampaignResponse]
    total: int
    page: int
    page_size: int
    has_next: bool
```

---

### 2. Repository Layer (`{feature}/repository.py`)

Repositories handle all data access using `execute_query()`.

**File: `app/features/google_ads/overview/repository.py`**

```python
"""
Google Ads Overview repository - Data access layer for overview metrics.
"""
from datetime import date
from typing import Optional
from app.core.database import execute_query


class GoogleAdsOverviewRepository:
    """Repository for Google Ads overview data access operations."""

    @staticmethod
    def get_overview_metrics(
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> Optional[dict]:
        """
        Fetch aggregated Google Ads overview metrics, optionally filtered by date range.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            Dictionary with aggregated metrics or None if no data
        """
        # Build date filter conditions
        date_conditions = []
        params = {}

        if date_from:
            date_conditions.append("f.DATE_DAY >= %(date_from)s")
            params["date_from"] = date_from.isoformat()

        if date_to:
            date_conditions.append("f.DATE_DAY <= %(date_to)s")
            params["date_to"] = date_to.isoformat()

        # Build the date filter clause
        date_filter = ""
        if date_conditions:
            date_filter = "AND " + " AND ".join(date_conditions)

        query = f"""
            SELECT
                perf.TOTAL_SPEND,
                perf.TOTAL_CONVERSIONS,
                perf.TOTAL_REVENUE,
                perf.ROAS,
                perf.CTR,
                perf.CPC,
                qs.AVG_QUALITY_SCORE
            FROM (
                SELECT
                    SUM(f.SPEND) AS TOTAL_SPEND,
                    SUM(f.CONVERSIONS) AS TOTAL_CONVERSIONS,
                    SUM(f.CONVERSION_VALUE) AS TOTAL_REVENUE,
                    CASE WHEN SUM(f.SPEND) > 0 THEN SUM(f.CONVERSION_VALUE) / SUM(f.SPEND) ELSE 0 END AS ROAS,
                    CASE WHEN SUM(f.IMPRESSIONS) > 0 THEN (SUM(f.CLICKS) / SUM(f.IMPRESSIONS)) * 100 ELSE 0 END AS CTR,
                    CASE WHEN SUM(f.CLICKS) > 0 THEN SUM(f.SPEND) / SUM(f.CLICKS) ELSE 0 END AS CPC
                FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_CAMPAIGN_PERFORMANCE f
                JOIN CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.DIM_PLATFORM p ON f.PLATFORM = p.PLATFORM_CODE
                WHERE p.PLATFORM_CODE = 'google_ads'
                    {date_filter}
            ) perf
            CROSS JOIN (
                SELECT AVG(k.QUALITY_SCORE) AS AVG_QUALITY_SCORE
                FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.DIM_KEYWORD k
                JOIN CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.DIM_PLATFORM p ON k.PLATFORM = p.PLATFORM_CODE
                WHERE p.PLATFORM_CODE = 'google_ads'
                    AND k.QUALITY_SCORE IS NOT NULL
                    AND k.IS_CURRENT = TRUE
            ) qs
        """

        results = execute_query(query, params if params else None)
        return results[0] if results else None


# Singleton instance for dependency injection
google_ads_overview_repository = GoogleAdsOverviewRepository()
```

**Repository Patterns:**

```python
# Pagination pattern
@staticmethod
def get_all(
    page: int = 1,
    page_size: int = 20,
    platform: Optional[str] = None
) -> tuple[list[dict], int]:
    """Fetch paginated results with total count."""
    conditions = ["1=1"]
    params = {}

    if platform:
        conditions.append("platform = %(platform)s")
        params["platform"] = platform

    where_clause = " AND ".join(conditions)
    offset = (page - 1) * page_size

    # Count query
    count_query = f"""
        SELECT COUNT(*) as TOTAL
        FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.TABLE_NAME
        WHERE {where_clause}
    """
    count_result = execute_query(count_query, params)
    total = count_result[0]["TOTAL"] if count_result else 0

    # Data query
    data_query = f"""
        SELECT id, name, platform, status
        FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.TABLE_NAME
        WHERE {where_clause}
        ORDER BY created_at DESC
        LIMIT %(limit)s OFFSET %(offset)s
    """
    params["limit"] = page_size
    params["offset"] = offset

    results = execute_query(data_query, params)
    return results, total


# Single record lookup
@staticmethod
def get_by_id(record_id: int) -> Optional[dict]:
    """Fetch a single record by ID."""
    query = """
        SELECT id, name, platform, status
        FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.TABLE_NAME
        WHERE id = %(id)s
    """
    results = execute_query(query, {"id": record_id})
    return results[0] if results else None
```

---

### 3. Service Layer (`{feature}/service.py`)

Services contain business logic and orchestrate repository calls.

**File: `app/features/google_ads/overview/service.py`**

```python
"""
Google Ads Overview service - Business logic layer for overview operations.
"""
from datetime import date
from typing import Optional
from fastapi import HTTPException, status

from .repository import google_ads_overview_repository
from .models import GoogleAdsOverviewResponse


class GoogleAdsOverviewService:
    """Service class for Google Ads overview business logic."""

    def __init__(self, repository=google_ads_overview_repository):
        self.repository = repository

    def get_overview(
        self,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> GoogleAdsOverviewResponse:
        """
        Get Google Ads overview metrics, optionally filtered by date range.

        Args:
            date_from: Optional start date for the metrics
            date_to: Optional end date for the metrics

        Returns:
            GoogleAdsOverviewResponse with aggregated metrics

        Raises:
            HTTPException: 400 if date_from > date_to
            HTTPException: 404 if no data found
        """
        # Validate date range if both dates are provided
        if date_from and date_to and date_from > date_to:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="date_from must be less than or equal to date_to"
            )

        # Fetch metrics from repository
        metrics = self.repository.get_overview_metrics(date_from, date_to)

        if not metrics:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No Google Ads data found for date range {date_from} to {date_to}"
            )

        # Map database result (uppercase keys from Snowflake) to response model
        return self._map_to_response(metrics)

    @staticmethod
    def _map_to_response(data: dict) -> GoogleAdsOverviewResponse:
        """Map database row (uppercase keys) to response model."""
        return GoogleAdsOverviewResponse(
            total_spend=float(data.get("TOTAL_SPEND") or 0),
            total_conversions=float(data.get("TOTAL_CONVERSIONS") or 0),
            total_revenue=float(data.get("TOTAL_REVENUE") or 0),
            roas=float(data.get("ROAS") or 0),
            ctr=float(data.get("CTR") or 0),
            cpc=float(data.get("CPC") or 0),
            avg_quality_score=float(data["AVG_QUALITY_SCORE"]) if data.get("AVG_QUALITY_SCORE") is not None else None
        )


# Singleton instance for dependency injection
google_ads_overview_service = GoogleAdsOverviewService()
```

**Service Patterns:**

```python
# Paginated list with business logic
def get_items(
    self,
    page: int = 1,
    page_size: int = 20,
    platform: Optional[str] = None
) -> ItemListResponse:
    """Get paginated list with derived calculations."""
    items, total = self.repository.get_all(
        page=page,
        page_size=page_size,
        platform=platform
    )

    # Apply business logic transformations
    response_items = [self._map_to_response(item) for item in items]

    return ItemListResponse(
        items=response_items,
        total=total,
        page=page,
        page_size=page_size,
        has_next=(page * page_size) < total
    )


# Single item lookup with 404 handling
def get_by_id(self, item_id: int) -> ItemResponse:
    """Get single item, raise 404 if not found."""
    item = self.repository.get_by_id(item_id)

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found"
        )

    return self._map_to_response(item)
```

---

### 4. Router Layer (`{feature}/router.py`)

Routers define API endpoints and delegate to services.

**File: `app/features/google_ads/overview/router.py`**

```python
"""
Google Ads Overview router - API endpoints for overview operations.
"""
from datetime import date
from typing import Optional
from fastapi import APIRouter, Query

from .service import google_ads_overview_service
from .models import GoogleAdsOverviewResponse

router = APIRouter()


@router.get(
    "/overview",
    response_model=GoogleAdsOverviewResponse,
    summary="Get Google Ads overview metrics",
    description="Retrieve aggregated Google Ads performance metrics. Optionally filter by date range."
)
async def get_google_ads_overview(
    date_from: Optional[date] = Query(
        default=None,
        description="Start date for metrics (YYYY-MM-DD format). If not provided, no start date filter.",
        example="2024-01-01"
    ),
    date_to: Optional[date] = Query(
        default=None,
        description="End date for metrics (YYYY-MM-DD format). If not provided, no end date filter.",
        example="2024-12-31"
    ),
):
    """
    Get Google Ads overview metrics including:
    - Total Spend
    - Total Conversions
    - Total Revenue
    - ROAS (Return on Ad Spend)
    - CTR (Click-Through Rate)
    - CPC (Cost Per Click)
    - Average Quality Score
    """
    return google_ads_overview_service.get_overview(
        date_from=date_from,
        date_to=date_to
    )
```

**Router Patterns:**

```python
from typing import Optional
from fastapi import APIRouter, Query, Path

router = APIRouter()


# List endpoint with pagination and filters
@router.get(
    "",
    response_model=ItemListResponse,
    summary="List all items",
    description="Retrieve a paginated list of items with optional filters."
)
async def get_items(
    page: int = Query(default=1, ge=1, description="Page number"),
    page_size: int = Query(default=20, ge=1, le=100, description="Items per page"),
    platform: Optional[str] = Query(default=None, description="Filter by platform"),
    status: Optional[str] = Query(default=None, description="Filter by status"),
):
    """Get paginated items."""
    return item_service.get_items(
        page=page,
        page_size=page_size,
        platform=platform,
        status=status
    )


# Single item endpoint
@router.get(
    "/{item_id}",
    response_model=ItemResponse,
    summary="Get item by ID",
    description="Retrieve a single item by its ID."
)
async def get_item(
    item_id: int = Path(..., gt=0, description="Item ID"),
):
    """Get a specific item by ID."""
    return item_service.get_by_id(item_id)
```

---

### 5. Feature Module (`{platform}/__init__.py`)

Combines all sub-feature routers into a single platform router.

**File: `app/features/google_ads/__init__.py`**

```python
"""
Google Ads feature module - Combines all Google Ads sub-features.
"""
from fastapi import APIRouter

from .overview.router import router as overview_router
# from .campaigns.router import router as campaigns_router
# from .keywords.router import router as keywords_router

# Main router for Google Ads feature
router = APIRouter(prefix="/google-ads", tags=["Google Ads"])

# Include all sub-feature routers
router.include_router(overview_router)
# router.include_router(campaigns_router)
# router.include_router(keywords_router)

__all__ = ["router"]
```

---

### 6. Main Application (`app/main.py`)

Registers all feature routers.

**File: `app/main.py`**

```python
"""
Marketing IQ - FastAPI Application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import feature routers
from app.features.google_ads import router as google_ads_router
# from app.features.meta import router as meta_router

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


# Include feature routers with /api/v1 prefix
app.include_router(google_ads_router, prefix="/api/v1")
# app.include_router(meta_router, prefix="/api/v1")
```

---

## Import Patterns

### Within a Sub-Feature (Relative Imports)

```python
# In service.py - import from same feature folder
from .repository import google_ads_overview_repository
from .models import GoogleAdsOverviewResponse

# In router.py - import from same feature folder
from .service import google_ads_overview_service
from .models import GoogleAdsOverviewResponse
```

### From Core Modules (Absolute Imports)

```python
# In repository.py - import database utilities
from app.core.database import execute_query

# In service.py - import exceptions
from fastapi import HTTPException, status
```

### In Feature __init__.py

```python
# Import sub-feature routers
from .overview.router import router as overview_router
from .campaigns.router import router as campaigns_router
```

---

## Database Conventions

### Snowflake Table References

Always use fully qualified names: `DATABASE.SCHEMA.TABLE`

```sql
-- Correct
SELECT * FROM CLIENT_RARE_SEEDS_DB.PUBLIC_ANALYTICS.FCT_CAMPAIGN_PERFORMANCE

-- Avoid (depends on session context)
SELECT * FROM FCT_CAMPAIGN_PERFORMANCE
```

### Key Tables in PUBLIC_ANALYTICS Schema

| Table | Type | Description |
|-------|------|-------------|
| `FCT_CAMPAIGN_PERFORMANCE` | Fact | Daily campaign metrics (spend, clicks, impressions, conversions) |
| `DIM_PLATFORM` | Dimension | Platform definitions (google_ads, meta, etc.) |
| `DIM_CAMPAIGN` | Dimension | Campaign details |
| `DIM_KEYWORD` | Dimension | Keyword details with quality scores |
| `DIM_AD_GROUP` | Dimension | Ad group details |

### Snowflake Column Naming

Snowflake returns UPPERCASE column names. Map in service layer:

```python
# Database returns: {"TOTAL_SPEND": 1000, "CTR": 2.5}
# Map to response model with lowercase:
return Response(
    total_spend=float(data.get("TOTAL_SPEND") or 0),
    ctr=float(data.get("CTR") or 0)
)
```

### Parameterized Queries (SQL Injection Prevention)

```python
# GOOD - Parameterized
query = "SELECT * FROM table WHERE id = %(id)s AND date >= %(date)s"
execute_query(query, {"id": campaign_id, "date": date_from.isoformat()})

# BAD - SQL Injection vulnerability!
query = f"SELECT * FROM table WHERE id = {campaign_id}"
```

---

## Naming Conventions

| Layer | File Naming | Class Naming | Instance Naming |
|-------|-------------|--------------|-----------------|
| **Models** | `models.py` | `{Feature}Response`, `{Feature}Create` | N/A |
| **Repository** | `repository.py` | `{Feature}Repository` | `{feature}_repository` |
| **Service** | `service.py` | `{Feature}Service` | `{feature}_service` |
| **Router** | `router.py` | N/A | `router` |

### API Route Naming

| HTTP Method | Route Pattern | Description |
|-------------|---------------|-------------|
| GET | `/items` | List items (paginated) |
| GET | `/items/{id}` | Get single item |
| POST | `/items` | Create item |
| PUT | `/items/{id}` | Update item |
| DELETE | `/items/{id}` | Delete item |
| GET | `/items/summary` | Get aggregated data |

---

## Best Practices

### 1. Optional Query Parameters

Make date filters optional with sensible behavior:

```python
@router.get("/metrics")
async def get_metrics(
    date_from: Optional[date] = Query(
        default=None,
        description="Start date (YYYY-MM-DD). If not provided, no start filter.",
        example="2024-01-01"
    ),
    date_to: Optional[date] = Query(
        default=None,
        description="End date (YYYY-MM-DD). If not provided, no end filter.",
        example="2024-12-31"
    ),
):
    pass
```

### 2. Error Handling

Use HTTPException with appropriate status codes:

```python
from fastapi import HTTPException, status

# 400 - Bad Request (validation errors)
if date_from and date_to and date_from > date_to:
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="date_from must be less than or equal to date_to"
    )

# 404 - Not Found
if not data:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No data found for the specified criteria"
    )
```

### 3. Null-Safe Calculations

Handle division by zero and null values:

```python
# In SQL
CASE WHEN SUM(spend) > 0 THEN SUM(revenue) / SUM(spend) ELSE 0 END AS roas

# In Python mapping
total_spend=float(data.get("TOTAL_SPEND") or 0),
avg_score=float(data["AVG_SCORE"]) if data.get("AVG_SCORE") is not None else None
```

### 4. Response Model Validation

Always specify `response_model` for automatic validation and documentation:

```python
@router.get("/overview", response_model=OverviewResponse)
async def get_overview():
    pass  # Response automatically validated against OverviewResponse
```

### 5. Singleton Pattern for DI

Use singleton instances for easy testing:

```python
# In repository.py
google_ads_overview_repository = GoogleAdsOverviewRepository()

# In service.py
class GoogleAdsOverviewService:
    def __init__(self, repository=google_ads_overview_repository):
        self.repository = repository

google_ads_overview_service = GoogleAdsOverviewService()
```

---

## Testing Patterns

### Unit Test Structure

```python
# tests/features/google_ads/overview/test_service.py
import pytest
from unittest.mock import Mock
from fastapi import HTTPException
from app.features.google_ads.overview.service import GoogleAdsOverviewService


class TestGoogleAdsOverviewService:

    @pytest.fixture
    def mock_repository(self):
        return Mock()

    @pytest.fixture
    def service(self, mock_repository):
        return GoogleAdsOverviewService(repository=mock_repository)

    def test_get_overview_returns_metrics(self, service, mock_repository):
        # Arrange
        mock_repository.get_overview_metrics.return_value = {
            "TOTAL_SPEND": 1000.0,
            "TOTAL_CONVERSIONS": 50,
            "TOTAL_REVENUE": 5000.0,
            "ROAS": 5.0,
            "CTR": 2.5,
            "CPC": 1.5,
            "AVG_QUALITY_SCORE": 7.5
        }

        # Act
        result = service.get_overview()

        # Assert
        assert result.total_spend == 1000.0
        assert result.roas == 5.0
        mock_repository.get_overview_metrics.assert_called_once()

    def test_get_overview_invalid_date_range_raises_400(self, service):
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            service.get_overview(
                date_from=date(2024, 12, 31),
                date_to=date(2024, 1, 1)
            )

        assert exc_info.value.status_code == 400

    def test_get_overview_no_data_raises_404(self, service, mock_repository):
        # Arrange
        mock_repository.get_overview_metrics.return_value = None

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            service.get_overview()

        assert exc_info.value.status_code == 404
```

---

## Checklist for New Sub-Feature

When implementing a new sub-feature (e.g., `campaigns` under `google_ads`):

### 1. Create Feature Folder
```
app/features/google_ads/campaigns/
├── __init__.py
├── models.py
├── repository.py
├── service.py
└── router.py
```

### 2. Implementation Order
- [ ] `models.py` - Define request/response Pydantic models
- [ ] `repository.py` - Implement data access with SQL queries
- [ ] `service.py` - Implement business logic and validation
- [ ] `router.py` - Define API endpoints
- [ ] `__init__.py` - Export router (usually just empty or `from .router import router`)

### 3. Register Router
Update `app/features/google_ads/__init__.py`:
```python
from .campaigns.router import router as campaigns_router
router.include_router(campaigns_router)
```

### 4. Quality Checks
- [ ] All inputs validated via Pydantic
- [ ] Parameterized SQL queries (no f-strings with user input)
- [ ] HTTPException with proper status codes
- [ ] response_model on all endpoints
- [ ] Optional filters handled correctly
- [ ] Null-safe calculations in SQL and Python
- [ ] Type hints on all functions

---

## Quick Reference: Adding New Platform

To add a new platform (e.g., `meta`):

1. Create platform folder:
   ```
   app/features/meta/
   ├── __init__.py
   └── overview/
       ├── __init__.py
       ├── models.py
       ├── repository.py
       ├── service.py
       └── router.py
   ```

2. Create platform router (`app/features/meta/__init__.py`):
   ```python
   from fastapi import APIRouter
   from .overview.router import router as overview_router

   router = APIRouter(prefix="/meta", tags=["Meta"])
   router.include_router(overview_router)

   __all__ = ["router"]
   ```

3. Register in `app/main.py`:
   ```python
   from app.features.meta import router as meta_router
   app.include_router(meta_router, prefix="/api/v1")
   ```

4. API will be available at: `GET /api/v1/meta/overview`
