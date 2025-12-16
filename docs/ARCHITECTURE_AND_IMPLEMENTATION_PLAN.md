# Marketing IQ - Complete Architecture & Implementation Plan

## Executive Summary

**Product Type:** Multi-tenant SaaS marketing analytics platform
**Target Market:** Marketing agencies and businesses needing unified analytics
**Data Volume:** 1-10TB across all tenants
**Team Size:** 3-5 people
**MVP Timeline:** 8-12 weeks
**Estimated Monthly Cost:** $400-$800 (MVP), scaling to $1,500-$2,500

---

## Table of Contents

1. [Product Vision](#product-vision)
2. [Critical Architectural Review](#critical-architectural-review)
3. [System Architecture](#system-architecture)
4. [Technology Stack](#technology-stack)
5. [Multi-Tenant Design](#multi-tenant-design)
6. [Database Schema](#database-schema)
7. [ETL Pipeline Design](#etl-pipeline-design)
8. [API Architecture](#api-architecture)
9. [Security & Authentication](#security--authentication)
10. [Implementation Plan](#implementation-plan)
11. [Code Examples](#code-examples)
12. [Testing Strategy](#testing-strategy)
13. [Deployment & DevOps](#deployment--devops)
14. [Cost Analysis](#cost-analysis)
15. [Risks & Mitigations](#risks--mitigations)

---

## Product Vision

### What We're Building

An AI-enabled analytical dashboard application that:
- Aggregates data from **Google Ads, Meta Ads, and Google Analytics**
- Provides **25 individual dashboards** across **5 segments**
- Runs **configurable ETL pipelines** (default: 3x daily)
- Stores data in a **data warehouse** with proper fact/dimensional schema
- Exposes **REST APIs** with filtering and caching
- Supports **multi-tenant SaaS** model
- Prepares for future **agentic AI framework** integration

### What Makes This Different

- **Multi-tenant from Day 1:** Built to serve multiple customers, not just one
- **API-first:** All data access through consistent APIs
- **Cloud-native:** Leverages best-of-breed cloud services (Snowflake + Azure)
- **AI-ready:** Architecture designed to support future LLM agents

---

## Critical Architectural Review

### ✅ What's Good in Original Proposal

1. **Python for backend/ETL** - Correct choice, compatible with data science ecosystem
2. **Fact/dimensional tables** - Shows proper data warehouse understanding
3. **API-based data access** - Smart for preventing agent/dashboard inconsistency
4. **Configurable ETL frequency** - Good flexibility
5. **Best-of-breed cloud stack** - Snowflake for warehouse, Azure for compute/storage

### ⚠️ Critical Issues Found & Fixed

#### 1. **OVER-ENGINEERING: 25 Separate APIs**

**Original Proposal:** Build 25 individual APIs, one per dashboard

**Problem:**
- Massive code duplication
- Maintenance nightmare
- Inconsistent filtering logic
- Harder to evolve

**Solution:**
Consolidate to **1-3 unified APIs** with parameters:
```
GET /api/v1/dashboards/{dashboard_id}?metrics=ctr,conversions&date_range=30d
GET /api/v1/metrics?metrics[]=impressions&dimensions[]=campaign&filters={}
```

#### 2. **MISSING: Data Transformation Layer**

**Problem:** Raw data from Google Ads/Meta ≠ dashboard-ready data

**Solution:** Implement **DBT (Data Build Tool)**
- Industry standard for SQL transformations
- Version-controlled data models
- Built-in testing and documentation
- Incremental materialization

#### 3. **MISSING: Multi-Tenant Architecture**

**Original Proposal:** Generic architecture, no multi-tenancy mentioned

**Critical Gap:** For a SaaS product serving multiple clients, you need:
- Tenant isolation (can't see each other's data)
- Per-tenant OAuth tokens (each client connects their own accounts)
- Per-tenant configuration (different dashboards, ETL schedules)
- User management with RBAC
- Billing and metering

**Solution:** Implemented comprehensive multi-tenant design with Row-Level Security

#### 4. **MISSING: Application Authentication**

**Problem:** OAuth for platforms mentioned, but nothing for securing YOUR APIs

**Solution:**
- User authentication (Supabase Auth or Azure AD B2C)
- JWT-based API authentication
- Role-Based Access Control (Admin, Analyst, Viewer)
- Per-tenant rate limiting

#### 5. **UNDEFINED: Data Warehouse Choice**

**Problem:** "We need to decide on type of warehouse" - too vague

**Solution:** For 1-10TB SaaS product:
- **Chosen:** Snowflake (best for multi-tenant SaaS)
- **Why:** Better performance, lower cost, simpler management
- **Alternative:** Azure Synapse (if you need Azure-only stack)

#### 6. **MISSING: Complete List of Components**

**Added:**
- Monitoring & observability (Sentry, Azure Monitor)
- Caching layer (Redis)
- Message queue (Azure Service Bus)
- Secrets management (Azure Key Vault)
- API gateway (Azure API Management)
- Data quality checks
- Tenant onboarding flow
- Billing & metering system
- CI/CD pipeline
- Infrastructure as Code (Terraform)

---

## System Architecture

### High-Level Architecture Diagram

```
┌──────────────────────────────────────────────────────────────────┐
│                  TENANTS (Multiple Companies)                     │
│         Each with their own Google Ads, Meta, GA accounts        │
└──────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│                   AUTHENTICATION LAYER                            │
│                   Supabase Auth / Azure AD B2C                    │
│                   - User signup/login                             │
│                   - JWT tokens                                    │
└──────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│                    API GATEWAY (Future)                           │
│                  Azure API Management                             │
│                  - Rate limiting                                  │
│                  - Request analytics                              │
└──────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│                   TENANT MANAGEMENT SERVICE                       │
│                        FastAPI                                    │
│                   - Tenant CRUD                                   │
│                   - OAuth setup                                   │
│                   - User management                               │
└──────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│              MULTI-TENANT ETL ORCHESTRATION                       │
│                    Prefect Cloud                                  │
│                                                                   │
│  Per Tenant (Dynamic DAGs):                                       │
│  1. Fetch OAuth tokens (Azure Key Vault)                         │
│  2. Extract from Google Ads/Meta/GA APIs                          │
│  3. Handle rate limits & pagination                               │
│  4. Load to staging (Azure Blob)                                  │
│  5. Run DBT transformations                                       │
│  6. Load to Synapse (with tenant_id)                              │
│  7. Invalidate cache                                              │
└──────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│                      STAGING LAYER                                │
│                  Azure Blob Storage                               │
│         /tenant-{id}/raw/{platform}/YYYY-MM-DD/                  │
└──────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│                  TRANSFORMATION LAYER                             │
│                      DBT Cloud                                    │
│                                                                   │
│  Models:                                                          │
│  - Staging: Clean raw data, add tenant_id                        │
│  - Intermediate: Join across platforms                           │
│  - Marts: Dashboard-ready aggregations                           │
└──────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│                   DATA WAREHOUSE                                  │
│              Azure Synapse Analytics                              │
│                                                                   │
│  - Fact Tables (metrics with tenant_id)                          │
│  - Dimension Tables (campaigns, dates, etc.)                     │
│  - Row-Level Security (RLS)                                      │
│  - Star/Snowflake Schema                                         │
└──────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│                      API LAYER                                    │
│                  FastAPI (Python)                                 │
│                                                                   │
│  Endpoints:                                                       │
│  - GET /api/v1/dashboards                                        │
│  - GET /api/v1/dashboards/{id}                                   │
│  - GET /api/v1/metrics (unified query)                           │
│                                                                   │
│  Features:                                                        │
│  - Filtering & pagination                                        │
│  - Tenant isolation                                              │
│  - RBAC authorization                                            │
│  - Request validation                                            │
└──────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│                    CACHING LAYER                                  │
│               Upstash Redis → Azure Redis                         │
│                                                                   │
│  - Per-tenant cache namespaces                                   │
│  - 5-minute TTL for dashboard data                               │
│  - Invalidation on ETL completion                                │
└──────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│                  CONSUMPTION LAYER                                │
│                                                                   │
│  ┌──────────────────────────────────┐                           │
│  │  Next.js Frontend (Future)       │                           │
│  │  - Dashboard UI                  │                           │
│  │  - Tenant admin panel            │                           │
│  └──────────────────────────────────┘                           │
│                                                                   │
│  ┌──────────────────────────────────┐                           │
│  │  Agentic AI Framework (Future)   │                           │
│  │  - LangGraph / CrewAI            │                           │
│  │  - Cross-dashboard queries       │                           │
│  │  - Data via APIs (consistency)   │                           │
│  └──────────────────────────────────┘                           │
└──────────────────────────────────────────────────────────────────┘
```

### Architecture Layers Explained

#### 1. **Data Ingestion Layer**
- **Purpose:** Extract data from marketing platforms
- **Technology:** Prefect Cloud (managed orchestration)
- **Key Features:**
  - OAuth 2.0 authentication
  - Rate limiting & retry logic
  - Incremental extraction
  - Error handling & alerting
  - Per-tenant scheduling

#### 2. **Data Storage Layer**
- **Staging:** Azure Blob Storage (raw data)
- **Warehouse:** Azure Synapse Analytics (transformed data)
- **App Database:** Supabase/Postgres (tenants, users, config)
- **Cache:** Redis (API responses)

#### 3. **Data Transformation Layer**
- **Purpose:** Clean, join, aggregate raw data
- **Technology:** DBT (Data Build Tool)
- **Key Features:**
  - SQL-based transformations
  - Incremental materialization
  - Data quality tests
  - Documentation generation

#### 4. **API Layer**
- **Purpose:** Expose data to frontends and agents
- **Technology:** FastAPI on Azure Container Apps
- **Key Features:**
  - RESTful endpoints
  - JWT authentication
  - Tenant isolation via middleware
  - RBAC authorization
  - Response caching
  - Rate limiting

#### 5. **Cross-Cutting Concerns**
- **Security:** Azure Key Vault, RLS policies
- **Monitoring:** Sentry, Azure Monitor, Application Insights
- **DevOps:** GitHub Actions, Terraform
- **Billing:** Stripe integration, usage metering

---

## Technology Stack

### Complete Tech Stack (Startup-Optimized)

| Component | Technology | Rationale |
|-----------|------------|-----------|
| **Data Warehouse** | Azure Synapse Serverless → Dedicated Pool | Pay-per-query for MVP, scale to dedicated when needed |
| **ETL Orchestration** | Prefect Cloud | Managed, better DX than Airflow, Python-native |
| **Data Transformation** | DBT Cloud | Managed DBT, SQL-based, testable |
| **API Framework** | FastAPI | Modern, fast, async, auto-docs, Python 3.11+ |
| **Application Database** | Supabase (Postgres) | Fast setup, managed, includes auth |
| **User Authentication** | Supabase Auth or Clerk | Faster than Azure AD B2C for startups |
| **Caching** | Upstash Redis (serverless) | Pay-per-request for MVP, migrate to Azure Redis later |
| **Blob Storage** | Azure Blob Storage | Azure-native, cheap, reliable |
| **Secret Management** | Azure Key Vault | Secure, auditable, Azure-native |
| **Container Hosting** | Azure Container Apps | Simpler than AKS, auto-scaling, cost-effective |
| **Monitoring (Errors)** | Sentry | Better DX than App Insights for startups |
| **Monitoring (Infra)** | Azure Monitor | Azure-native, infrastructure monitoring |
| **Logging** | Better Stack (Logtail) | Centralized logging, great search |
| **API Gateway** | Skip for MVP → Azure APIM | Add when 10+ customers |
| **CI/CD** | GitHub Actions | Free for public/private repos, easy setup |
| **Infrastructure as Code** | Terraform | Multi-cloud, declarative, widely used |
| **Message Queue** | Azure Service Bus | Async tasks, notifications |
| **Billing** | Stripe | Easy integration, subscription management |
| **Frontend (Future)** | Next.js 14+ | React framework, App Router, Server Components |
| **AI Framework (Future)** | LangGraph or CrewAI | Multi-agent orchestration |

### Why This Stack?

**For a 3-5 Person Startup Team:**

1. **Prefer Managed Services** - Your time > server costs
   - Prefect Cloud vs self-hosted Airflow
   - DBT Cloud vs DBT Core on VMs
   - Supabase vs managing Postgres
   - Azure Container Apps vs Kubernetes

2. **Python-First** - Single language for backend, ETL, future AI
   - FastAPI for APIs
   - Prefect for ETL
   - DBT for SQL (called from Python)
   - Future: LangGraph for AI agents

3. **Cloud-Compatible** - Best-of-breed services
   - Snowflake (data warehouse)
   - Azure Blob Storage (staging)
   - Azure Key Vault (secrets)
   - Azure Container Apps (hosting)
   - Azure Monitor (observability)

4. **Developer Experience** - Fast iteration, good docs
   - FastAPI auto-generates API docs
   - Prefect has beautiful UI
   - DBT has excellent documentation
   - Sentry has great error tracking

---

## Multi-Tenant Design

### Multi-Tenancy Strategy

**Chosen Model:** Shared Database with Row-Level Security (RLS) + Virtual Warehouses (Snowflake)

**Why This Model?**

| Aspect | Shared DB + RLS + Virtual Warehouses | Separate DB per Tenant | Separate Schema per Tenant |
|--------|--------------------------------------|------------------------|----------------------------|
| **Data Isolation** | ✅ Excellent (RLS + compute isolation) | ✅ Excellent | ✅ Excellent |
| **Cost Efficiency** | ✅ Best | ❌ Expensive | ⚠️ Moderate |
| **Operational Complexity** | ✅ Simple | ❌ Very Complex | ⚠️ Moderate |
| **Scalability** | ✅ Scales to 1000s | ⚠️ Limited to 100s | ⚠️ Limited to 100s |
| **Performance Isolation** | ✅ Virtual warehouses prevent noisy neighbors | ⚠️ Good | ⚠️ Moderate |
| **Backup/Restore** | ✅ Time Travel (90 days) | ✅ Per-tenant | ✅ Per-tenant |
| **Compliance** | ✅ Good with proper RLS | ✅ Easy to comply | ✅ Easy to comply |
| **Recommendation** | ✅ **Best for SaaS** | ❌ Only for regulated industries | ⚠️ Middle ground |

### Row-Level Security Implementation

**Concept:** Every query automatically filtered by user's tenant_id

**Implementation in Snowflake:**

```sql
-- 1. Create role for each tenant
CREATE ROLE tenant_a_role;
CREATE ROLE tenant_b_role;

-- 2. Create RLS policy using mapping table
CREATE OR REPLACE ROW ACCESS POLICY tenant_isolation
  AS (tenant_id VARCHAR)
  RETURNS BOOLEAN ->
    CASE
      WHEN CURRENT_ROLE() = 'SUPER_ADMIN' THEN TRUE
      WHEN tenant_id = CURRENT_USER() THEN TRUE  -- Assuming user = tenant_id
      ELSE FALSE
    END;

-- 3. Apply policy to tables
ALTER TABLE fact_ad_performance
  ADD ROW ACCESS POLICY tenant_isolation ON (tenant_id);

ALTER TABLE dim_campaigns
  ADD ROW ACCESS POLICY tenant_isolation ON (tenant_id);

ALTER TABLE dim_ad_groups
  ADD ROW ACCESS POLICY tenant_isolation ON (tenant_id);

-- Snowflake automatically enforces RLS on all queries!
```

**Alternative: Virtual Warehouses per Tenant (Even Better!)**

```sql
-- Create dedicated warehouse for each tenant
CREATE WAREHOUSE tenant_a_warehouse
  WITH WAREHOUSE_SIZE = 'SMALL'
       AUTO_SUSPEND = 60
       AUTO_RESUME = TRUE;

-- Tenant A's queries use their warehouse
USE WAREHOUSE tenant_a_warehouse;
SELECT * FROM fact_ad_performance WHERE tenant_id = 'tenant_a';

-- Benefits:
-- - Complete compute isolation (no noisy neighbors)
-- - Per-tenant cost tracking
-- - Per-tenant performance tuning
```

**In Application Code (FastAPI):**

```python
# Middleware to extract tenant from JWT
@app.middleware("http")
async def tenant_context_middleware(request: Request, call_next):
    user = get_user_from_jwt(request.headers.get("Authorization"))
    request.state.tenant_id = user.tenant_id

    # Option 1: Use RLS (tenant_id in WHERE clause)
    # Snowflake RLS automatically filters

    # Option 2: Use tenant-specific warehouse
    request.state.warehouse = f"tenant_{user.tenant_id}_warehouse"

    response = await call_next(request)
    return response

# In query code
async def query_snowflake(tenant_id: UUID, warehouse: str):
    conn = snowflake.connector.connect(
        user='your_user',
        account='your_account',
        warehouse=warehouse  # Use tenant's warehouse
    )

    # RLS automatically filters by tenant_id
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM fact_ad_performance
        WHERE tenant_id = %s
    """, (tenant_id,))
```

### Tenant Data Model

**Core Tables:**

```sql
-- Tenants
CREATE TABLE tenants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_name TEXT NOT NULL,
    subdomain TEXT UNIQUE,  -- e.g., "acme" -> acme.marketing-iq.com
    subscription_tier TEXT DEFAULT 'free',  -- free/pro/enterprise
    status TEXT DEFAULT 'trial',  -- trial/active/suspended/churned
    settings JSONB DEFAULT '{}',  -- {etl_schedule: "0 */8 * * *", enabled_dashboards: [...]}
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tenant Users
CREATE TABLE tenant_users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
    email TEXT NOT NULL UNIQUE,
    full_name TEXT,
    role TEXT DEFAULT 'user',  -- super_admin/tenant_admin/analyst/viewer
    auth_user_id TEXT,  -- Reference to Supabase Auth user
    is_active BOOLEAN DEFAULT TRUE,
    last_login_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tenant OAuth Connections
CREATE TABLE tenant_oauth_connections (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
    platform TEXT NOT NULL,  -- google_ads/meta/ga
    account_id TEXT,  -- Platform-specific account ID
    account_name TEXT,
    access_token_ref TEXT,  -- Reference to Azure Key Vault secret
    refresh_token_ref TEXT,
    scope TEXT,  -- OAuth scopes granted
    expires_at TIMESTAMPTZ,
    is_active BOOLEAN DEFAULT TRUE,
    last_synced_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(tenant_id, platform, account_id)
);

-- ETL Run History (per tenant)
CREATE TABLE etl_run_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
    platform TEXT NOT NULL,
    run_type TEXT,  -- incremental/full
    status TEXT,  -- running/success/failed/partial
    records_extracted INTEGER,
    records_loaded INTEGER,
    error_message TEXT,
    error_details JSONB,
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    duration_seconds INTEGER
);

-- Usage Metering (for billing)
CREATE TABLE usage_metrics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
    metric_type TEXT,  -- api_calls/etl_runs/data_volume_gb
    metric_value DECIMAL,
    period_start DATE,
    period_end DATE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### Tenant Onboarding Flow

```
┌─────────────────────────────────────────┐
│ 1. User Signup                          │
│    - Email + Password                   │
│    - Or Social Login (Google, etc.)     │
└─────────────────────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│ 2. Create Tenant                        │
│    - Company name                       │
│    - Subdomain                          │
│    - Select plan (trial/pro)            │
└─────────────────────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│ 3. Create Admin User                    │
│    - Link to tenant                     │
│    - Assign 'tenant_admin' role         │
└─────────────────────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│ 4. OAuth Connection Wizard              │
│    - Guide: Connect Google Ads          │
│      → OAuth flow                       │
│      → Store tokens in Key Vault        │
│    - Guide: Connect Meta Ads (optional) │
│    - Guide: Connect GA (optional)       │
└─────────────────────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│ 5. Configure Preferences                │
│    - Select which dashboards to enable  │
│    - Set ETL frequency (3x daily default)│
│    - Set timezone                       │
└─────────────────────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│ 6. Initial Data Sync (Backfill)        │
│    - Trigger full ETL run               │
│    - Show progress indicator            │
│    - Usually 30-90 days of history      │
└─────────────────────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│ 7. Activate Tenant                      │
│    - Status: trial → active             │
│    - Deploy scheduled ETL flows         │
│    - Send welcome email                 │
│    - Show dashboards                    │
└─────────────────────────────────────────┘
```

---

## Database Schema

### Data Warehouse Schema (Snowflake)

**Schema Design:** Star Schema with RLS + Virtual Warehouses

#### Dimension Tables

```sql
-- Date Dimension (no tenant_id - shared across all)
CREATE TABLE dim_date (
    date_key INT PRIMARY KEY,  -- YYYYMMDD format
    date DATE NOT NULL,
    day_of_week INT,  -- 1-7
    day_name VARCHAR(10),  -- Monday, Tuesday, ...
    week_of_year INT,
    month INT,
    month_name VARCHAR(10),
    quarter INT,
    year INT,
    is_weekend BIT,
    is_holiday BIT
);

-- Campaign Dimension
CREATE TABLE dim_campaigns (
    campaign_key BIGINT IDENTITY(1,1) PRIMARY KEY,
    tenant_id UNIQUEIDENTIFIER NOT NULL,  -- FOR RLS
    platform VARCHAR(50) NOT NULL,  -- google_ads, meta, ga
    campaign_id VARCHAR(255) NOT NULL,  -- Platform-specific ID
    campaign_name NVARCHAR(500),
    campaign_type VARCHAR(100),  -- Search, Display, Video, etc.
    campaign_status VARCHAR(50),  -- Active, Paused, Removed
    campaign_objective VARCHAR(100),  -- Conversions, Traffic, etc.
    budget_amount DECIMAL(18,2),
    budget_type VARCHAR(50),  -- Daily, Lifetime
    start_date DATE,
    end_date DATE,
    created_date DATE,
    updated_date DATE,
    is_current BIT DEFAULT 1,  -- For SCD Type 2
    valid_from DATETIME2 DEFAULT GETDATE(),
    valid_to DATETIME2,
    UNIQUE(tenant_id, platform, campaign_id, valid_from)
);

-- Ad Group Dimension
CREATE TABLE dim_ad_groups (
    ad_group_key BIGINT IDENTITY(1,1) PRIMARY KEY,
    tenant_id UNIQUEIDENTIFIER NOT NULL,  -- FOR RLS
    campaign_key BIGINT REFERENCES dim_campaigns(campaign_key),
    platform VARCHAR(50) NOT NULL,
    ad_group_id VARCHAR(255) NOT NULL,
    ad_group_name NVARCHAR(500),
    ad_group_type VARCHAR(100),
    ad_group_status VARCHAR(50),
    created_date DATE,
    is_current BIT DEFAULT 1,
    valid_from DATETIME2 DEFAULT GETDATE(),
    valid_to DATETIME2
);

-- Ad Dimension
CREATE TABLE dim_ads (
    ad_key BIGINT IDENTITY(1,1) PRIMARY KEY,
    tenant_id UNIQUEIDENTIFIER NOT NULL,  -- FOR RLS
    ad_group_key BIGINT REFERENCES dim_ad_groups(ad_group_key),
    platform VARCHAR(50) NOT NULL,
    ad_id VARCHAR(255) NOT NULL,
    ad_name NVARCHAR(500),
    ad_type VARCHAR(100),  -- Text, Image, Video, Carousel
    ad_status VARCHAR(50),
    headline NVARCHAR(MAX),
    description NVARCHAR(MAX),
    destination_url NVARCHAR(2000),
    created_date DATE,
    is_current BIT DEFAULT 1,
    valid_from DATETIME2 DEFAULT GETDATE(),
    valid_to DATETIME2
);

-- Geography Dimension
CREATE TABLE dim_geography (
    geography_key INT IDENTITY(1,1) PRIMARY KEY,
    country_code VARCHAR(2),
    country_name VARCHAR(100),
    region_code VARCHAR(10),
    region_name VARCHAR(100),
    city_name VARCHAR(100),
    postal_code VARCHAR(20)
);
```

#### Fact Tables

```sql
-- Fact: Ad Performance (main fact table)
CREATE TABLE fact_ad_performance (
    tenant_id UNIQUEIDENTIFIER NOT NULL,  -- FOR RLS
    date_key INT NOT NULL REFERENCES dim_date(date_key),
    campaign_key BIGINT REFERENCES dim_campaigns(campaign_key),
    ad_group_key BIGINT REFERENCES dim_ad_groups(ad_group_key),
    ad_key BIGINT REFERENCES dim_ads(ad_key),
    geography_key INT REFERENCES dim_geography(geography_key),
    platform VARCHAR(50) NOT NULL,

    -- Metrics
    impressions BIGINT DEFAULT 0,
    clicks BIGINT DEFAULT 0,
    cost DECIMAL(18,2) DEFAULT 0,
    conversions DECIMAL(18,4) DEFAULT 0,
    conversion_value DECIMAL(18,2) DEFAULT 0,
    video_views BIGINT DEFAULT 0,
    engagements BIGINT DEFAULT 0,

    -- Calculated Metrics (for performance)
    ctr DECIMAL(10,6),  -- Click-Through Rate
    cpc DECIMAL(18,2),  -- Cost Per Click
    cpm DECIMAL(18,2),  -- Cost Per Mille
    cpa DECIMAL(18,2),  -- Cost Per Acquisition
    roas DECIMAL(18,4),  -- Return on Ad Spend

    -- Metadata
    loaded_at DATETIME2 DEFAULT GETDATE(),
    etl_batch_id UNIQUEIDENTIFIER
);

-- Snowflake: No indexes needed! Auto-clustering handles it
-- Define clustering key for better performance
ALTER TABLE fact_ad_performance
  CLUSTER BY (tenant_id, date_key);

-- Snowflake automatically maintains clustering

-- Fact: Conversions (detailed conversion tracking)
CREATE TABLE fact_conversions (
    tenant_id UNIQUEIDENTIFIER NOT NULL,  -- FOR RLS
    date_key INT NOT NULL,
    campaign_key BIGINT,
    conversion_id VARCHAR(255),
    conversion_name VARCHAR(500),
    conversion_type VARCHAR(100),  -- Purchase, Lead, SignUp, etc.
    conversion_category VARCHAR(100),
    conversion_count DECIMAL(18,4),
    conversion_value DECIMAL(18,2),
    conversion_currency VARCHAR(3),
    attribution_model VARCHAR(50),  -- Last Click, Linear, etc.
    loaded_at DATETIME2 DEFAULT GETDATE()
);

-- Clustering for better query performance
ALTER TABLE fact_conversions
  CLUSTER BY (tenant_id, date_key);

-- Fact: GA Sessions (Google Analytics data)
CREATE TABLE fact_ga_sessions (
    tenant_id UNIQUEIDENTIFIER NOT NULL,  -- FOR RLS
    date_key INT NOT NULL,
    session_id VARCHAR(255),
    user_id VARCHAR(255),
    source VARCHAR(255),
    medium VARCHAR(255),
    campaign VARCHAR(255),  -- UTM campaign

    -- Session Metrics
    pageviews INT,
    session_duration_seconds INT,
    bounce_rate DECIMAL(5,2),
    is_bounce BIT,
    transactions INT,
    transaction_revenue DECIMAL(18,2),

    loaded_at DATETIME2 DEFAULT GETDATE()
);

-- Clustering for GA sessions
ALTER TABLE fact_ga_sessions
  CLUSTER BY (tenant_id, date_key);
```

#### Apply Row-Level Security

```sql
-- Apply RLS to all tenant-specific tables
CREATE SECURITY POLICY security.tenant_isolation
ADD FILTER PREDICATE security.fn_tenant_access(tenant_id)
ON dbo.fact_ad_performance,
ADD FILTER PREDICATE security.fn_tenant_access(tenant_id)
ON dbo.fact_conversions,
ADD FILTER PREDICATE security.fn_tenant_access(tenant_id)
ON dbo.fact_ga_sessions,
ADD FILTER PREDICATE security.fn_tenant_access(tenant_id)
ON dbo.dim_campaigns,
ADD FILTER PREDICATE security.fn_tenant_access(tenant_id)
ON dbo.dim_ad_groups,
ADD FILTER PREDICATE security.fn_tenant_access(tenant_id)
ON dbo.dim_ads
WITH (STATE = ON);
```

### Data Warehouse Partitioning Strategy

For 1-10TB, partitioning is essential for performance:

```sql
-- Partition fact tables by date (monthly partitions)
CREATE PARTITION FUNCTION pf_monthly (INT)
AS RANGE RIGHT FOR VALUES (
    20250101, 20250201, 20250301, 20250401,  -- 2025
    20250501, 20250601, 20250701, 20250801,
    20250901, 20251001, 20251101, 20251201
);

CREATE PARTITION SCHEME ps_monthly
AS PARTITION pf_monthly
ALL TO ([PRIMARY]);

-- Create partitioned fact table
CREATE TABLE fact_ad_performance (
    -- ... columns ...
) ON ps_monthly(date_key);
```

**Benefits:**
- Faster queries (partition elimination)
- Easier data archiving (drop old partitions)
- Better maintenance (rebuild indexes per partition)

---

## ETL Pipeline Design

### ETL Architecture Overview

```
┌──────────────────────────────────────────────────────────┐
│                   PREFECT CLOUD                          │
│                  (Orchestration)                         │
│                                                          │
│  Per Active Tenant:                                      │
│  ┌────────────────────────────────────────┐            │
│  │ Google Ads ETL Flow                    │            │
│  │   Schedule: 0 */8 * * * (3x daily)     │            │
│  │   Triggered: Scheduled + Manual        │            │
│  └────────────────────────────────────────┘            │
│  ┌────────────────────────────────────────┐            │
│  │ Meta Ads ETL Flow                      │            │
│  │   Schedule: 0 */8 * * *                │            │
│  └────────────────────────────────────────┘            │
│  ┌────────────────────────────────────────┐            │
│  │ Google Analytics ETL Flow              │            │
│  │   Schedule: 0 */8 * * *                │            │
│  └────────────────────────────────────────┘            │
└──────────────────────────────────────────────────────────┘
                      ↓
┌──────────────────────────────────────────────────────────┐
│              ETL FLOW EXECUTION                          │
│                                                          │
│  1. Extract                                              │
│     - Fetch OAuth tokens (Azure Key Vault)              │
│     - Initialize API client                             │
│     - Determine date range (incremental/full)           │
│     - Query platform API with pagination                │
│     - Handle rate limits (exp backoff)                  │
│     - Validate data quality                             │
│                                                          │
│  2. Load to Staging                                      │
│     - Upload to Azure Blob Storage                      │
│     - Format: Parquet (compressed)                      │
│     - Path: /tenant-{id}/raw/{platform}/{date}/         │
│                                                          │
│  3. Transform (DBT)                                      │
│     - Trigger DBT Cloud job                             │
│     - Run staging models                                │
│     - Run intermediate models                           │
│     - Run mart models                                   │
│     - Run data quality tests                            │
│                                                          │
│  4. Load to Warehouse                                    │
│     - DBT loads to Synapse                              │
│     - Upsert to dimension tables (SCD Type 2)           │
│     - Append/merge to fact tables                       │
│                                                          │
│  5. Post-Processing                                      │
│     - Invalidate Redis cache for tenant                 │
│     - Update etl_run_history                            │
│     - Send notification if failed                       │
│     - Update tenant.last_synced_at                      │
└──────────────────────────────────────────────────────────┘
```

### Incremental Loading Strategy

**Problem:** Don't want to re-extract all historical data every run

**Solution:** Track what's been loaded, only fetch new data

```python
async def get_date_range_for_extraction(
    tenant_id: UUID,
    platform: str,
    is_full_refresh: bool = False
) -> tuple[str, str]:
    """Determine date range to extract"""

    if is_full_refresh:
        # Full backfill (for initial sync or re-sync)
        start_date = "2023-01-01"  # Or tenant.created_at
        end_date = datetime.now().strftime("%Y-%m-%d")
    else:
        # Incremental: get last successful run date
        last_run = await db.execute(
            """
            SELECT MAX(completed_at)
            FROM etl_run_history
            WHERE tenant_id = :tenant_id
              AND platform = :platform
              AND status = 'success'
            """,
            {"tenant_id": tenant_id, "platform": platform}
        )

        if last_run:
            # Go back 7 days to catch any late conversions
            start_date = (last_run - timedelta(days=7)).strftime("%Y-%m-%d")
        else:
            # First run for this tenant
            start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

        end_date = datetime.now().strftime("%Y-%m-%d")

    return start_date, end_date
```

### Rate Limiting & Retry Logic

**Challenge:** Marketing platforms have strict API rate limits

**Google Ads API Limits:**
- 15,000 operations per day (free tier)
- 40,000 operations per day (paid tier)

**Meta Marketing API Limits:**
- 200 calls per hour per user
- Rate limit headers in response

**Solution: Exponential Backoff with Jitter**

```python
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)
import httpx

class RateLimitError(Exception):
    pass

@retry(
    retry=retry_if_exception_type((RateLimitError, httpx.TimeoutException)),
    wait=wait_exponential(multiplier=1, min=4, max=60),
    stop=stop_after_attempt(5)
)
async def call_api_with_retry(url: str, headers: dict, params: dict):
    """Call API with automatic retry on rate limits"""

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)

        # Check for rate limit
        if response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", 60))
            await asyncio.sleep(retry_after)
            raise RateLimitError("Rate limit hit, retrying...")

        response.raise_for_status()
        return response.json()
```

### Data Quality Checks

**Implement checks at multiple stages:**

1. **Extraction Stage:**
   - Schema validation (expected fields present)
   - Data type validation
   - Required fields not null
   - Date ranges make sense

2. **Transformation Stage (DBT Tests):**
   - Uniqueness tests
   - Referential integrity tests
   - Accepted values tests
   - Custom business logic tests

3. **Loading Stage:**
   - Row count validation (extracted vs loaded)
   - Sum validation (costs, conversions)
   - Anomaly detection (sudden 10x increase?)

**Example DBT Test:**

```yaml
# dbt/models/marts/fct_ad_performance.yml

version: 2

models:
  - name: fct_ad_performance
    description: "Daily ad performance metrics across all platforms"

    tests:
      - dbt_utils.unique_combination_of_columns:
          combination_of_columns:
            - tenant_id
            - date_key
            - campaign_key
            - ad_group_key
            - platform

    columns:
      - name: tenant_id
        tests:
          - not_null

      - name: impressions
        tests:
          - not_null
          - dbt_expectations.expect_column_values_to_be_between:
              min_value: 0
              max_value: 100000000

      - name: cost
        tests:
          - not_null
          - dbt_expectations.expect_column_values_to_be_between:
              min_value: 0

      - name: ctr
        tests:
          - dbt_expectations.expect_column_values_to_be_between:
              min_value: 0
              max_value: 1
              config:
                where: "impressions > 0"
```

---

## API Architecture

### API Design Principles

1. **RESTful** - Follow REST conventions
2. **Tenant-Scoped** - All endpoints filtered by tenant
3. **Filtered** - Support date ranges, campaigns, metrics
4. **Paginated** - Handle large result sets
5. **Cached** - Reduce warehouse queries
6. **Documented** - Auto-generated OpenAPI docs
7. **Versioned** - `/api/v1/` for future compatibility

### API Endpoints

#### Authentication & Tenant Management

```
POST   /auth/signup                    - User signup
POST   /auth/login                     - User login
POST   /auth/refresh                   - Refresh JWT token
POST   /auth/logout                    - Logout

GET    /tenants/me                     - Get current user's tenant info
PUT    /tenants/me                     - Update tenant settings
GET    /tenants/me/users               - List users in tenant (admin only)
POST   /tenants/me/users               - Invite user (admin only)
DELETE /tenants/me/users/{id}          - Remove user (admin only)

POST   /tenants/me/oauth/google-ads    - Connect Google Ads account
POST   /tenants/me/oauth/meta          - Connect Meta account
POST   /tenants/me/oauth/ga            - Connect GA account
GET    /tenants/me/oauth               - List connected accounts
DELETE /tenants/me/oauth/{platform}    - Disconnect account
```

#### Dashboard & Metrics APIs

```
GET    /api/v1/dashboards                          - List available dashboards
GET    /api/v1/dashboards/{id}                     - Get dashboard data
GET    /api/v1/segments/{id}/dashboards            - List dashboards in segment

GET    /api/v1/metrics                             - Unified metrics query
GET    /api/v1/campaigns                           - List campaigns
GET    /api/v1/campaigns/{id}/performance          - Campaign performance
GET    /api/v1/platforms                           - List connected platforms
```

### API Request/Response Examples

#### 1. Get Dashboard Data

**Request:**
```http
GET /api/v1/dashboards/campaign-overview?start_date=2025-01-01&end_date=2025-01-31&campaigns[]=123&campaigns[]=456
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response:**
```json
{
  "dashboard_id": "campaign-overview",
  "dashboard_name": "Campaign Overview",
  "date_range": {
    "start": "2025-01-01",
    "end": "2025-01-31"
  },
  "summary": {
    "total_impressions": 1250000,
    "total_clicks": 25000,
    "total_cost": 5000.00,
    "total_conversions": 500,
    "avg_ctr": 0.02,
    "avg_cpc": 0.20,
    "total_roas": 3.5
  },
  "campaigns": [
    {
      "campaign_id": "123",
      "campaign_name": "Spring Sale 2025",
      "platform": "google_ads",
      "impressions": 800000,
      "clicks": 16000,
      "cost": 3200.00,
      "conversions": 320,
      "ctr": 0.02,
      "cpc": 0.20,
      "roas": 3.75
    },
    {
      "campaign_id": "456",
      "campaign_name": "Brand Awareness Q1",
      "platform": "meta",
      "impressions": 450000,
      "clicks": 9000,
      "cost": 1800.00,
      "conversions": 180,
      "ctr": 0.02,
      "cpc": 0.20,
      "roas": 3.1
    }
  ],
  "time_series": [
    {
      "date": "2025-01-01",
      "impressions": 40000,
      "clicks": 800,
      "cost": 160.00,
      "conversions": 16
    },
    // ... more days
  ],
  "metadata": {
    "cached": true,
    "cached_at": "2025-01-15T10:30:00Z",
    "query_time_ms": 5
  }
}
```

#### 2. Unified Metrics Query

**Request:**
```http
GET /api/v1/metrics?metrics[]=impressions&metrics[]=clicks&metrics[]=cost&dimensions[]=date&dimensions[]=platform&start_date=2025-01-01&end_date=2025-01-31&filters={"campaign_type":"Search"}
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response:**
```json
{
  "metrics": ["impressions", "clicks", "cost"],
  "dimensions": ["date", "platform"],
  "filters": {
    "campaign_type": "Search"
  },
  "data": [
    {
      "date": "2025-01-01",
      "platform": "google_ads",
      "impressions": 25000,
      "clicks": 500,
      "cost": 100.00
    },
    {
      "date": "2025-01-01",
      "platform": "meta",
      "impressions": 15000,
      "clicks": 300,
      "cost": 60.00
    },
    // ... more rows
  ],
  "total_rows": 62,
  "metadata": {
    "query_time_ms": 45
  }
}
```

### API Implementation (FastAPI)

See "Code Examples" section below for detailed FastAPI implementation.

---

## Security & Authentication

### Multi-Layer Security

```
┌───────────────────────────────────────────────────┐
│ Layer 1: Network Security                         │
│ - HTTPS only (TLS 1.3)                           │
│ - Azure Virtual Network                          │
│ - Private endpoints for Synapse/Blob             │
└───────────────────────────────────────────────────┘
                     ↓
┌───────────────────────────────────────────────────┐
│ Layer 2: API Gateway (Future)                     │
│ - Azure API Management                            │
│ - IP whitelisting                                │
│ - DDoS protection                                │
│ - Request throttling                             │
└───────────────────────────────────────────────────┘
                     ↓
┌───────────────────────────────────────────────────┐
│ Layer 3: Application Authentication               │
│ - JWT tokens (Supabase Auth)                     │
│ - Short expiration (15 min access, 7 day refresh)│
│ - Secure token storage (httpOnly cookies)        │
└───────────────────────────────────────────────────┘
                     ↓
┌───────────────────────────────────────────────────┐
│ Layer 4: Authorization (RBAC)                     │
│ - Role-based access control                      │
│ - Tenant-scoped permissions                      │
│ - Resource-level permissions                     │
└───────────────────────────────────────────────────┘
                     ↓
┌───────────────────────────────────────────────────┐
│ Layer 5: Data Access (RLS)                        │
│ - Row-Level Security in Synapse                  │
│ - Automatic tenant filtering                     │
│ - Defense in depth (app + DB filtering)          │
└───────────────────────────────────────────────────┘
                     ↓
┌───────────────────────────────────────────────────┐
│ Layer 6: Secrets Management                       │
│ - Azure Key Vault for OAuth tokens              │
│ - Encrypted at rest                              │
│ - Audit logging                                  │
│ - Automatic rotation                             │
└───────────────────────────────────────────────────┘
```

### OAuth 2.0 Security Best Practices

**Storing Tokens Securely:**

```python
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

class TokenManager:
    def __init__(self):
        credential = DefaultAzureCredential()
        self.client = SecretClient(
            vault_url="https://marketing-iq-vault.vault.azure.net/",
            credential=credential
        )

    async def store_oauth_tokens(
        self,
        tenant_id: UUID,
        platform: str,
        access_token: str,
        refresh_token: str,
        expires_at: datetime
    ):
        """Store OAuth tokens in Key Vault"""

        # Generate secret names
        access_secret_name = f"tenant-{tenant_id}-{platform}-access"
        refresh_secret_name = f"tenant-{tenant_id}-{platform}-refresh"

        # Store tokens
        self.client.set_secret(access_secret_name, access_token)
        self.client.set_secret(refresh_secret_name, refresh_token)

        # Store reference in database (NOT the actual token)
        await db.execute(
            """
            INSERT INTO tenant_oauth_connections
            (tenant_id, platform, access_token_ref, refresh_token_ref, expires_at)
            VALUES (:tenant_id, :platform, :access_ref, :refresh_ref, :expires_at)
            ON CONFLICT (tenant_id, platform)
            DO UPDATE SET
                access_token_ref = :access_ref,
                refresh_token_ref = :refresh_ref,
                expires_at = :expires_at,
                updated_at = NOW()
            """,
            {
                "tenant_id": tenant_id,
                "platform": platform,
                "access_ref": access_secret_name,
                "refresh_ref": refresh_secret_name,
                "expires_at": expires_at
            }
        )

    async def get_access_token(self, tenant_id: UUID, platform: str) -> str:
        """Retrieve access token from Key Vault"""

        # Get reference from DB
        result = await db.fetch_one(
            """
            SELECT access_token_ref, refresh_token_ref, expires_at
            FROM tenant_oauth_connections
            WHERE tenant_id = :tenant_id AND platform = :platform
            """,
            {"tenant_id": tenant_id, "platform": platform}
        )

        if not result:
            raise ValueError(f"No OAuth connection for {platform}")

        # Check if token expired
        if result['expires_at'] < datetime.now():
            # Refresh the token
            await self.refresh_oauth_token(tenant_id, platform, result['refresh_token_ref'])
            # Recursively call to get new token
            return await self.get_access_token(tenant_id, platform)

        # Get from Key Vault
        secret = self.client.get_secret(result['access_token_ref'])
        return secret.value
```

### RBAC (Role-Based Access Control)

**Roles:**

| Role | Permissions | Use Case |
|------|-------------|----------|
| **Super Admin** | Full system access, can see all tenants | Your team only |
| **Tenant Admin** | Manage tenant settings, users, OAuth, view all dashboards | Customer's admin |
| **Analyst** | View all dashboards, export data, no admin | Customer's marketing team |
| **Viewer** | Read-only access to dashboards | Customer's executives |

**Implementation:**

```python
from enum import Enum
from functools import wraps
from fastapi import HTTPException, status

class Role(str, Enum):
    SUPER_ADMIN = "super_admin"
    TENANT_ADMIN = "tenant_admin"
    ANALYST = "analyst"
    VIEWER = "viewer"

def require_role(required_role: Role):
    """Decorator to require specific role"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, current_user=None, **kwargs):
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated"
                )

            # Check role hierarchy
            role_hierarchy = {
                Role.SUPER_ADMIN: 4,
                Role.TENANT_ADMIN: 3,
                Role.ANALYST: 2,
                Role.VIEWER: 1
            }

            if role_hierarchy.get(current_user.role, 0) < role_hierarchy.get(required_role, 999):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Requires {required_role} role"
                )

            return await func(*args, current_user=current_user, **kwargs)
        return wrapper
    return decorator

# Usage
@app.post("/tenants/me/users")
@require_role(Role.TENANT_ADMIN)
async def invite_user(
    email: str,
    role: Role,
    current_user: User = Depends(get_current_user)
):
    """Only tenant admins can invite users"""
    # ... implementation
```

---

## Implementation Plan

### MVP Timeline (8-12 Weeks)

#### Week 1-2: Foundations

**Infrastructure Setup**
- [ ] Create Azure subscription & resource groups (dev/staging/prod)
- [ ] Set up Terraform project
- [ ] Deploy Azure Synapse Serverless workspace
- [ ] Deploy Azure Blob Storage with containers
- [ ] Deploy Azure Key Vault
- [ ] Set up Supabase project
- [ ] Create Prefect Cloud account
- [ ] Create Upstash Redis instance

**Database Schemas**
- [ ] Design and create app database schema (Supabase)
  - tenants, tenant_users, tenant_oauth_connections, etl_run_history
- [ ] Design and create Snowflake schema
  - Dimension tables (dim_date, dim_campaigns, dim_ad_groups, dim_ads)
  - Fact tables (fact_ad_performance, fact_conversions)
- [ ] Implement Row-Level Security policies (Snowflake)
- [ ] Create virtual warehouses per tenant (optional)
- [ ] Create database migration system (Alembic for app DB)

**DevOps**
- [ ] Set up Git repository
- [ ] Create GitHub Actions workflows (test, deploy)
- [ ] Set up Docker & docker-compose for local dev
- [ ] Configure environment variables & secrets

#### Week 3-4: Authentication & Tenant Management

**User Authentication**
- [ ] Integrate Supabase Auth
- [ ] Implement JWT middleware in FastAPI
- [ ] Create signup/login endpoints
- [ ] Implement refresh token rotation

**Tenant Management**
- [ ] Create tenant CRUD APIs
- [ ] Create user management APIs
- [ ] Implement RBAC middleware
- [ ] Build tenant settings management

**OAuth Integration (Google Ads)**
- [ ] Register Google Cloud project
- [ ] Implement OAuth 2.0 flow
- [ ] Create OAuth callback endpoint
- [ ] Integrate with Azure Key Vault for token storage
- [ ] Implement token refresh logic

#### Week 5-7: ETL Pipeline (Google Ads Only for MVP)

**ETL Framework**
- [ ] Set up Prefect Cloud workspace
- [ ] Create base ETL flow structure
- [ ] Implement dynamic DAG generation per tenant
- [ ] Set up Azure Blob Storage loader

**Google Ads Extractor**
- [ ] Integrate Google Ads API client
- [ ] Implement campaign data extraction
- [ ] Implement ad group data extraction
- [ ] Implement performance metrics extraction
- [ ] Add pagination handling
- [ ] Add rate limit handling (exponential backoff)
- [ ] Add data validation

**DBT Setup**
- [ ] Create DBT Cloud project
- [ ] Connect to Snowflake
- [ ] Create staging models (stg_google_ads__*)
- [ ] Create intermediate models
- [ ] Create mart models for 5-8 dashboards
- [ ] Write data quality tests
- [ ] Set up DBT documentation
- [ ] Configure Snowflake-specific features (clustering, time travel)

**Orchestration**
- [ ] Deploy ETL flows to Prefect Cloud
- [ ] Implement per-tenant scheduling
- [ ] Add error handling & notifications
- [ ] Create ETL monitoring dashboard

#### Week 8-10: API Development

**API Foundation**
- [ ] Set up FastAPI project structure
- [ ] Implement database connection pooling
- [ ] Create Pydantic models
- [ ] Set up error handling framework
- [ ] Configure CORS
- [ ] Generate OpenAPI documentation

**Core Endpoints**
- [ ] GET /api/v1/dashboards (list dashboards)
- [ ] GET /api/v1/dashboards/{id} (get dashboard data)
- [ ] GET /api/v1/metrics (unified metrics query)
- [ ] GET /api/v1/campaigns (list campaigns)
- [ ] Add filtering (date ranges, campaigns, metrics)
- [ ] Add pagination
- [ ] Add sorting

**Caching Layer**
- [ ] Integrate Redis (Upstash)
- [ ] Implement cache decorator
- [ ] Create cache key strategy (tenant-aware)
- [ ] Implement cache invalidation on ETL completion
- [ ] Add cache hit/miss metrics

**Performance Optimization**
- [ ] Add database indexes
- [ ] Create materialized views for common queries
- [ ] Optimize SQL queries
- [ ] Add query result streaming for large datasets

#### Week 11: Testing

**Unit Tests**
- [ ] Test ETL extractors (mocked API responses)
- [ ] Test DBT models
- [ ] Test API endpoints
- [ ] Test authentication & authorization
- [ ] Achieve 80%+ code coverage

**Integration Tests**
- [ ] End-to-end ETL test (extract → load → transform)
- [ ] API integration tests
- [ ] OAuth flow tests

**Critical Tests**
- [ ] **Tenant isolation tests** (MUST PASS)
  - Verify tenant A cannot see tenant B's data
  - Test at API level
  - Test at database level (RLS)
- [ ] RBAC tests (verify permissions)
- [ ] Data quality tests

**Performance Tests**
- [ ] Load testing (100 concurrent users)
- [ ] Stress testing (spike in requests)
- [ ] ETL performance benchmarks

**Security Tests**
- [ ] OWASP Top 10 checks
- [ ] SQL injection testing
- [ ] XSS testing
- [ ] CSRF testing (if applicable)
- [ ] JWT token security

#### Week 12: Deployment & Launch Prep

**Production Deployment**
- [ ] Deploy to Azure Container Apps (production)
- [ ] Configure production environment variables
- [ ] Set up Azure Key Vault secrets
- [ ] Configure custom domain & SSL
- [ ] Set up Azure CDN (if needed)

**Monitoring & Observability**
- [ ] Integrate Sentry for error tracking
- [ ] Set up Azure Monitor for infrastructure
- [ ] Create custom dashboards (Grafana or Azure Dashboard)
- [ ] Configure alerts (ETL failures, API errors, high latency)
- [ ] Set up log aggregation (Better Stack)

**Documentation**
- [ ] API documentation (Swagger/Postman)
- [ ] Tenant onboarding guide
- [ ] Admin runbook
- [ ] Architecture documentation
- [ ] Disaster recovery procedures

**Pilot Launch**
- [ ] Onboard 3-5 pilot customers
- [ ] Monitor closely (24/7 for first week)
- [ ] Gather feedback
- [ ] Create feedback tracking system
- [ ] Iterate based on feedback

### Post-MVP Roadmap

#### Months 3-4: Platform Expansion
- [ ] Add Meta Ads integration
- [ ] Add Google Analytics integration
- [ ] Build remaining dashboards (up to 25)
- [ ] Implement dashboard customization

#### Months 5-6: Frontend & UX
- [ ] Build Next.js frontend
- [ ] Create dashboard UI components
- [ ] Build tenant admin panel
- [ ] Implement OAuth connection wizard
- [ ] Add data export features (CSV, Excel)

#### Months 7-9: AI & Advanced Features
- [ ] Integrate LangGraph or CrewAI
- [ ] Build multi-agent framework
- [ ] Train agents on marketing data
- [ ] Implement cross-dashboard queries
- [ ] Add predictive analytics
- [ ] Build recommendation engine

#### Ongoing: Growth & Scale
- [ ] Migrate to Azure Synapse Dedicated Pool (if needed)
- [ ] Add API gateway (Azure APIM)
- [ ] Implement white-labeling
- [ ] Add more platform integrations
- [ ] Build mobile app
- [ ] Enterprise features (SSO, advanced RBAC)

---

## Code Examples

### 1. FastAPI Application Structure

```python
# app/main.py

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from app.api import auth, tenants, dashboards, metrics
from app.core.config import settings
from app.middleware.tenant import TenantContextMiddleware
from app.middleware.auth import AuthenticationMiddleware

# Initialize Sentry
sentry_sdk.init(dsn=settings.SENTRY_DSN)

# Create FastAPI app
app = FastAPI(
    title="Marketing IQ API",
    version="1.0.0",
    description="Multi-tenant marketing analytics API",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom middleware
app.add_middleware(TenantContextMiddleware)
app.add_middleware(AuthenticationMiddleware)
app.add_middleware(SentryAsgiMiddleware)

# Exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(tenants.router, prefix="/tenants", tags=["Tenants"])
app.include_router(dashboards.router, prefix="/api/v1", tags=["Dashboards"])
app.include_router(metrics.router, prefix="/api/v1", tags=["Metrics"])

# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

### 2. Authentication Middleware

```python
# app/middleware/auth.py

from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import jwt
from app.core.config import settings
from app.models.user import User

class AuthenticationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Skip auth for public endpoints
        if request.url.path in ["/health", "/auth/login", "/auth/signup", "/api/docs"]:
            return await call_next(request)

        # Extract JWT from Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Missing or invalid authorization header"}
            )

        token = auth_header.split(" ")[1]

        try:
            # Verify JWT
            payload = jwt.decode(
                token,
                settings.JWT_SECRET,
                algorithms=["HS256"]
            )

            # Get user from database
            user = await User.get_by_id(payload["sub"])
            if not user or not user.is_active:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User not found or inactive"
                )

            # Attach user to request state
            request.state.user = user
            request.state.tenant_id = user.tenant_id

        except jwt.ExpiredSignatureError:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Token expired"}
            )
        except jwt.InvalidTokenError:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Invalid token"}
            )

        response = await call_next(request)
        return response
```

### 3. Dashboard API Endpoint

```python
# app/api/dashboards.py

from fastapi import APIRouter, Depends, Query, HTTPException
from typing import List, Optional
from datetime import date
from uuid import UUID

from app.auth import get_current_user
from app.models.user import User
from app.models.dashboard import DashboardResponse
from app.queries.dashboard import DashboardQueryService
from app.cache import cached

router = APIRouter()

@router.get("/dashboards")
async def list_dashboards(
    segment_id: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    """List available dashboards for the tenant"""
    # Implementation
    pass

@router.get("/dashboards/{dashboard_id}", response_model=DashboardResponse)
@cached(ttl=300)  # Cache for 5 minutes
async def get_dashboard(
    dashboard_id: str,
    start_date: date = Query(..., description="Start date (YYYY-MM-DD)"),
    end_date: date = Query(..., description="End date (YYYY-MM-DD)"),
    campaigns: Optional[List[str]] = Query(None, description="Filter by campaign IDs"),
    platforms: Optional[List[str]] = Query(None, description="Filter by platforms"),
    current_user: User = Depends(get_current_user)
):
    """Get dashboard data with filters"""

    # Validate date range
    if end_date < start_date:
        raise HTTPException(400, "end_date must be after start_date")

    # Query service (handles RLS automatically)
    query_service = DashboardQueryService(tenant_id=current_user.tenant_id)

    data = await query_service.get_dashboard_data(
        dashboard_id=dashboard_id,
        start_date=start_date,
        end_date=end_date,
        campaign_filters=campaigns,
        platform_filters=platforms
    )

    if not data:
        raise HTTPException(404, f"Dashboard {dashboard_id} not found")

    return data
```

### 4. Database Query Layer

```python
# app/queries/dashboard.py

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from datetime import date
from typing import List, Optional

from app.database import get_db
from app.models.warehouse import FactAdPerformance, DimCampaigns, DimDate

class DashboardQueryService:
    def __init__(self, tenant_id: UUID):
        self.tenant_id = tenant_id

    async def get_dashboard_data(
        self,
        dashboard_id: str,
        start_date: date,
        end_date: date,
        campaign_filters: Optional[List[str]] = None,
        platform_filters: Optional[List[str]] = None
    ):
        """Query warehouse for dashboard data"""

        async with get_db() as session:
            # Set tenant context for RLS
            await session.execute(
                f"EXEC sp_set_session_context 'tenant_id', '{self.tenant_id}'"
            )

            # Build query
            query = select(
                DimCampaigns.campaign_name,
                DimCampaigns.platform,
                func.sum(FactAdPerformance.impressions).label("impressions"),
                func.sum(FactAdPerformance.clicks).label("clicks"),
                func.sum(FactAdPerformance.cost).label("cost"),
                func.sum(FactAdPerformance.conversions).label("conversions"),
                (func.sum(FactAdPerformance.clicks) * 1.0 /
                 func.nullif(func.sum(FactAdPerformance.impressions), 0)).label("ctr"),
                (func.sum(FactAdPerformance.cost) /
                 func.nullif(func.sum(FactAdPerformance.clicks), 0)).label("cpc")
            ).select_from(FactAdPerformance).join(
                DimCampaigns,
                FactAdPerformance.campaign_key == DimCampaigns.campaign_key
            ).join(
                DimDate,
                FactAdPerformance.date_key == DimDate.date_key
            ).where(
                FactAdPerformance.tenant_id == self.tenant_id,  # Defense in depth
                DimDate.date >= start_date,
                DimDate.date <= end_date
            ).group_by(
                DimCampaigns.campaign_name,
                DimCampaigns.platform
            )

            # Apply filters
            if campaign_filters:
                query = query.where(DimCampaigns.campaign_id.in_(campaign_filters))

            if platform_filters:
                query = query.where(DimCampaigns.platform.in_(platform_filters))

            # Execute
            result = await session.execute(query)
            rows = result.all()

            # Format response
            return {
                "dashboard_id": dashboard_id,
                "date_range": {"start": str(start_date), "end": str(end_date)},
                "campaigns": [
                    {
                        "campaign_name": row.campaign_name,
                        "platform": row.platform,
                        "impressions": row.impressions,
                        "clicks": row.clicks,
                        "cost": float(row.cost),
                        "conversions": float(row.conversions),
                        "ctr": float(row.ctr or 0),
                        "cpc": float(row.cpc or 0)
                    }
                    for row in rows
                ]
            }
```

### 5. Prefect ETL Flow

```python
# flows/google_ads_etl.py

from prefect import flow, task
from prefect.blocks.system import Secret
from datetime import datetime, timedelta
from uuid import UUID
import pandas as pd

from extractors.google_ads import GoogleAdsExtractor
from loaders.blob import BlobLoader
from loaders.synapse import SynapseLoader
from utils.cache import invalidate_tenant_cache

@task(retries=3, retry_delay_seconds=60)
async def extract_google_ads_campaigns(tenant_id: UUID, start_date: str, end_date: str):
    """Extract campaign data from Google Ads"""

    # Get OAuth token
    token_manager = TokenManager()
    access_token = await token_manager.get_access_token(tenant_id, "google_ads")

    # Initialize extractor
    extractor = GoogleAdsExtractor(access_token)

    # Extract data
    campaigns = await extractor.get_campaigns(start_date, end_date)

    return campaigns

@task(retries=3, retry_delay_seconds=60)
async def extract_google_ads_performance(
    tenant_id: UUID,
    start_date: str,
    end_date: str,
    campaign_ids: List[str]
):
    """Extract performance metrics from Google Ads"""

    token_manager = TokenManager()
    access_token = await token_manager.get_access_token(tenant_id, "google_ads")

    extractor = GoogleAdsExtractor(access_token)

    # Extract performance data
    performance = await extractor.get_performance_report(
        start_date=start_date,
        end_date=end_date,
        campaign_ids=campaign_ids
    )

    return performance

@task
async def validate_data(data: pd.DataFrame, data_type: str):
    """Validate extracted data"""

    # Check for required columns
    required_columns = {
        "campaigns": ["campaign_id", "campaign_name", "status"],
        "performance": ["date", "campaign_id", "impressions", "clicks", "cost"]
    }

    missing = set(required_columns[data_type]) - set(data.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    # Check for nulls in critical fields
    if data_type == "performance":
        if data["impressions"].isnull().any():
            raise ValueError("Null values in impressions column")

    return True

@task
async def load_to_staging(tenant_id: UUID, data: pd.DataFrame, platform: str, data_type: str):
    """Load data to Azure Blob Storage"""

    blob_loader = BlobLoader()

    blob_path = f"tenant-{tenant_id}/raw/{platform}/{data_type}/{datetime.now().date()}/data.parquet"

    await blob_loader.upload_dataframe(data, blob_path)

    return blob_path

@task
async def trigger_dbt_transformation(tenant_id: UUID):
    """Trigger DBT transformation"""

    # Call DBT Cloud API to trigger job
    # Or run dbt locally if using DBT Core

    # For DBT Cloud:
    dbt_cloud_api = DBTCloudAPI(settings.DBT_ACCOUNT_ID, settings.DBT_API_KEY)

    job_run = await dbt_cloud_api.trigger_job(
        job_id=settings.DBT_JOB_ID,
        cause=f"Triggered by ETL for tenant {tenant_id}"
    )

    # Wait for completion
    await dbt_cloud_api.wait_for_job(job_run["id"], timeout=600)

    return job_run

@task
async def invalidate_cache_task(tenant_id: UUID):
    """Invalidate Redis cache for tenant"""
    await invalidate_tenant_cache(tenant_id)

@task
async def log_etl_run(
    tenant_id: UUID,
    platform: str,
    status: str,
    records_extracted: int,
    error: Optional[str] = None
):
    """Log ETL run to database"""

    await db.execute(
        """
        INSERT INTO etl_run_history
        (tenant_id, platform, status, records_extracted, error_message, completed_at)
        VALUES (:tenant_id, :platform, :status, :records, :error, NOW())
        """,
        {
            "tenant_id": tenant_id,
            "platform": platform,
            "status": status,
            "records": records_extracted,
            "error": error
        }
    )

@flow(name="google-ads-etl")
async def google_ads_etl_flow(
    tenant_id: UUID,
    is_incremental: bool = True,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
):
    """Main Google Ads ETL flow"""

    try:
        # Determine date range
        if not start_date:
            if is_incremental:
                start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
            else:
                start_date = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")

        if not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")

        # Extract campaigns
        campaigns_df = await extract_google_ads_campaigns(tenant_id, start_date, end_date)
        await validate_data(campaigns_df, "campaigns")

        # Extract performance
        campaign_ids = campaigns_df["campaign_id"].tolist()
        performance_df = await extract_google_ads_performance(
            tenant_id, start_date, end_date, campaign_ids
        )
        await validate_data(performance_df, "performance")

        # Load to staging
        await load_to_staging(tenant_id, campaigns_df, "google_ads", "campaigns")
        await load_to_staging(tenant_id, performance_df, "google_ads", "performance")

        # Transform (DBT)
        await trigger_dbt_transformation(tenant_id)

        # Invalidate cache
        await invalidate_cache_task(tenant_id)

        # Log success
        await log_etl_run(
            tenant_id,
            "google_ads",
            "success",
            len(performance_df)
        )

    except Exception as e:
        # Log failure
        await log_etl_run(
            tenant_id,
            "google_ads",
            "failed",
            0,
            str(e)
        )
        raise
```

### 6. DBT Transformation Model

```sql
-- dbt/models/marts/fct_ad_performance.sql

{{
  config(
    materialized='incremental',
    unique_key=['tenant_id', 'date_key', 'campaign_key', 'platform'],
    cluster_by=['tenant_id', 'date_key']
  )
}}

WITH google_ads_performance AS (
    SELECT * FROM {{ ref('stg_google_ads__performance') }}
    {% if is_incremental() %}
    WHERE loaded_at > (SELECT MAX(loaded_at) FROM {{ this }})
    {% endif %}
),

meta_performance AS (
    SELECT * FROM {{ ref('stg_meta__performance') }}
    {% if is_incremental() %}
    WHERE loaded_at > (SELECT MAX(loaded_at) FROM {{ this }})
    {% endif %}
),

combined_performance AS (
    SELECT * FROM google_ads_performance
    UNION ALL
    SELECT * FROM meta_performance
),

final AS (
    SELECT
        cp.tenant_id,
        cp.date_key,
        cp.campaign_key,
        cp.ad_group_key,
        cp.ad_key,
        cp.platform,

        -- Metrics
        SUM(cp.impressions) AS impressions,
        SUM(cp.clicks) AS clicks,
        SUM(cp.cost) AS cost,
        SUM(cp.conversions) AS conversions,
        SUM(cp.conversion_value) AS conversion_value,

        -- Calculated metrics
        CASE
            WHEN SUM(cp.impressions) > 0
            THEN SUM(cp.clicks) * 1.0 / SUM(cp.impressions)
            ELSE 0
        END AS ctr,

        CASE
            WHEN SUM(cp.clicks) > 0
            THEN SUM(cp.cost) / SUM(cp.clicks)
            ELSE 0
        END AS cpc,

        CASE
            WHEN SUM(cp.impressions) > 0
            THEN SUM(cp.cost) / (SUM(cp.impressions) / 1000.0)
            ELSE 0
        END AS cpm,

        CASE
            WHEN SUM(cp.conversions) > 0
            THEN SUM(cp.cost) / SUM(cp.conversions)
            ELSE 0
        END AS cpa,

        CASE
            WHEN SUM(cp.cost) > 0
            THEN SUM(cp.conversion_value) / SUM(cp.cost)
            ELSE 0
        END AS roas,

        CURRENT_TIMESTAMP AS loaded_at

    FROM combined_performance cp
    GROUP BY
        cp.tenant_id,
        cp.date_key,
        cp.campaign_key,
        cp.ad_group_key,
        cp.ad_key,
        cp.platform
)

SELECT * FROM final
```

---

## Testing Strategy

### Testing Pyramid

```
         /\
        /  \  E2E Tests (5%)
       /────\
      /      \  Integration Tests (15%)
     /────────\
    /          \  Unit Tests (80%)
   /────────────\
```

### Test Categories

#### 1. Unit Tests (80% of tests)

**What to test:**
- Individual functions
- Data transformations
- Business logic
- Utilities

**Example:**

```python
# tests/test_metrics_calculation.py

import pytest
from app.utils.metrics import calculate_ctr, calculate_roas

def test_calculate_ctr():
    """Test CTR calculation"""
    assert calculate_ctr(clicks=100, impressions=1000) == 0.10
    assert calculate_ctr(clicks=0, impressions=1000) == 0.0
    assert calculate_ctr(clicks=100, impressions=0) == 0.0  # Avoid division by zero

def test_calculate_roas():
    """Test ROAS calculation"""
    assert calculate_roas(revenue=1000, cost=250) == 4.0
    assert calculate_roas(revenue=0, cost=100) == 0.0
    assert calculate_roas(revenue=100, cost=0) == 0.0
```

#### 2. Integration Tests (15% of tests)

**What to test:**
- API endpoints
- Database queries
- ETL flows
- External API integrations (mocked)

**Example:**

```python
# tests/integration/test_dashboard_api.py

import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_get_dashboard_success(test_tenant, test_user_token):
    """Test successful dashboard retrieval"""

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get(
            "/api/v1/dashboards/campaign-overview",
            headers={"Authorization": f"Bearer {test_user_token}"},
            params={
                "start_date": "2025-01-01",
                "end_date": "2025-01-31"
            }
        )

        assert response.status_code == 200
        data = response.json()

        assert "dashboard_id" in data
        assert data["dashboard_id"] == "campaign-overview"
        assert "campaigns" in data
        assert isinstance(data["campaigns"], list)

@pytest.mark.asyncio
async def test_get_dashboard_invalid_date_range(test_user_token):
    """Test dashboard with invalid date range"""

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get(
            "/api/v1/dashboards/campaign-overview",
            headers={"Authorization": f"Bearer {test_user_token}"},
            params={
                "start_date": "2025-01-31",
                "end_date": "2025-01-01"  # End before start
            }
        )

        assert response.status_code == 400
```

#### 3. **CRITICAL: Tenant Isolation Tests**

**These tests MUST pass before production deployment**

```python
# tests/integration/test_tenant_isolation.py

import pytest
from httpx import AsyncClient
from app.main import app
from tests.fixtures import create_test_tenant, create_test_data

@pytest.mark.asyncio
async def test_tenant_cannot_access_other_tenant_data():
    """CRITICAL: Ensure tenant A cannot see tenant B's data"""

    # Create two tenants with data
    tenant_a = await create_test_tenant("Tenant A")
    tenant_b = await create_test_tenant("Tenant B")

    # Create distinct data for each
    await create_test_data(tenant_a.id, campaigns=["A1", "A2"])
    await create_test_data(tenant_b.id, campaigns=["B1", "B2"])

    # Get tokens for each tenant's users
    token_a = await get_test_token(tenant_a.id)
    token_b = await get_test_token(tenant_b.id)

    async with AsyncClient(app=app, base_url="http://test") as client:
        # Tenant A requests dashboard
        response_a = await client.get(
            "/api/v1/dashboards/campaign-overview",
            headers={"Authorization": f"Bearer {token_a}"},
            params={"start_date": "2025-01-01", "end_date": "2025-01-31"}
        )

        # Tenant B requests dashboard
        response_b = await client.get(
            "/api/v1/dashboards/campaign-overview",
            headers={"Authorization": f"Bearer {token_b}"},
            params={"start_date": "2025-01-01", "end_date": "2025-01-31"}
        )

        data_a = response_a.json()
        data_b = response_b.json()

        # Extract campaign IDs
        campaigns_a = [c["campaign_id"] for c in data_a["campaigns"]]
        campaigns_b = [c["campaign_id"] for c in data_b["campaigns"]]

        # CRITICAL ASSERTION: No overlap
        assert set(campaigns_a) & set(campaigns_b) == set()
        assert "A1" in campaigns_a and "A2" in campaigns_a
        assert "B1" in campaigns_b and "B2" in campaigns_b
        assert "B1" not in campaigns_a
        assert "A1" not in campaigns_b

@pytest.mark.asyncio
async def test_database_rls_enforcement():
    """Test Row-Level Security at database level"""

    # Create two tenants
    tenant_a_id = UUID("00000000-0000-0000-0000-000000000001")
    tenant_b_id = UUID("00000000-0000-0000-0000-000000000002")

    # Insert data for both tenants
    await db.execute(
        """
        INSERT INTO fact_ad_performance (tenant_id, date_key, impressions)
        VALUES
            (:tenant_a, 20250101, 1000),
            (:tenant_b, 20250101, 2000)
        """,
        {"tenant_a": tenant_a_id, "tenant_b": tenant_b_id}
    )

    # Set session context to tenant A
    await db.execute(f"EXEC sp_set_session_context 'tenant_id', '{tenant_a_id}'")

    # Query should only return tenant A data
    result = await db.fetch_all("SELECT * FROM fact_ad_performance")

    assert len(result) == 1
    assert result[0]["tenant_id"] == tenant_a_id
    assert result[0]["impressions"] == 1000
```

#### 4. Load & Performance Tests

```python
# tests/performance/test_load.py

import pytest
from locust import HttpUser, task, between

class DashboardUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        """Login and get token"""
        response = self.client.post("/auth/login", json={
            "email": "test@example.com",
            "password": "testpass"
        })
        self.token = response.json()["access_token"]

    @task(3)
    def get_dashboard(self):
        """Get dashboard (most common operation)"""
        self.client.get(
            "/api/v1/dashboards/campaign-overview",
            headers={"Authorization": f"Bearer {self.token}"},
            params={"start_date": "2025-01-01", "end_date": "2025-01-31"}
        )

    @task(1)
    def get_metrics(self):
        """Query metrics"""
        self.client.get(
            "/api/v1/metrics",
            headers={"Authorization": f"Bearer {self.token}"},
            params={
                "metrics[]": ["impressions", "clicks"],
                "dimensions[]": ["date"],
                "start_date": "2025-01-01",
                "end_date": "2025-01-31"
            }
        )

# Run: locust -f tests/performance/test_load.py --host=http://localhost:8000
```

**Performance Targets:**
- API response time: p95 < 500ms
- Dashboard load time: p95 < 2 seconds
- Support 100 concurrent users
- ETL processing: < 10 minutes for 1 million records

---

## Deployment & DevOps

### CI/CD Pipeline

```yaml
# .github/workflows/ci-cd.yml

name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  AZURE_REGISTRY: marketingiq.azurecr.io
  IMAGE_NAME: marketing-iq-api

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

      redis:
        image: redis:7
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Cache dependencies
        uses: actions/cache@v3
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt

      - name: Run linter
        run: |
          flake8 app tests
          black --check app tests
          isort --check app tests

      - name: Run type checker
        run: mypy app

      - name: Run tests
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost/test
          REDIS_URL: redis://localhost:6379
        run: |
          pytest tests/ -v --cov=app --cov-report=xml --cov-report=term

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml

  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'

    steps:
      - uses: actions/checkout@v3

      - name: Login to Azure Container Registry
        uses: azure/docker-login@v1
        with:
          login-server: ${{ env.AZURE_REGISTRY }}
          username: ${{ secrets.AZURE_REGISTRY_USERNAME }}
          password: ${{ secrets.AZURE_REGISTRY_PASSWORD }}

      - name: Build and push Docker image
        run: |
          docker build -t ${{ env.AZURE_REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }} .
          docker push ${{ env.AZURE_REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}

          docker tag ${{ env.AZURE_REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }} \
                     ${{ env.AZURE_REGISTRY }}/${{ env.IMAGE_NAME }}:latest
          docker push ${{ env.AZURE_REGISTRY }}/${{ env.IMAGE_NAME }}:latest

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'

    steps:
      - uses: actions/checkout@v3

      - name: Login to Azure
        uses: azure/login@v1
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}

      - name: Deploy to Azure Container Apps
        run: |
          az containerapp update \
            --name marketing-iq-api \
            --resource-group marketing-iq-prod \
            --image ${{ env.AZURE_REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}

      - name: Run database migrations
        run: |
          # Run Alembic migrations
          az containerapp exec \
            --name marketing-iq-api \
            --resource-group marketing-iq-prod \
            --command "alembic upgrade head"

      - name: Notify Sentry of deployment
        run: |
          curl https://sentry.io/api/0/organizations/marketing-iq/releases/ \
            -X POST \
            -H "Authorization: Bearer ${{ secrets.SENTRY_AUTH_TOKEN }}" \
            -H "Content-Type: application/json" \
            -d "{\"version\": \"${{ github.sha }}\", \"projects\": [\"marketing-iq-api\"]}"
```

### Infrastructure as Code (Terraform)

```hcl
# terraform/main.tf

terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }

  backend "azurerm" {
    resource_group_name  = "terraform-state"
    storage_account_name = "marketingiqtfstate"
    container_name       = "tfstate"
    key                  = "prod.terraform.tfstate"
  }
}

provider "azurerm" {
  features {}
}

# Resource Group
resource "azurerm_resource_group" "main" {
  name     = "marketing-iq-${var.environment}"
  location = var.location

  tags = {
    Environment = var.environment
    Project     = "marketing-iq"
  }
}

# Azure Synapse Workspace
resource "azurerm_synapse_workspace" "main" {
  name                                 = "marketing-iq-synapse-${var.environment}"
  resource_group_name                  = azurerm_resource_group.main.name
  location                             = azurerm_resource_group.main.location
  storage_data_lake_gen2_filesystem_id = azurerm_storage_data_lake_gen2_filesystem.main.id

  sql_administrator_login          = var.sql_admin_login
  sql_administrator_login_password = var.sql_admin_password

  identity {
    type = "SystemAssigned"
  }
}

# Storage Account
resource "azurerm_storage_account" "main" {
  name                     = "marketingiq${var.environment}"
  resource_group_name      = azurerm_resource_group.main.name
  location                 = azurerm_resource_group.main.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  is_hns_enabled           = true
}

# Container Apps Environment
resource "azurerm_container_app_environment" "main" {
  name                = "marketing-iq-env-${var.environment}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
}

# Container App (API)
resource "azurerm_container_app" "api" {
  name                         = "marketing-iq-api"
  container_app_environment_id = azurerm_container_app_environment.main.id
  resource_group_name          = azurerm_resource_group.main.name
  revision_mode                = "Single"

  template {
    container {
      name   = "api"
      image  = "${var.acr_name}.azurecr.io/marketing-iq-api:latest"
      cpu    = 1.0
      memory = "2Gi"

      env {
        name  = "DATABASE_URL"
        value = var.database_url
      }

      env {
        name        = "JWT_SECRET"
        secret_name = "jwt-secret"
      }
    }

    min_replicas = 2
    max_replicas = 10
  }

  ingress {
    external_enabled = true
    target_port      = 8000

    traffic_weight {
      percentage      = 100
      latest_revision = true
    }
  }

  secret {
    name  = "jwt-secret"
    value = var.jwt_secret
  }
}

# Key Vault
resource "azurerm_key_vault" "main" {
  name                = "marketing-iq-kv-${var.environment}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  tenant_id           = data.azurerm_client_config.current.tenant_id
  sku_name            = "standard"

  access_policy {
    tenant_id = data.azurerm_client_config.current.tenant_id
    object_id = azurerm_container_app.api.identity[0].principal_id

    secret_permissions = [
      "Get",
      "List"
    ]
  }
}

# Redis Cache
resource "azurerm_redis_cache" "main" {
  name                = "marketing-iq-redis-${var.environment}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  capacity            = 1
  family              = "C"
  sku_name            = "Standard"
  enable_non_ssl_port = false
  minimum_tls_version = "1.2"
}
```

---

## Cost Analysis

### Monthly Cost Breakdown (10 Active Tenants)

#### MVP Phase (Months 1-3)

| Service | Configuration | Monthly Cost | Notes |
|---------|---------------|--------------|-------|
| **Azure Synapse Serverless** | Pay-per-query | $500 - $1,500 | Highly variable, depends on query volume |
| **Azure Blob Storage** | 500GB Standard LRS | $10 | Raw data staging |
| **Azure Container Apps** | 2 vCPU, 4GB RAM, 2 replicas | $150 | API hosting |
| **Azure Key Vault** | 1,000 operations/day | $5 | Secrets management |
| **Supabase** | Pro plan | $25 | App database + auth |
| **Prefect Cloud** | Free tier | $0 | ETL orchestration |
| **Upstash Redis** | 10GB serverless | $30 | Caching |
| **Sentry** | Team plan | $26 | Error tracking |
| **DBT Cloud** | Team plan | $100 | Data transformations |
| **Better Stack** | Basic plan | $20 | Logging |
| **Domain & SSL** | Azure custom domain | $10 | DNS + SSL cert |
| **Azure Monitor** | Basic | $50 | Monitoring & alerts |
| **Bandwidth** | Estimate | $50 | Data transfer |
| **TOTAL (MVP)** | | **$976 - $1,976/month** | |

#### Scale Phase (50+ Tenants, 5-10TB Data)

| Service | Configuration | Monthly Cost | Notes |
|---------|---------------|--------------|-------|
| **Azure Synapse Dedicated** | DW500c (8 hrs/day) | $2,500 | Warehouse compute |
| **Azure Blob Storage** | 5TB Premium | $200 | Increased data volume |
| **Azure Container Apps** | 4 vCPU, 8GB RAM, 5 replicas | $400 | Scaled API hosting |
| **Azure Key Vault** | 10,000 operations/day | $10 | More tenants = more secrets |
| **Supabase** | Pro plan | $25 | App database |
| **Prefect Cloud** | Standard plan | $150 | More ETL flows |
| **Azure Redis Premium** | P1 (6GB cluster) | $250 | Production caching |
| **Sentry** | Business plan | $80 | More error volume |
| **DBT Cloud** | Team plan | $100 | Data transformations |
| **Better Stack** | Professional | $50 | More log volume |
| **Azure API Management** | Developer tier | $50 | Added API gateway |
| **Azure Monitor** | Standard | $150 | Advanced monitoring |
| **Bandwidth** | Estimate | $200 | Increased data transfer |
| **TOTAL (Scale)** | | **$4,165/month** | |

### Cost Optimization Strategies

1. **Synapse Optimization:**
   - Use serverless SQL pool for exploratory queries
   - Pause dedicated pool when not in use
   - Implement query result caching
   - Use materialized views for common aggregations

2. **Storage Optimization:**
   - Archive old data to Cool/Archive tier
   - Use Parquet compression
   - Implement data retention policies (e.g., keep raw data for 90 days)

3. **Compute Optimization:**
   - Use Azure Container Apps auto-scaling
   - Right-size container resources based on metrics
   - Implement API response caching (reduce DB queries)

4. **Bandwidth Optimization:**
   - Use Azure CDN for static assets
   - Implement pagination for large result sets
   - Compress API responses (gzip)

### Revenue Model Considerations

To be profitable, pricing should consider:

**Cost per Tenant (at scale):**
- Infrastructure: ~$80/tenant/month
- Support overhead: ~$20/tenant/month
- **Total Cost: ~$100/tenant/month**

**Suggested Pricing Tiers:**

| Tier | Price/Month | Dashboards | ETL Frequency | API Calls/Month | Margin |
|------|-------------|------------|---------------|-----------------|--------|
| **Free** | $0 | 3 | Daily | 1,000 | Loss leader |
| **Starter** | $199 | 10 | 3x daily | 10,000 | 50% margin |
| **Professional** | $499 | 25 | Hourly | 50,000 | 80% margin |
| **Enterprise** | $1,499+ | Unlimited | Real-time | Unlimited | 93% margin |

---

## Risks & Mitigations

### Technical Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| **Data Isolation Bug** | Low | CRITICAL | - Rigorous tenant isolation testing<br>- Code reviews<br>- Penetration testing<br>- RLS at DB + app level |
| **API Rate Limits** (Google/Meta) | High | High | - Exponential backoff<br>- Spread requests over time<br>- Monitor quota usage<br>- Multiple API keys if needed |
| **Cost Overrun** | Low | Medium | - Daily cost monitoring<br>- Snowflake resource monitors<br>- Auto-suspend warehouses<br>- Pay-per-second billing |
| **Performance Issues** | Medium | Medium | - Load testing before launch<br>- Caching layer<br>- Query optimization<br>- Materialized views |
| **OAuth Token Expiry** | Medium | Medium | - Automated refresh<br>- Alerting on failures<br>- Graceful degradation |
| **Data Quality Issues** | Medium | Medium | - DBT tests<br>- Anomaly detection<br>- Manual spot checks<br>- Customer alerts |
| **Query Performance** | Low | Medium | - Snowflake auto-clustering<br>- Virtual warehouses<br>- Caching<br>- Query optimization |
| **ETL Failures** | Medium | Medium | - Retry logic<br>- Error notifications<br>- Monitoring<br>- SLA tracking |

### Business Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| **Low Customer Adoption** | Medium | CRITICAL | - Focus on pilot customers<br>- Gather feedback early<br>- Iterate quickly<br>- Prove value |
| **High Churn Rate** | Medium | High | - Excellent onboarding<br>- Proactive support<br>- Regular check-ins<br>- Feature requests |
| **Platform API Changes** | Medium | Medium | - Monitor API changelogs<br>- Maintain API version flexibility<br>- Automated tests |
| **Competitor Launch** | Medium | Medium | - Move fast<br>- Differentiate with AI<br>- Focus on UX |
| **Team Burnout** | Medium | High | - Realistic timelines<br>- Avoid over-engineering<br>- Use managed services |

### Security Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| **Data Breach** | Low | CRITICAL | - Encryption at rest & transit<br>- Regular security audits<br>- Penetration testing<br>- SOC 2 compliance (future) |
| **SQL Injection** | Low | High | - Parameterized queries<br>- ORM usage<br>- Input validation<br>- Security scanning |
| **XSS Attacks** | Low | Medium | - Content Security Policy<br>- Input sanitization<br>- React (auto-escapes) |
| **DDoS Attack** | Medium | Medium | - Azure DDoS Protection<br>- Rate limiting<br>- API gateway |
| **Credential Theft** | Medium | High | - Key Vault for secrets<br>- No credentials in code<br>- Rotate secrets regularly |

---

## Conclusion

### Summary

This document outlines a **comprehensive, production-ready architecture** for Marketing IQ, a multi-tenant SaaS marketing analytics platform. The architecture is designed for a **3-5 person startup team** to build and launch an **MVP in 8-12 weeks**.

### Key Takeaways

1. **Multi-Tenant from Day 1** - Shared database with Row-Level Security
2. **Start Lean** - 5-8 dashboards for MVP, not all 25
3. **Managed Services** - Prioritize speed over cost for MVP
4. **Security First** - Tenant isolation, encryption, RBAC
5. **Scalable Foundation** - Can grow to 100s of tenants without rewrite
6. **Cost-Conscious** - Start at ~$1K/month, scale to $4-5K

### Critical Success Factors

✅ **Tenant Isolation** - Must be bulletproof
✅ **Performance** - < 2 sec dashboard loads
✅ **Reliability** - > 99% ETL success rate
✅ **Cost Management** - Stay within budget
✅ **Speed to Market** - Launch in 8-12 weeks
✅ **Customer Validation** - Get 3-5 paying pilots

### Next Steps

1. ✅ **Review & approve this plan**
2. Set up Azure accounts & subscriptions
3. Initialize Git repository
4. Begin Week 1: Infrastructure setup
5. Start building!

---

**Document Version:** 1.0
**Last Updated:** 2025-01-23
**Author:** Architecture Team
**Status:** Ready for Implementation
