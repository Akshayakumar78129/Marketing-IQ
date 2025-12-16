# Marketing IQ Backend API Implementation Guide

## Overview

This guide defines the standard architecture and patterns for implementing backend APIs in the Marketing IQ application. All new APIs must follow this layered architecture to ensure consistency, maintainability, and testability.

---

## Running the Server

From the `backend/` directory, start the development server with:

1. Activate the virtual environment
```bash
./venv/Scripts/activatein:app --reload
```
2. Run the app
```bash
py -m uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000` with auto-reload enabled for development.

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
│                      ROUTERS (Controllers)                       │
│                       app/routers/*.py                          │
│                                                                 │
│  - Define API endpoints (@router.get, @router.post, etc.)       │
│  - Handle HTTP request/response                                 │
│  - Input validation via Pydantic models                         │
│  - Call Service layer (no business logic here)                  │
└─────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                      SERVICES (Business Logic)                   │
│                       app/services/*.py                         │
│                                                                 │
│  - Implement business rules and logic                           │
│  - Orchestrate multiple repository calls                        │
│  - Data transformation and aggregation                          │
│  - No direct database access (use Repository)                   │
└─────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                    REPOSITORIES (Data Access)                    │
│                     app/repositories/*.py                       │
│                                                                 │
│  - Execute SQL queries via execute_query()                      │
│  - Map database results to domain objects                       │
│  - Handle data persistence operations                           │
│  - No business logic (pure data access)                         │
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
│   ├── main.py                    # FastAPI app entry point
│   │
│   ├── routers/                   # API route handlers
│   │   ├── __init__.py
│   │   ├── campaigns.py           # /api/v1/campaigns endpoints
│   │   ├── accounts.py            # /api/v1/accounts endpoints
│   │   ├── metrics.py             # /api/v1/metrics endpoints
│   │   └── dashboards.py          # /api/v1/dashboards endpoints
│   │
│   ├── services/                  # Business logic layer
│   │   ├── __init__.py
│   │   ├── campaign_service.py
│   │   ├── account_service.py
│   │   ├── metrics_service.py
│   │   └── dashboard_service.py
│   │
│   ├── repositories/              # Data access layer
│   │   ├── __init__.py
│   │   ├── campaign_repository.py
│   │   ├── account_repository.py
│   │   ├── metrics_repository.py
│   │   └── dashboard_repository.py
│   │
│   ├── models/                    # Pydantic request/response models
│   │   ├── __init__.py
│   │   ├── campaign.py            # Campaign-related DTOs
│   │   ├── account.py             # Account-related DTOs
│   │   ├── metrics.py             # Metrics-related DTOs
│   │   ├── dashboard.py           # Dashboard-related DTOs
│   │   └── common.py              # Shared models (pagination, errors)
│   │
│   └── core/                      # Core utilities
│       ├── __init__.py
│       ├── config.py              # Settings management
│       ├── database.py            # Database connection
│       └── exceptions.py          # Custom exceptions
│
└── tests/
    ├── __init__.py
    ├── conftest.py
    ├── routers/
    ├── services/
    └── repositories/
```

---

## Layer Implementation Templates

### 1. Models Layer (`app/models/`)

Models define request/response schemas using Pydantic. Follow these conventions:

**File: `app/models/campaign.py`**

```python
"""
Campaign-related Pydantic models (DTOs).
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


# ============================================================================
# BASE MODELS (shared fields)
# ============================================================================

class CampaignBase(BaseModel):
    """Base campaign fields shared across models."""
    name: str = Field(..., min_length=1, max_length=255, description="Campaign name")
    platform: str = Field(..., description="Platform (google_ads, meta, etc.)")
    status: str = Field(default="active", description="Campaign status")


# ============================================================================
# REQUEST MODELS (input)
# ============================================================================

class CampaignCreate(CampaignBase):
    """Request model for creating a campaign."""
    account_id: int = Field(..., gt=0, description="Associated account ID")
    budget: Optional[float] = Field(None, ge=0, description="Campaign budget")


class CampaignUpdate(BaseModel):
    """Request model for updating a campaign. All fields optional."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    status: Optional[str] = None
    budget: Optional[float] = Field(None, ge=0)


class CampaignFilter(BaseModel):
    """Query parameters for filtering campaigns."""
    platform: Optional[str] = None
    status: Optional[str] = None
    account_id: Optional[int] = None


# ============================================================================
# RESPONSE MODELS (output)
# ============================================================================

class CampaignResponse(CampaignBase):
    """Response model for a single campaign."""
    id: int
    account_id: int
    budget: Optional[float] = None
    impressions: int = 0
    clicks: int = 0
    spend: float = 0.0
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True  # Enable ORM mode for dict unpacking


class CampaignListResponse(BaseModel):
    """Response model for paginated campaign list."""
    items: list[CampaignResponse]
    total: int
    page: int
    page_size: int
    has_next: bool
```

**File: `app/models/common.py`**

```python
"""
Shared/common Pydantic models.
"""
from typing import Generic, TypeVar, Optional
from pydantic import BaseModel, Field

T = TypeVar("T")


class PaginationParams(BaseModel):
    """Standard pagination parameters."""
    page: int = Field(default=1, ge=1, description="Page number")
    page_size: int = Field(default=20, ge=1, le=100, description="Items per page")


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response wrapper."""
    items: list[T]
    total: int
    page: int
    page_size: int
    has_next: bool


class ErrorResponse(BaseModel):
    """Standard error response."""
    error: str
    detail: Optional[str] = None
    code: Optional[str] = None


class SuccessResponse(BaseModel):
    """Standard success response for operations."""
    success: bool = True
    message: str
```

---

### 2. Repository Layer (`app/repositories/`)

Repositories handle all data access. They receive SQL and call `execute_query()`.

**File: `app/repositories/campaign_repository.py`**

```python
"""
Campaign repository - Data access layer for campaigns.
"""
from typing import Optional
from app.core.database import execute_query
from app.models.campaign import CampaignFilter


class CampaignRepository:
    """Repository for campaign data access operations."""

    @staticmethod
    def get_all(
        tenant_id: int,
        filters: Optional[CampaignFilter] = None,
        page: int = 1,
        page_size: int = 20
    ) -> tuple[list[dict], int]:
        """
        Fetch paginated campaigns for a tenant.

        Returns:
            Tuple of (campaigns list, total count)
        """
        # Build WHERE conditions
        conditions = ["tenant_id = %(tenant_id)s"]
        params = {"tenant_id": tenant_id}

        if filters:
            if filters.platform:
                conditions.append("platform = %(platform)s")
                params["platform"] = filters.platform
            if filters.status:
                conditions.append("status = %(status)s")
                params["status"] = filters.status
            if filters.account_id:
                conditions.append("account_id = %(account_id)s")
                params["account_id"] = filters.account_id

        where_clause = " AND ".join(conditions)
        offset = (page - 1) * page_size

        # Get total count
        count_query = f"""
            SELECT COUNT(*) as total
            FROM campaigns
            WHERE {where_clause}
        """
        count_result = execute_query(count_query, params)
        total = count_result[0]["TOTAL"] if count_result else 0

        # Get paginated results
        data_query = f"""
            SELECT
                id,
                account_id,
                name,
                platform,
                status,
                budget,
                impressions,
                clicks,
                spend,
                created_at,
                updated_at
            FROM campaigns
            WHERE {where_clause}
            ORDER BY created_at DESC
            LIMIT %(limit)s OFFSET %(offset)s
        """
        params["limit"] = page_size
        params["offset"] = offset

        campaigns = execute_query(data_query, params)
        return campaigns, total

    @staticmethod
    def get_by_id(campaign_id: int, tenant_id: int) -> Optional[dict]:
        """Fetch a single campaign by ID."""
        query = """
            SELECT
                id,
                account_id,
                name,
                platform,
                status,
                budget,
                impressions,
                clicks,
                spend,
                created_at,
                updated_at
            FROM campaigns
            WHERE id = %(campaign_id)s AND tenant_id = %(tenant_id)s
        """
        params = {"campaign_id": campaign_id, "tenant_id": tenant_id}
        results = execute_query(query, params)
        return results[0] if results else None

    @staticmethod
    def get_metrics_summary(
        tenant_id: int,
        campaign_ids: Optional[list[int]] = None
    ) -> list[dict]:
        """Fetch aggregated metrics for campaigns."""
        query = """
            SELECT
                campaign_id,
                SUM(impressions) as total_impressions,
                SUM(clicks) as total_clicks,
                SUM(spend) as total_spend,
                CASE WHEN SUM(impressions) > 0
                     THEN SUM(clicks) / SUM(impressions) * 100
                     ELSE 0 END as ctr
            FROM campaign_metrics
            WHERE tenant_id = %(tenant_id)s
        """
        params = {"tenant_id": tenant_id}

        if campaign_ids:
            query += " AND campaign_id IN (%(campaign_ids)s)"
            params["campaign_ids"] = ",".join(map(str, campaign_ids))

        query += " GROUP BY campaign_id"

        return execute_query(query, params)


# Singleton instance for dependency injection
campaign_repository = CampaignRepository()
```

---

### 3. Service Layer (`app/services/`)

Services contain business logic and orchestrate repository calls.

**File: `app/services/campaign_service.py`**

```python
"""
Campaign service - Business logic layer for campaigns.
"""
from typing import Optional
from fastapi import HTTPException, status

from app.repositories.campaign_repository import campaign_repository
from app.models.campaign import (
    CampaignCreate,
    CampaignUpdate,
    CampaignFilter,
    CampaignResponse,
    CampaignListResponse,
)


class CampaignService:
    """Service class for campaign business logic."""

    def __init__(self, repository=campaign_repository):
        self.repository = repository

    def get_campaigns(
        self,
        tenant_id: int,
        filters: Optional[CampaignFilter] = None,
        page: int = 1,
        page_size: int = 20
    ) -> CampaignListResponse:
        """
        Get paginated list of campaigns with optional filters.

        Business rules:
        - Only returns campaigns for the specified tenant
        - Applies pagination with sensible defaults
        """
        campaigns, total = self.repository.get_all(
            tenant_id=tenant_id,
            filters=filters,
            page=page,
            page_size=page_size
        )

        # Transform database results to response models
        items = [self._map_to_response(c) for c in campaigns]

        return CampaignListResponse(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            has_next=(page * page_size) < total
        )

    def get_campaign_by_id(
        self,
        campaign_id: int,
        tenant_id: int
    ) -> CampaignResponse:
        """
        Get a single campaign by ID.

        Raises:
            HTTPException: 404 if campaign not found
        """
        campaign = self.repository.get_by_id(campaign_id, tenant_id)

        if not campaign:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Campaign with id {campaign_id} not found"
            )

        return self._map_to_response(campaign)

    def get_campaign_performance(
        self,
        tenant_id: int,
        campaign_ids: Optional[list[int]] = None
    ) -> dict:
        """
        Get aggregated performance metrics for campaigns.

        Business rules:
        - Calculates CTR, CPC, CPM
        - Returns zero-safe calculations
        """
        metrics = self.repository.get_metrics_summary(tenant_id, campaign_ids)

        # Apply business logic: calculate derived metrics
        for metric in metrics:
            clicks = metric.get("TOTAL_CLICKS", 0) or 0
            spend = metric.get("TOTAL_SPEND", 0) or 0

            # Cost per click (avoid division by zero)
            metric["cpc"] = spend / clicks if clicks > 0 else 0

        return {"metrics": metrics}

    @staticmethod
    def _map_to_response(data: dict) -> CampaignResponse:
        """Map database row (uppercase keys) to response model."""
        return CampaignResponse(
            id=data["ID"],
            account_id=data["ACCOUNT_ID"],
            name=data["NAME"],
            platform=data["PLATFORM"],
            status=data["STATUS"],
            budget=data.get("BUDGET"),
            impressions=data.get("IMPRESSIONS", 0),
            clicks=data.get("CLICKS", 0),
            spend=data.get("SPEND", 0.0),
            created_at=data["CREATED_AT"],
            updated_at=data.get("UPDATED_AT"),
        )


# Singleton instance for dependency injection
campaign_service = CampaignService()
```

---

### 4. Router Layer (`app/routers/`)

Routers define API endpoints and delegate to services.

**File: `app/routers/campaigns.py`**

```python
"""
Campaign router - API endpoints for campaign operations.
"""
from typing import Optional
from fastapi import APIRouter, Query, status

from app.services.campaign_service import campaign_service
from app.models.campaign import (
    CampaignFilter,
    CampaignResponse,
    CampaignListResponse,
)

router = APIRouter(prefix="/campaigns", tags=["Campaigns"])


@router.get(
    "",
    response_model=CampaignListResponse,
    summary="List all campaigns",
    description="Retrieve a paginated list of campaigns with optional filters."
)
async def get_campaigns(
    page: int = Query(default=1, ge=1, description="Page number"),
    page_size: int = Query(default=20, ge=1, le=100, description="Items per page"),
    platform: Optional[str] = Query(default=None, description="Filter by platform"),
    status: Optional[str] = Query(default=None, description="Filter by status"),
    account_id: Optional[int] = Query(default=None, description="Filter by account"),
    tenant_id: int = Query(..., description="Tenant ID"),
):
    """Get paginated campaigns for the current tenant."""
    filters = CampaignFilter(
        platform=platform,
        status=status,
        account_id=account_id
    )
    return campaign_service.get_campaigns(
        tenant_id=tenant_id,
        filters=filters,
        page=page,
        page_size=page_size
    )


@router.get(
    "/{campaign_id}",
    response_model=CampaignResponse,
    summary="Get campaign by ID",
    description="Retrieve a single campaign by its ID."
)
async def get_campaign(
    campaign_id: int,
    tenant_id: int = Query(..., description="Tenant ID"),
):
    """Get a specific campaign by ID."""
    return campaign_service.get_campaign_by_id(campaign_id, tenant_id)


@router.get(
    "/performance/summary",
    summary="Get campaign performance metrics",
    description="Retrieve aggregated performance metrics for campaigns."
)
async def get_campaign_performance(
    campaign_ids: Optional[str] = Query(
        default=None,
        description="Comma-separated campaign IDs (optional)"
    ),
    tenant_id: int = Query(..., description="Tenant ID"),
):
    """Get performance metrics for campaigns."""
    ids = None
    if campaign_ids:
        ids = [int(id.strip()) for id in campaign_ids.split(",")]

    return campaign_service.get_campaign_performance(tenant_id, ids)
```

---

### 5. Register Router in Main (`app/main.py`)

**File: `app/main.py`**

```python
"""
Marketing IQ - FastAPI Application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import routers
from app.routers import campaigns, accounts, metrics, dashboards

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


# Include routers with /api/v1 prefix
app.include_router(campaigns.router, prefix="/api/v1")
app.include_router(accounts.router, prefix="/api/v1")
app.include_router(metrics.router, prefix="/api/v1")
app.include_router(dashboards.router, prefix="/api/v1")
```

---

## Naming Conventions

| Layer | File Naming | Class Naming | Function Naming |
|-------|-------------|--------------|-----------------|
| **Models** | `{entity}.py` | `{Entity}Response`, `{Entity}Create` | N/A |
| **Repository** | `{entity}_repository.py` | `{Entity}Repository` | `get_all()`, `get_by_id()` |
| **Service** | `{entity}_service.py` | `{Entity}Service` | `get_{entity}s()`, `create_{entity}()` |
| **Router** | `{entity}s.py` (plural) | N/A | `get_{entity}s()`, `get_{entity}()` |

---

## Best Practices

### 1. Tenant Context

Pass tenant ID as a required query parameter for multi-tenant isolation:

```python
from fastapi import Query

@router.get("/items")
async def get_items(tenant_id: int = Query(..., description="Tenant ID")):
    pass
```

### 2. SQL Injection Prevention

ALWAYS use parameterized queries:

```python
# GOOD - Parameterized
query = "SELECT * FROM campaigns WHERE id = %(id)s"
execute_query(query, {"id": campaign_id})

# BAD - SQL Injection vulnerability!
query = f"SELECT * FROM campaigns WHERE id = {campaign_id}"
```

### 3. Error Handling

Use HTTPException with appropriate status codes:

```python
from fastapi import HTTPException, status

# 404 - Not Found
raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Campaign not found"
)

# 400 - Bad Request
raise HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Invalid date range"
)

# 403 - Forbidden
raise HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Access denied to this resource"
)
```

### 4. Snowflake Column Naming

Snowflake returns uppercase column names. Handle in service layer:

```python
# Database returns: {"ID": 1, "NAME": "Campaign A"}
# Map to response model:
CampaignResponse(
    id=data["ID"],
    name=data["NAME"]
)
```

### 5. Pagination Pattern

Always implement pagination for list endpoints:

```python
@router.get("/items")
async def get_items(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
):
    offset = (page - 1) * page_size
    # Use LIMIT/OFFSET in SQL
```

### 6. Response Model Validation

Always specify `response_model` on endpoints for automatic validation:

```python
@router.get("/campaigns", response_model=CampaignListResponse)
async def get_campaigns():
    pass  # Response automatically validated
```

### 7. Logging

Add logging for debugging and monitoring:

```python
import logging

logger = logging.getLogger(__name__)

class CampaignService:
    def get_campaigns(self, tenant_id: int):
        logger.info(f"Fetching campaigns for tenant {tenant_id}")
        # ...
```

### 8. Type Hints

Always use type hints for better code quality:

```python
def get_by_id(self, campaign_id: int, tenant_id: int) -> Optional[dict]:
    pass

def get_campaigns(self, filters: CampaignFilter) -> CampaignListResponse:
    pass
```

---

## Testing Patterns

### Unit Test Structure

```python
# tests/services/test_campaign_service.py
import pytest
from unittest.mock import Mock, patch
from app.services.campaign_service import CampaignService


class TestCampaignService:

    @pytest.fixture
    def mock_repository(self):
        return Mock()

    @pytest.fixture
    def service(self, mock_repository):
        return CampaignService(repository=mock_repository)

    def test_get_campaigns_returns_list(self, service, mock_repository):
        # Arrange
        mock_repository.get_all.return_value = ([{"ID": 1, "NAME": "Test"}], 1)

        # Act
        result = service.get_campaigns(tenant_id=1)

        # Assert
        assert len(result.items) == 1
        mock_repository.get_all.assert_called_once()

    def test_get_campaign_by_id_not_found_raises_404(self, service, mock_repository):
        # Arrange
        mock_repository.get_by_id.return_value = None

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            service.get_campaign_by_id(999, tenant_id=1)

        assert exc_info.value.status_code == 404
```

---

## Checklist for New API Implementation

When implementing a new API endpoint, follow this checklist:

- [ ] **Models**: Create request/response Pydantic models in `app/models/{entity}.py`
- [ ] **Repository**: Create data access class in `app/repositories/{entity}_repository.py`
- [ ] **Service**: Create business logic class in `app/services/{entity}_service.py`
- [ ] **Router**: Create API routes in `app/routers/{entity}s.py`
- [ ] **Main**: Register router in `app/main.py` with proper prefix
- [ ] **Tests**: Add unit tests for service and repository layers
- [ ] **Validation**: Ensure all inputs are validated via Pydantic
- [ ] **Pagination**: Implement pagination for list endpoints
- [ ] **Error Handling**: Use HTTPException with proper status codes
- [ ] **SQL Safety**: Use parameterized queries (never string formatting)
- [ ] **Multi-tenancy**: Always filter by `tenant_id`

---

## Quick Reference: File Creation Order

When adding a new entity (e.g., "accounts"):

1. `app/models/account.py` - Define DTOs
2. `app/repositories/account_repository.py` - Data access
3. `app/services/account_service.py` - Business logic
4. `app/routers/accounts.py` - API endpoints
5. Update `app/main.py` - Register router
6. `tests/services/test_account_service.py` - Tests
