# Marketing IQ - System Architecture

**Version:** 1.0 (Simplified for 1-3 Clients)
**Last Updated:** 2025-01-24
**Tech Stack:** Python + Snowflake + Azure + FastAPI

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         DATA SOURCES                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐     │
│  │ Google Ads   │  │  Meta Ads    │  │  Google Analytics    │     │
│  │  (Client 1)  │  │  (Client 1)  │  │     (Client 1)       │     │
│  │  (Client 2)  │  │  (Client 2)  │  │     (Client 2)       │     │
│  │  (Client 3)  │  │  (Client 3)  │  │     (Client 3)       │     │
│  └──────────────┘  └──────────────┘  └──────────────────────┘     │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              │ OAuth 2.0 Authentication
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    EXTRACTION LAYER (Python ETL)                     │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │  Python Scripts (Scheduled via Cron / Manual Trigger)       │  │
│  │                                                              │  │
│  │  • etl_google_ads.py                                        │  │
│  │  • etl_meta_ads.py                                          │  │
│  │  • etl_google_analytics.py                                  │  │
│  │                                                              │  │
│  │  Features:                                                   │  │
│  │  - OAuth token refresh (Azure Key Vault)                    │  │
│  │  - Rate limiting & retry logic                              │  │
│  │  - Incremental data extraction                              │  │
│  │  - Data validation                                           │  │
│  └─────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              │ Raw JSON/Parquet Files
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      STAGING LAYER (Azure)                           │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │           Azure Blob Storage (Raw Data)                      │  │
│  │                                                              │  │
│  │  Path Structure:                                             │  │
│  │  /tenant-{client_id}/raw/google_ads/2025-01-24/             │  │
│  │  /tenant-{client_id}/raw/meta_ads/2025-01-24/               │  │
│  │  /tenant-{client_id}/raw/ga/2025-01-24/                     │  │
│  │                                                              │  │
│  │  Cost: ~$0.20/month (10GB)                                   │  │
│  └─────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              │ Trigger DBT
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   TRANSFORMATION LAYER (DBT)                         │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │                   DBT Cloud (Free Tier)                      │  │
│  │                                                              │  │
│  │  SQL Transformations:                                        │  │
│  │                                                              │  │
│  │  1. Staging Layer:                                           │  │
│  │     • Parse raw JSON → structured tables                     │  │
│  │     • Standardize field names across platforms               │  │
│  │     • Convert units (micros → dollars)                       │  │
│  │                                                              │  │
│  │  2. Intermediate Layer:                                      │  │
│  │     • Join campaigns across platforms                        │  │
│  │     • Calculate derived metrics (CTR, CPC, ROAS)             │  │
│  │                                                              │  │
│  │  3. Mart Layer (Dashboard Tables):                           │  │
│  │     • fact_ad_performance                                    │  │
│  │     • dim_campaigns                                          │  │
│  │     • dim_date                                               │  │
│  │                                                              │  │
│  │  Cost: FREE                                                  │  │
│  └─────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              │ Insert/Update Data
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   DATA WAREHOUSE (Snowflake)                         │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │              Snowflake X-Small Warehouse                     │  │
│  │                                                              │  │
│  │  Fact Tables:                                                │  │
│  │  ┌────────────────────────────────────────────┐            │  │
│  │  │  fact_ad_performance                       │            │  │
│  │  │  - tenant_id, date, campaign_key           │            │  │
│  │  │  - impressions, clicks, cost, conversions  │            │  │
│  │  │  - ctr, cpc, cpa, roas                     │            │  │
│  │  └────────────────────────────────────────────┘            │  │
│  │                                                              │  │
│  │  Dimension Tables:                                           │  │
│  │  ┌────────────────────────────────────────────┐            │  │
│  │  │  dim_campaigns                             │            │  │
│  │  │  - tenant_id, platform, campaign_id        │            │  │
│  │  │  - campaign_name, type, status, budget     │            │  │
│  │  └────────────────────────────────────────────┘            │  │
│  │                                                              │  │
│  │  ┌────────────────────────────────────────────┐            │  │
│  │  │  dim_date                                  │            │  │
│  │  │  - date, day_of_week, month, quarter, year │            │  │
│  │  └────────────────────────────────────────────┘            │  │
│  │                                                              │  │
│  │  Security:                                                   │  │
│  │  • Row-Level Security (RLS) by tenant_id                    │  │
│  │  • Auto-clustering on (tenant_id, date)                     │  │
│  │                                                              │  │
│  │  Cost: $17/month (50GB storage + 30min/day compute)         │  │
│  └─────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              │ SQL Queries
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        API LAYER (FastAPI)                           │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │         Azure Container Apps (Python + FastAPI)              │  │
│  │                                                              │  │
│  │  REST API Endpoints:                                         │  │
│  │                                                              │  │
│  │  Authentication:                                             │  │
│  │  • POST   /auth/signup                                       │  │
│  │  • POST   /auth/login                                        │  │
│  │  • POST   /auth/refresh                                      │  │
│  │                                                              │  │
│  │  Tenant Management:                                          │  │
│  │  • GET    /tenants/me                                        │  │
│  │  • POST   /tenants/me/oauth/google-ads                       │  │
│  │  • POST   /tenants/me/oauth/meta                             │  │
│  │  • POST   /tenants/me/oauth/ga                               │  │
│  │                                                              │  │
│  │  Dashboards & Metrics:                                       │  │
│  │  • GET    /api/v1/dashboards                                 │  │
│  │  • GET    /api/v1/dashboards/{id}                            │  │
│  │  • GET    /api/v1/metrics                                    │  │
│  │  • GET    /api/v1/campaigns                                  │  │
│  │  • GET    /api/v1/campaigns/{id}/performance                 │  │
│  │                                                              │  │
│  │  Features:                                                   │  │
│  │  • JWT Authentication                                        │  │
│  │  • Tenant Isolation (RLS)                                    │  │
│  │  • Request Validation                                        │  │
│  │  • Response Caching (Redis)                                  │  │
│  │  • Auto-generated OpenAPI docs                               │  │
│  │                                                              │  │
│  │  Cost: $30/month                                             │  │
│  └─────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              │ HTTPS/JSON
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     CONSUMPTION LAYER (Future)                       │
│                                                                      │
│  ┌──────────────────────────┐  ┌──────────────────────────────┐   │
│  │  Next.js Frontend        │  │  Agentic AI Framework        │   │
│  │  (Phase 2)               │  │  (Phase 3)                   │   │
│  │                          │  │                              │   │
│  │  • Dashboard UI          │  │  • LangGraph / CrewAI        │   │
│  │  • Admin Panel           │  │  • Natural language queries  │   │
│  │  • OAuth Wizard          │  │  • Predictive analytics      │   │
│  │  • Data Export           │  │  • Recommendations           │   │
│  └──────────────────────────┘  └──────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Supporting Services

```
┌─────────────────────────────────────────────────────────────────────┐
│                      AZURE SERVICES                                  │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │  Azure Key Vault ($2/month)                                │    │
│  │  • OAuth tokens (Google Ads, Meta, GA)                     │    │
│  │  • API secrets                                              │    │
│  │  • Database credentials                                     │    │
│  └────────────────────────────────────────────────────────────┘    │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │  Azure Container Registry ($5/month)                       │    │
│  │  • Docker images for FastAPI                               │    │
│  └────────────────────────────────────────────────────────────┘    │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │  Azure Monitor ($5/month)                                  │    │
│  │  • Infrastructure logs                                      │    │
│  │  • Performance metrics                                      │    │
│  │  • Alerts                                                   │    │
│  └────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                    APPLICATION DATABASE                              │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │  Supabase (PostgreSQL) - FREE                              │    │
│  │                                                             │    │
│  │  Tables:                                                    │    │
│  │  • tenants (clients)                                        │    │
│  │  • tenant_users (marketing team members)                    │    │
│  │  • tenant_oauth_connections (platform credentials)          │    │
│  │  • etl_run_history (job logs)                              │    │
│  │                                                             │    │
│  │  500MB storage - sufficient for 1-3 clients                │    │
│  └────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                         CACHING LAYER                                │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │  Upstash Redis (Serverless) - FREE                         │    │
│  │                                                             │    │
│  │  • API response caching                                     │    │
│  │  • 5-minute TTL                                             │    │
│  │  • 10K commands/day free tier                              │    │
│  │                                                             │    │
│  │  Cache Keys:                                                │    │
│  │  • dashboard:{tenant_id}:{dashboard_id}:{params}            │    │
│  │  • campaigns:{tenant_id}:{date_range}                       │    │
│  └────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                      MONITORING & ERRORS                             │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │  Sentry (Error Tracking) - FREE                            │    │
│  │  • Application errors                                       │    │
│  │  • Performance monitoring                                   │    │
│  │  • 5K events/month                                          │    │
│  └────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                       CI/CD PIPELINE                                 │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │  GitHub Actions - FREE                                     │    │
│  │                                                             │    │
│  │  Workflows:                                                 │    │
│  │  • Run tests on PR                                          │    │
│  │  • Build Docker image                                       │    │
│  │  • Push to Azure Container Registry                        │    │
│  │  • Deploy to Azure Container Apps                          │    │
│  │                                                             │    │
│  │  2000 free minutes/month                                    │    │
│  └────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Data Flow (Step-by-Step)

```
1. CLIENT ONBOARDING
   ↓
   Marketing person logs in → Connects Google Ads/Meta/GA via OAuth
   ↓
   OAuth tokens stored in Azure Key Vault (encrypted)

2. DATA EXTRACTION (Daily at 6am, 2pm, 10pm)
   ↓
   Python ETL script runs (cron job)
   ↓
   Fetches data from Google Ads/Meta/GA APIs
   ↓
   Saves raw JSON files to Azure Blob Storage

3. DATA TRANSFORMATION (After extraction)
   ↓
   DBT Cloud runs transformations
   ↓
   Parses JSON → Clean tables
   ↓
   Standardizes metrics across platforms
   ↓
   Calculates derived metrics (CTR, CPC, ROAS)

4. DATA LOADING
   ↓
   DBT loads clean data into Snowflake
   ↓
   Updates fact_ad_performance table
   ↓
   Updates dimension tables (campaigns, dates)

5. API CONSUMPTION
   ↓
   User requests dashboard data via API
   ↓
   FastAPI checks Redis cache (if fresh, return cached)
   ↓
   If not cached: Query Snowflake (with RLS filtering)
   ↓
   Cache response in Redis (5 min TTL)
   ↓
   Return JSON response

6. FUTURE: FRONTEND/AI
   ↓
   Next.js dashboard calls FastAPI
   ↓
   OR AI agent queries data via API
   ↓
   All data access goes through consistent API layer
```

---

## Security Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                          SECURITY LAYERS                             │
│                                                                      │
│  Layer 1: Network Security                                          │
│  • HTTPS only (TLS 1.3)                                             │
│  • Azure Virtual Network                                            │
│                                                                      │
│  Layer 2: Authentication                                            │
│  • JWT tokens (15 min expiry)                                       │
│  • Refresh tokens (7 day expiry)                                    │
│  • Supabase Auth                                                    │
│                                                                      │
│  Layer 3: Authorization                                             │
│  • Role-Based Access Control (RBAC)                                 │
│  • Roles: Tenant Admin, Analyst, Viewer                             │
│                                                                      │
│  Layer 4: Data Access                                               │
│  • Row-Level Security (RLS) in Snowflake                            │
│  • Automatic tenant_id filtering                                    │
│  • Defense in depth (app + DB filtering)                            │
│                                                                      │
│  Layer 5: Secrets Management                                        │
│  • Azure Key Vault for OAuth tokens                                 │
│  • Encrypted at rest                                                │
│  • Audit logging enabled                                            │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Cost Summary (Monthly)

```
┌────────────────────────────────────────┬─────────────────┐
│ SERVICE                                │ MONTHLY COST    │
├────────────────────────────────────────┼─────────────────┤
│ Snowflake (50GB + 30min/day)           │ $17             │
│ Azure Container Apps (FastAPI)         │ $30             │
│ Azure Blob Storage (10GB)              │ $0.20           │
│ Azure Key Vault (OAuth tokens)         │ $2              │
│ Azure Monitor (logs)                   │ $5              │
│ Azure Container Registry (images)      │ $5              │
│ Supabase (app database)                │ FREE            │
│ Upstash Redis (caching)                │ FREE            │
│ DBT Cloud (transformations)            │ FREE            │
│ Sentry (error tracking)                │ FREE            │
│ GitHub Actions (CI/CD)                 │ FREE            │
├────────────────────────────────────────┼─────────────────┤
│ TOTAL                                  │ $59/month       │
└────────────────────────────────────────┴─────────────────┘

BREAK-EVEN: 1 client at $299/month
MARGIN: 80% gross margin per client
```

---

## Technology Stack Summary

| Layer | Technology | Why? |
|-------|------------|------|
| **Data Warehouse** | Snowflake | 90% cheaper than Azure Synapse for small scale |
| **Data Transformation** | DBT Cloud | SQL-based, testable, version-controlled |
| **ETL Orchestration** | Python + Cron | Simple, no overhead for 1-3 clients |
| **API Framework** | FastAPI | Modern, fast, async, auto-docs |
| **App Database** | Supabase | Free tier, includes auth, managed |
| **Blob Storage** | Azure Blob | Azure-native, cheap, reliable |
| **Secrets** | Azure Key Vault | Secure, auditable, Azure-native |
| **API Hosting** | Azure Container Apps | Serverless, auto-scaling, cost-effective |
| **Caching** | Upstash Redis | Serverless, pay-per-request |
| **Monitoring** | Sentry + Azure Monitor | Best-in-class error tracking + infra monitoring |
| **CI/CD** | GitHub Actions | Free, easy setup |

---

## Multi-Tenant Isolation

```
CLIENT 1                    CLIENT 2                    CLIENT 3
    │                           │                           │
    │ tenant_id=abc             │ tenant_id=def             │ tenant_id=ghi
    ▼                           ▼                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                   SHARED SNOWFLAKE DATABASE                      │
│                                                                  │
│  fact_ad_performance                                            │
│  ┌────────────┬──────────┬──────────────────────────────┐     │
│  │ tenant_id  │   date   │  impressions  clicks  cost   │     │
│  ├────────────┼──────────┼──────────────────────────────┤     │
│  │   abc      │ 2025-01-24│   15000      300    $60     │     │
│  │   def      │ 2025-01-24│   28000      500    $120    │ ◄── RLS ensures
│  │   ghi      │ 2025-01-24│   12000      250    $45     │     each client
│  │   abc      │ 2025-01-23│   14500      290    $58     │     only sees
│  │   def      │ 2025-01-23│   27500      495    $115    │     their own data
│  └────────────┴──────────┴──────────────────────────────┘     │
│                                                                  │
│  Row-Level Security Policy:                                     │
│  • Client 1 API calls: Only see tenant_id='abc' rows           │
│  • Client 2 API calls: Only see tenant_id='def' rows           │
│  • Client 3 API calls: Only see tenant_id='ghi' rows           │
└─────────────────────────────────────────────────────────────────┘
```

---

## Key Features

✅ **Multi-Tenant SaaS** - Shared infrastructure, isolated data
✅ **OAuth Integration** - Connect Google Ads, Meta, GA accounts
✅ **Automated ETL** - 3x daily data sync (6am, 2pm, 10pm)
✅ **Data Warehouse** - Proper fact/dimension schema
✅ **REST APIs** - Filtered, cached, authenticated
✅ **Row-Level Security** - Guaranteed tenant isolation
✅ **Scalable** - Start with 1-3 clients, scale to 100+
✅ **Cost-Effective** - $59/month infrastructure for MVP
✅ **AI-Ready** - Architecture supports future AI agents

---

## Next Steps (Development Phases)

**Phase 0: Setup (Week 1)**
- Create Azure account resources
- Set up Snowflake account
- Create Supabase project
- Set up GitHub repository

**Phase 1: API Access (Week 2)**
- Get Google Ads API credentials
- Get Meta API credentials
- Get GA API credentials
- Test OAuth flows manually

**Phase 2: Database (Week 3)**
- Create Snowflake schema (fact/dim tables)
- Create Supabase schema (tenants, users)
- Implement Row-Level Security

**Phase 3: ETL (Weeks 4-5)**
- Build Python extractors
- Implement DBT transformations
- Schedule cron jobs
- Test end-to-end data flow

**Phase 4: API (Weeks 6-7)**
- Build FastAPI application
- Implement authentication
- Create dashboard endpoints
- Add caching

**Phase 5: Testing & Deploy (Week 8)**
- Unit tests
- Integration tests
- Deploy to Azure
- Onboard first client

---

**Questions?** See full documentation in `ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md`
