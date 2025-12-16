# Marketing IQ - Project Standards & Coding Rules

> **IMPORTANT:** These rules MUST be followed throughout the entire project. Reference this document before writing any code.

---

## Table of Contents
1. [Data Layer Standards](#1-data-layer-standards)
2. [Backend Standards](#2-backend-standards)
3. [API Standards](#3-api-standards)
4. [Frontend Standards](#4-frontend-standards)
5. [Security Standards](#5-security-standards)
6. [Error Handling Standards](#6-error-handling-standards)
7. [Testing Standards](#7-testing-standards)
8. [Code Organization Standards](#8-code-organization-standards)

---

## 1. Data Layer Standards

### 1.1 NO Raw SQL in Application Code
```python
# NEVER DO THIS
cursor.execute("SELECT * FROM campaigns WHERE tenant_id = '" + tenant_id + "'")

# NEVER DO THIS EITHER
query = f"SELECT * FROM fact_campaign WHERE date BETWEEN '{start}' AND '{end}'"
```

### 1.2 USE DBT for All Data Transformations
- All fact and dimension tables MUST be created via DBT models
- NO raw SQL files for creating analytics tables
- All transformations are version-controlled in `dbt/` folder

```
dbt/models/
├── staging/      # Clean raw Fivetran data
├── intermediate/ # Business logic transformations
└── marts/        # Final fact/dim tables for API consumption
```

### 1.3 USE Repository Pattern for Data Access
```python
# ALWAYS USE THIS PATTERN
class CampaignRepository:
    def __init__(self, tenant_id: str, db: SnowflakeConnection):
        self.tenant_id = tenant_id  # Set once, enforced everywhere
        self.db = db

    def get_performance(
        self,
        metrics: list[Metric],
        filters: FilterSet,
        date_range: DateRange
    ) -> list[CampaignPerformance]:
        query = self._build_query(metrics, filters, date_range)
        return self._execute(query)
```

### 1.4 USE Query Builder (PyPika) Instead of Raw SQL
```python
# CORRECT - Using query builder
from pypika import Query, Table, Field

fact_campaign = Table('fact_campaign_performance_daily')

query = (
    Query.from_(fact_campaign)
    .select(
        fact_campaign.campaign_id,
        fn.Sum(fact_campaign.clicks).as_('total_clicks')
    )
    .where(fact_campaign.tenant_id == self.tenant_id)
    .where(fact_campaign.date >= date_range.start)
    .where(fact_campaign.date <= date_range.end)
    .groupby(fact_campaign.campaign_id)
)
```

### 1.5 Fivetran for ETL - NO Custom Pipelines
- All data ingestion is handled by Fivetran
- NO Prefect, Airflow, or custom ETL scripts
- DBT transforms Fivetran data, that's it

### 1.6 Star Schema Data Model (21 Dimensions + 22 Facts)

**Dimension Tables (21):**
| Table | Source | Purpose |
|-------|--------|---------|
| DIM_DATE | Generated | Date attributes |
| DIM_HOUR | Generated | Hour of day |
| DIM_PLATFORM | Generated | google_ads, meta, ga4, klaviyo |
| DIM_DEVICE | GA4 + Meta | desktop, mobile, tablet |
| DIM_ACCOUNT | All platforms | Account metadata |
| DIM_CAMPAIGN | All platforms | Campaign attributes |
| DIM_AD_GROUP | Google Ads | Ad groups |
| DIM_AD_SET | Facebook Ads | Ad sets |
| DIM_AD | Google + Facebook | Ad creative |
| DIM_KEYWORD | Google Ads | Keywords |
| DIM_GEOGRAPHY | All platforms | Country, region, city |
| DIM_SOURCE_MEDIUM | GA4 | Traffic sources |
| DIM_CONVERSION_ACTION | GA4 + Google Ads | Conversion types |
| DIM_EMAIL_CAMPAIGN | Klaviyo | Email campaigns |
| DIM_EMAIL_FLOW | Klaviyo | Automated flows |
| DIM_EMAIL_TEMPLATE | Klaviyo | Template content |
| DIM_SEGMENT | Klaviyo | Audience segments |
| DIM_LIST | Klaviyo | Email lists |
| DIM_BIDDING_STRATEGY | Google Ads | Bidding configs |
| DIM_AUDIENCE | Google + Meta | Audience definitions |
| DIM_VIDEO | Facebook Ads | Video creative |

**Fact Tables (22):**
| Table | Grain | Purpose |
|-------|-------|---------|
| FACT_CAMPAIGN_PERFORMANCE_DAILY | Campaign × Date × Device | Core metrics |
| FACT_CAMPAIGN_HOURLY | Campaign × Date × Hour | Hourly trends |
| FACT_AD_GROUP_PERFORMANCE_DAILY | Ad Group × Date | Google ad groups |
| FACT_AD_SET_PERFORMANCE_DAILY | Ad Set × Date | Facebook ad sets |
| FACT_AD_PERFORMANCE_DAILY | Ad × Date × Device | Ad-level metrics |
| FACT_VIDEO_PERFORMANCE_DAILY | Video × Date | Video milestones |
| FACT_AD_REACTIONS_DAILY | Ad × Date × Reaction | Facebook reactions |
| FACT_KEYWORD_PERFORMANCE_DAILY | Keyword × Date | Keyword metrics |
| FACT_SEARCH_TERM_DAILY | Keyword × Search Term × Date | Search queries |
| FACT_GA4_TRAFFIC_DAILY | Source × Geo × Device × Date | Website traffic |
| FACT_GA4_CONVERSIONS_DAILY | Conversion × Source × Date | Conversions |
| FACT_ECOMMERCE_ITEM_DAILY | Item × Date | Product sales |
| FACT_EMAIL_CAMPAIGN_DAILY | Campaign × Message × Date | Email metrics |
| FACT_EMAIL_FLOW_DAILY | Flow × Action × Date | Flow metrics |
| FACT_SEGMENT_MEMBERSHIP | Segment × Person × Date | Segment membership |
| FACT_LIST_MEMBERSHIP | List × Person × Date | List membership |
| FACT_DEMOGRAPHICS_DAILY | Campaign × Geo × Age × Gender × Date | Demographics |
| FACT_AUDIENCE_DAILY | Campaign × Audience × Date | Audience performance |
| FACT_CAMPAIGN_SETTINGS_HISTORY | Campaign × Change Date | Config changes |
| FACT_AD_GROUP_SETTINGS_HISTORY | Ad Group × Change Date | Config changes |
| FACT_BIDDING_CHANGES_HISTORY | Entity × Change Date | Bidding changes |
| FACT_BUDGET_CHANGES_HISTORY | Campaign × Change Date | Budget changes |

### 1.7 Data Coverage Requirements
| Platform | Min Coverage | What Must Be Captured |
|----------|--------------|----------------------|
| Google Ads | 98% | All performance + config history |
| Facebook Ads | 95% | All performance + video + reactions |
| GA4 | 85% | All reports (raw events unavailable) |
| Klaviyo | 98% | All performance + segment membership |

---

## 2. Backend Standards

### 2.1 Architecture Layers (Strict Separation)
```
┌─────────────────────────────────────────────────────┐
│  API Layer (api/v1/*.py)                            │
│  - HTTP request/response handling ONLY              │
│  - Input validation via Pydantic                    │
│  - NO business logic here                           │
├─────────────────────────────────────────────────────┤
│  Service Layer (services/*.py)                      │
│  - All business logic lives here                    │
│  - Orchestrates repositories and cache              │
│  - Transaction management                           │
├─────────────────────────────────────────────────────┤
│  Repository Layer (repositories/*.py)               │
│  - Data access ONLY                                 │
│  - Query building                                   │
│  - NO business logic here                           │
├─────────────────────────────────────────────────────┤
│  Cache Layer (cache/*.py)                           │
│  - Redis operations                                 │
│  - Cache key management                             │
│  - TTL policies                                     │
├─────────────────────────────────────────────────────┤
│  Database Layer (db/*.py)                           │
│  - Connection management                            │
│  - Connection pooling                               │
│  - Health checks                                    │
└─────────────────────────────────────────────────────┘
```

### 2.2 Dependency Injection Pattern
```python
# ALWAYS inject dependencies, never instantiate inside functions
class MetricsService:
    def __init__(
        self,
        campaign_repo: CampaignRepository,
        cache_manager: CacheManager,
        snowflake: SnowflakeConnection
    ):
        self.campaign_repo = campaign_repo
        self.cache_manager = cache_manager
        self.snowflake = snowflake

# In FastAPI endpoints
@router.post("/metrics")
async def get_metrics(
    request: MetricsRequest,
    service: MetricsService = Depends(get_metrics_service)
):
    return await service.get_metrics(request)
```

### 2.3 Pydantic for All Data Validation
```python
# ALWAYS define request/response schemas
class MetricsRequest(BaseModel):
    metrics: list[MetricName]
    dimensions: list[DimensionName]
    filters: list[Filter]
    date_range: DateRange

    class Config:
        extra = "forbid"  # Reject unknown fields

class MetricsResponse(BaseModel):
    data: list[dict]
    metadata: ResponseMetadata
    pagination: PaginationInfo
```

### 2.4 Async/Await for All I/O Operations
```python
# ALWAYS use async for database, cache, external calls
async def get_campaign_performance(self) -> list[dict]:
    cached = await self.cache.get(cache_key)
    if cached:
        return cached

    result = await self.snowflake.execute(query)
    await self.cache.set(cache_key, result, ttl=3600)
    return result
```

---

## 3. API Standards

### 3.1 Unified Metrics Endpoint
- ONE endpoint for all metric queries: `POST /api/v1/metrics`
- NO separate endpoints per dashboard
- Parameters determine what data is returned

### 3.2 Consistent Response Format
```python
# ALL API responses follow this structure
{
    "data": [...],           # Always an array
    "metadata": {
        "total_rows": 1500,
        "query_time_ms": 245,
        "cache_status": "hit" | "miss",
        "data_freshness": "2024-01-15T06:00:00Z"
    },
    "pagination": {
        "limit": 100,
        "offset": 0,
        "has_more": true
    },
    "errors": []             # Empty if success
}
```

### 3.3 Filter Schema
```python
class Filter(BaseModel):
    field: str
    operator: Literal["eq", "ne", "in", "not_in", "between", "gt", "gte", "lt", "lte", "contains"]
    value: Any

# Example usage
filters = [
    {"field": "platform", "operator": "in", "value": ["google_ads", "meta"]},
    {"field": "date", "operator": "between", "value": ["2024-01-01", "2024-01-31"]},
    {"field": "spend", "operator": "gt", "value": 100}
]
```

### 3.4 Mandatory Pagination
```python
# ALL list endpoints MUST be paginated
class PaginationParams(BaseModel):
    limit: int = Field(default=100, le=1000)  # Max 1000 rows
    offset: int = Field(default=0, ge=0)
```

### 3.5 API Versioning
- All endpoints under `/api/v1/`
- Breaking changes require new version (`/api/v2/`)
- Old versions supported for 6 months minimum

---

## 4. Frontend Standards

### 4.1 Component Organization
```
components/
├── ui/           # shadcn/ui primitives (Button, Card, etc.)
├── charts/       # Chart components (LineChart, BarChart, etc.)
├── filters/      # Filter components (DateRangePicker, MultiSelect)
├── dashboard/    # Dashboard-specific components
└── layout/       # Layout components (Sidebar, Header)
```

### 4.2 Custom Hooks for Data Fetching
```typescript
// ALWAYS use custom hooks, never fetch in components
function useMetrics(params: MetricsParams) {
  return useQuery({
    queryKey: ['metrics', params],
    queryFn: () => api.metrics.get(params),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
}

// In component
function CampaignDashboard() {
  const { data, isLoading, error } = useMetrics({
    metrics: ['clicks', 'impressions'],
    dateRange: selectedRange
  });
}
```

### 4.3 Type Safety
```typescript
// ALWAYS define types for API responses
interface MetricsResponse {
  data: MetricData[];
  metadata: ResponseMetadata;
  pagination: PaginationInfo;
}

// NEVER use `any` type
// eslint rule: @typescript-eslint/no-explicit-any: error
```

### 4.4 Loading & Error States
```typescript
// ALWAYS handle loading and error states
if (isLoading) return <DashboardSkeleton />;
if (error) return <ErrorMessage error={error} />;
if (!data?.data.length) return <EmptyState />;

return <DashboardContent data={data} />;
```

---

## 5. Security Standards

### 5.1 Tenant Isolation (CRITICAL)
```python
# EVERY database query MUST filter by tenant_id
class BaseRepository:
    def __init__(self, tenant_id: str):
        if not tenant_id:
            raise ValueError("tenant_id is required")
        self.tenant_id = tenant_id

    def _base_query(self, table: Table) -> QueryBuilder:
        # ALL queries start with tenant filter
        return Query.from_(table).where(table.tenant_id == self.tenant_id)

# NEVER allow queries without tenant_id
# NEVER trust client-provided tenant_id - extract from JWT
```

### 5.2 Input Validation
```python
# ALWAYS validate and sanitize inputs
class FilterField(str, Enum):
    CAMPAIGN = "campaign"
    DATE = "date"
    PLATFORM = "platform"
    # ... whitelist allowed fields

class Filter(BaseModel):
    field: FilterField  # Only allowed fields
    operator: FilterOperator
    value: Any

    @validator('value')
    def validate_value(cls, v, values):
        # Validate value based on field type
        pass
```

### 5.3 No SQL Injection Possible
- Query builder with parameterized queries
- No string concatenation for SQL
- No f-strings with user input

### 5.4 Secrets Management
```python
# NEVER hardcode secrets
# ALWAYS use environment variables or Azure Key Vault

class Settings(BaseSettings):
    snowflake_password: SecretStr
    jwt_secret: SecretStr

    class Config:
        env_file = ".env"
```

---

## 6. Error Handling Standards

### 6.1 Custom Exception Classes
```python
# Define specific exceptions
class TenantNotFoundError(Exception):
    pass

class InvalidFilterError(Exception):
    pass

class SnowflakeConnectionError(Exception):
    pass

class CacheUnavailableError(Exception):
    pass
```

### 6.2 Circuit Breaker for External Services
```python
class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, reset_timeout: int = 60):
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.state = CircuitState.CLOSED
        self.last_failure_time = None

    async def execute(self, func: Callable) -> Any:
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self.state = CircuitState.HALF_OPEN
            else:
                raise ServiceUnavailableError("Service temporarily unavailable")

        try:
            result = await func()
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise
```

### 6.3 Graceful Degradation
```python
async def get_metrics_with_fallback(self, request: MetricsRequest):
    try:
        # Try live data
        return await self.get_live_metrics(request)
    except SnowflakeConnectionError:
        # Fall back to cached data with warning
        cached = await self.cache.get_stale(cache_key)
        if cached:
            return MetricsResponse(
                data=cached,
                metadata={"warning": "Using cached data, live data unavailable"}
            )
        raise ServiceUnavailableError("Data temporarily unavailable")
```

### 6.4 Structured Error Responses
```python
# ALL errors return consistent format
{
    "error": {
        "code": "INVALID_FILTER",
        "message": "Filter field 'foo' is not allowed",
        "details": {
            "field": "foo",
            "allowed_fields": ["campaign", "date", "platform"]
        }
    }
}
```

---

## 7. Testing Standards

### 7.1 Test Structure
```
tests/
├── unit/
│   ├── test_services/
│   ├── test_repositories/
│   └── test_utils/
├── integration/
│   ├── test_api/
│   └── test_database/
└── conftest.py  # Shared fixtures
```

### 7.2 Repository Tests with Mocked DB
```python
@pytest.fixture
def mock_snowflake():
    return AsyncMock(spec=SnowflakeConnection)

async def test_campaign_repo_filters_by_tenant(mock_snowflake):
    repo = CampaignRepository(tenant_id="tenant_123", db=mock_snowflake)
    await repo.get_performance(...)

    # Verify tenant_id was in the query
    query = mock_snowflake.execute.call_args[0][0]
    assert "tenant_id = 'tenant_123'" in str(query)
```

### 7.3 API Tests
```python
async def test_metrics_endpoint_requires_auth(client):
    response = await client.post("/api/v1/metrics", json={...})
    assert response.status_code == 401

async def test_metrics_returns_paginated_results(authenticated_client):
    response = await authenticated_client.post("/api/v1/metrics", json={
        "metrics": ["clicks"],
        "limit": 10
    })
    assert response.status_code == 200
    assert len(response.json()["data"]) <= 10
    assert "pagination" in response.json()
```

---

## 8. Code Organization Standards

### 8.1 File Naming
```
# Python: snake_case
campaign_repository.py
metrics_service.py

# TypeScript: kebab-case for files, PascalCase for components
date-range-picker.tsx
export function DateRangePicker() {...}

# DBT models: snake_case with prefixes
stg_google_ads__campaigns.sql
int_campaign_performance.sql
fact_campaign_performance_daily.sql
dim_campaign.sql
```

### 8.2 Import Order
```python
# 1. Standard library
import os
from datetime import datetime

# 2. Third-party packages
from fastapi import APIRouter, Depends
from pydantic import BaseModel

# 3. Local imports
from app.services import MetricsService
from app.repositories import CampaignRepository
```

### 8.3 Constants Location
```python
# app/core/constants.py
class Platform(str, Enum):
    GOOGLE_ADS = "google_ads"
    META = "meta"
    GA4 = "ga4"
    KLAVIYO = "klaviyo"

class MetricName(str, Enum):
    IMPRESSIONS = "impressions"
    CLICKS = "clicks"
    SPEND = "spend"
    CONVERSIONS = "conversions"
    CTR = "ctr"
    CPC = "cpc"
    ROAS = "roas"
```

### 8.4 Configuration
```python
# app/core/config.py
class Settings(BaseSettings):
    # Database
    database_url: PostgresDsn
    snowflake_account: str
    snowflake_database: str = "CLIENT_RARE_SEEDS_DB"

    # Cache
    redis_url: RedisDsn
    cache_default_ttl: int = 3600

    # API
    api_v1_prefix: str = "/api/v1"
    max_page_size: int = 1000

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
```

---

## Quick Reference Card

| Area | Rule | Reason |
|------|------|--------|
| Data | Use DBT, not raw SQL | Version control, testing |
| Data | Use Repository Pattern | Separation of concerns |
| Data | Use PyPika query builder | No SQL injection |
| API | Single unified endpoint | Simpler, cacheable |
| API | Always paginate | Performance |
| Security | Always filter by tenant_id | Data isolation |
| Security | Validate all inputs | Security |
| Errors | Use circuit breaker | Resilience |
| Errors | Graceful degradation | UX |
| Frontend | Custom hooks for data | Reusability |
| Frontend | Handle loading/error | UX |
| Testing | Test tenant isolation | Security |

---

**Last Updated:** 2024-01-15
**Version:** 1.0
