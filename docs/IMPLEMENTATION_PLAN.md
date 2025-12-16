# Marketing IQ - Implementation Plan

> **Purpose:** This document outlines the complete implementation plan for the Marketing IQ platform.
> **Last Updated:** 2024-12-14
> **Related Docs:** PROJECT_STANDARDS.md, AGENT_DASHBOARD_MAPPING.md, ARCHITECTURE_FIVETRAN.md

---

## Executive Summary

| Item | Value |
|------|-------|
| **Product** | Multi-tenant SaaS marketing analytics platform |
| **Dashboards** | 18 total (12 AI agents + 6 platform views) |
| **Data Sources** | GA4, Google Ads, Meta Ads, Klaviyo via Fivetran |
| **Data Warehouse** | Snowflake (CLIENT_RARE_SEEDS_DB) |
| **Transformations** | DBT (21 dimensions + 22 facts) |
| **Backend** | FastAPI + Python 3.11 |
| **Frontend** | Next.js 14 + React + TypeScript + Tailwind |
| **Infrastructure** | Azure Container Apps + Terraform |
| **Est. Monthly Cost** | ~$250/mo (MVP) |

---

## Part 1: Data Model

### 1.1 Source Data Inventory

| Platform | Tables | Key Tables |
|----------|--------|------------|
| GA4 | 51 | TRAFFIC_ACQUISITION_*, CONVERSIONS_REPORT, DEMOGRAPHICS_* |
| Google Ads | 122 | CAMPAIGN_STATS, AD_GROUP_STATS, AD_STATS, KEYWORD_STATS |
| Facebook Ads | 124 | BASIC_*, AD_SET_HISTORY, DEMOGRAPHICS_*, ACTION_VIDEO_* |
| Klaviyo | 25 | EVENT (62M rows), CAMPAIGN, FLOW, SEGMENT_PERSON |

### 1.2 Dimension Tables (21)

| Table | Source | Type | Purpose |
|-------|--------|------|---------|
| DIM_DATE | Generated | Static | Date attributes (day, week, month, quarter) |
| DIM_HOUR | Generated | Static | Hour of day (0-23) |
| DIM_PLATFORM | Generated | Static | google_ads, meta, ga4, klaviyo, magento |
| DIM_DEVICE | GA4 + Meta | Reference | desktop, mobile, tablet |
| DIM_ACCOUNT | All platforms ACCOUNT_HISTORY | SCD Type 2 | Account metadata |
| DIM_CAMPAIGN | All platforms CAMPAIGN_HISTORY | SCD Type 2 | Campaign attributes |
| DIM_AD_GROUP | GOOGLE_ADS.AD_GROUP_HISTORY | SCD Type 2 | Google ad groups |
| DIM_AD_SET | FACEBOOK_ADS.AD_SET_HISTORY | SCD Type 2 | Facebook ad sets |
| DIM_AD | GOOGLE_ADS + FACEBOOK_ADS AD_HISTORY | SCD Type 2 | Ad creative metadata |
| DIM_KEYWORD | GOOGLE_ADS.AD_GROUP_CRITERION_HISTORY | SCD Type 2 | Keywords |
| DIM_GEOGRAPHY | GA4 + Meta + Google Ads GEO_TARGET | Slowly changing | Country, region, city |
| DIM_SOURCE_MEDIUM | GA4 source/medium reports | Append | Traffic sources |
| DIM_CONVERSION_ACTION | GA4 + Google Ads conversion tables | Reference | Conversion types |
| DIM_EMAIL_CAMPAIGN | Klaviyo CAMPAIGN + CAMPAIGN_MESSAGE | SCD Type 2 | Email campaigns |
| DIM_EMAIL_FLOW | Klaviyo FLOW + FLOW_ACTION | SCD Type 2 | Automated flows |
| DIM_EMAIL_TEMPLATE | Klaviyo EMAIL_TEMPLATE | SCD Type 2 | Template content |
| DIM_SEGMENT | Klaviyo SEGMENT | SCD Type 2 | Audience segments |
| DIM_LIST | Klaviyo LIST | SCD Type 2 | Email lists |
| DIM_BIDDING_STRATEGY | Google Ads BIDDING_STRATEGY_HISTORY | SCD Type 2 | Bidding configs |
| DIM_AUDIENCE | Google Ads USER_LIST + Meta CUSTOM_AUDIENCE | SCD Type 2 | Audience definitions |
| DIM_VIDEO | Facebook AD_VIDEO_HISTORY | SCD Type 2 | Video creative metadata |

### 1.3 Fact Tables (22)

#### Campaign Level
| Table | Grain | Source | Est. Rows |
|-------|-------|--------|-----------|
| FACT_CAMPAIGN_PERFORMANCE_DAILY | Campaign × Date × Device | GAds + Meta | 500K |
| FACT_CAMPAIGN_HOURLY | Campaign × Date × Hour × Device | GOOGLE_ADS.CAMPAIGN_HOURLY_STATS | 2M |

#### Ad Group / Ad Set Level
| Table | Grain | Source | Est. Rows |
|-------|-------|--------|-----------|
| FACT_AD_GROUP_PERFORMANCE_DAILY | Ad Group × Date × Device | GOOGLE_ADS.AD_GROUP_STATS | 1M |
| FACT_AD_SET_PERFORMANCE_DAILY | Ad Set × Date × Device | FACEBOOK_ADS.BASIC_AD_SET | 500K |

#### Ad Level
| Table | Grain | Source | Est. Rows |
|-------|-------|--------|-----------|
| FACT_AD_PERFORMANCE_DAILY | Ad × Date × Device | GAds + Meta | 1.5M |
| FACT_VIDEO_PERFORMANCE_DAILY | Video × Date | Meta ACTION_VIDEO_* | 200K |
| FACT_AD_REACTIONS_DAILY | Ad × Date × Reaction Type | Meta ACTION_REACTIONS_* | 100K |

#### Keyword / Search
| Table | Grain | Source | Est. Rows |
|-------|-------|--------|-----------|
| FACT_KEYWORD_PERFORMANCE_DAILY | Keyword × Date × Device | GOOGLE_ADS.KEYWORD_STATS | 500K |
| FACT_SEARCH_TERM_DAILY | Keyword × Search Term × Date | GOOGLE_ADS.SEARCH_TERM_STATS | 11M |

#### GA4 / Website
| Table | Grain | Source | Est. Rows |
|-------|-------|--------|-----------|
| FACT_GA4_TRAFFIC_DAILY | Source/Medium × Geo × Device × Date | GA4 TRAFFIC_ACQUISITION_* | 500K |
| FACT_GA4_CONVERSIONS_DAILY | Conversion × Source × Date | GA4 CONVERSIONS_REPORT | 50K |
| FACT_ECOMMERCE_ITEM_DAILY | Item × Date | GA4 ECOMMERCE_PURCHASES_ITEM_* | 20K |

#### Email (Klaviyo)
| Table | Grain | Source | Est. Rows |
|-------|-------|--------|-----------|
| FACT_EMAIL_CAMPAIGN_DAILY | Campaign × Message × Date | Klaviyo EVENT (aggregated) | 20K |
| FACT_EMAIL_FLOW_DAILY | Flow × Action × Date | Klaviyo EVENT (aggregated) | 10K |
| FACT_SEGMENT_MEMBERSHIP | Segment × Person × Date | Klaviyo SEGMENT_PERSON | 5.2M |
| FACT_LIST_MEMBERSHIP | List × Person × Date | Klaviyo LIST_PERSON | 950K |

#### Demographics / Audience
| Table | Grain | Source | Est. Rows |
|-------|-------|--------|-----------|
| FACT_DEMOGRAPHICS_DAILY | Campaign × Geo × Age × Gender × Date | Meta DEMOGRAPHICS_* | 50K |
| FACT_AUDIENCE_DAILY | Campaign × Audience × Date | GAds + Meta | 30K |

#### Config / Settings History
| Table | Grain | Source | Est. Rows |
|-------|-------|--------|-----------|
| FACT_CAMPAIGN_SETTINGS_HISTORY | Campaign × Change Date | GAds CAMPAIGN_*_SETTING_HISTORY | 100K |
| FACT_AD_GROUP_SETTINGS_HISTORY | Ad Group × Change Date | GAds AD_GROUP_*_SETTING_HISTORY | 200K |
| FACT_BIDDING_CHANGES_HISTORY | Entity × Change Date | GAds BIDDING_STRATEGY_HISTORY | 50K |
| FACT_BUDGET_CHANGES_HISTORY | Campaign × Change Date | GAds CAMPAIGN_BUDGET_HISTORY | 30K |

### 1.4 Data Coverage

| Platform | Coverage | Included |
|----------|----------|----------|
| Google Ads | **98%** | All performance + config/settings history |
| Facebook Ads | **95%** | All performance + video milestones + reactions |
| GA4 | **85%** | All reports (raw events not available via Fivetran) |
| Klaviyo | **98%** | All performance + segment/list membership |

---

## Part 2: API Architecture

### 2.1 Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/v1/metrics` | POST | Unified metrics query (all 18 dashboards) |
| `/api/v1/dashboards/{id}` | GET | Pre-configured dashboard data |
| `/api/v1/filters/{type}` | GET | Filter options (campaigns, etc.) |
| `/api/v1/schema` | GET | Schema discovery for agents |
| `/api/v1/agents/query` | POST | Natural language query |
| `/api/v1/agents/recommend` | POST | AI recommendations |
| `/api/v1/alerts` | GET | Active alerts/anomalies |
| `/api/v1/trends` | GET | Time-series data |

### 2.2 Caching Strategy

| Cache Layer | TTL | Use Case |
|-------------|-----|----------|
| API Response | 5 min | Same query, same params |
| Aggregated Metrics | 1 hour | Dashboard-level aggregations |
| Dimension Data | 24 hours | Campaign lists, filter options |
| Static Data | 7 days | Date dimension, platform codes |

### 2.3 Cache Invalidation

| Event | Invalidate |
|-------|------------|
| Fivetran sync complete | `metrics:*`, `dashboard:*` |
| Campaign created/updated | `filters:*:campaigns:*` |
| User saves filter | `dashboard:{tenant}:*` |
| Daily at 6 AM | All `metrics:*` |

---

## Part 3: Folder Structure

```
Marketing-IQ/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   ├── constants.py
│   │   │   └── exceptions.py
│   │   ├── api/v1/
│   │   │   ├── router.py
│   │   │   ├── auth.py
│   │   │   ├── metrics.py
│   │   │   ├── dashboards.py
│   │   │   ├── filters.py
│   │   │   └── agents.py
│   │   ├── services/
│   │   │   ├── metrics_service.py
│   │   │   ├── dashboard_service.py
│   │   │   └── cache_service.py
│   │   ├── repositories/
│   │   │   ├── base.py
│   │   │   ├── campaign_repo.py
│   │   │   ├── ga4_repo.py
│   │   │   ├── email_repo.py
│   │   │   └── unified_repo.py
│   │   ├── cache/
│   │   │   ├── redis_client.py
│   │   │   └── cache_manager.py
│   │   ├── db/
│   │   │   ├── session.py
│   │   │   ├── snowflake.py
│   │   │   └── models/
│   │   └── schemas/
│   │       ├── metrics.py
│   │       ├── filters.py
│   │       └── errors.py
│   ├── tests/
│   ├── alembic/
│   ├── Dockerfile
│   └── requirements.txt
│
├── dbt/
│   ├── dbt_project.yml
│   ├── profiles.yml
│   ├── models/
│   │   ├── staging/
│   │   │   ├── google_ads/
│   │   │   ├── facebook_ads/
│   │   │   ├── ga4/
│   │   │   └── klaviyo/
│   │   ├── intermediate/
│   │   └── marts/
│   │       ├── dimensions/
│   │       └── facts/
│   ├── seeds/
│   ├── macros/
│   └── tests/
│
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── (auth)/
│   │   │   └── (dashboard)/
│   │   ├── components/
│   │   │   ├── ui/
│   │   │   ├── charts/
│   │   │   ├── filters/
│   │   │   └── dashboard/
│   │   ├── hooks/
│   │   ├── lib/
│   │   └── types/
│   ├── package.json
│   └── tailwind.config.js
│
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   └── modules/
│
├── database/app_db/
│   └── schema.sql
│
├── docs/
│   ├── PROJECT_STANDARDS.md
│   ├── AGENT_DASHBOARD_MAPPING.md
│   ├── IMPLEMENTATION_PLAN.md
│   └── ARCHITECTURE_FIVETRAN.md
│
├── docker-compose.yml
├── Makefile
└── README.md
```

---

## Part 4: Implementation Phases

### Phase 1: Data Foundation
- [ ] Create DBT project structure
- [ ] Build staging models for all Fivetran sources (4 platforms)
- [ ] Build dimension tables (21)
- [ ] Build fact tables (22)
- [ ] Set up DBT Cloud / GitHub Actions for scheduling
- [ ] Test data quality with DBT tests

### Phase 2: Backend Core
- [ ] Set up FastAPI project structure
- [ ] Implement Snowflake connector with pooling
- [ ] Implement Redis caching layer
- [ ] Build unified metrics API (`POST /api/v1/metrics`)
- [ ] Build dashboard endpoint
- [ ] Build filter endpoints
- [ ] Implement repository pattern (no raw SQL)
- [ ] Implement tenant isolation middleware
- [ ] Write unit tests

### Phase 3: Authentication & Multi-tenancy
- [ ] Implement JWT authentication
- [ ] Build tenant management APIs
- [ ] Implement PostgreSQL models (SQLAlchemy)
- [ ] Set up Alembic migrations
- [ ] Row-level security testing

### Phase 4: Frontend Foundation
- [ ] Set up Next.js 14 project
- [ ] Install shadcn/ui components
- [ ] Build layout (sidebar, header)
- [ ] Build common components (charts, filters, cards)
- [ ] Implement API client with caching
- [ ] Build first 3 dashboards (Overview, GA4, Google Ads)

### Phase 5: All Dashboards
- [ ] Build remaining 15 dashboards
- [ ] Implement all filter types
- [ ] Implement all graph types
- [ ] Add loading states, error handling
- [ ] Responsive design

### Phase 6: Infrastructure & Deploy
- [ ] Write Terraform configurations
- [ ] Set up Azure resources
- [ ] Configure CI/CD pipelines
- [ ] Deploy to staging
- [ ] Security review

### Phase 7: Testing & Launch
- [ ] End-to-end testing
- [ ] Load testing
- [ ] Bug fixes
- [ ] Documentation
- [ ] Production deployment

---

## Part 5: Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| ETL | Fivetran (managed) | No custom ETL code to maintain |
| Transformations | DBT | Version-controlled, testable, incremental |
| Data Warehouse | Snowflake | Already in use, excellent for analytics |
| App Database | PostgreSQL | Multi-tenant, JSONB for configs |
| Cache | Redis | Industry standard, async support |
| Backend | FastAPI | Async, auto-docs, Pydantic |
| Data Access | Repository + PyPika | No raw SQL, type-safe |
| Frontend | Next.js 14 | App router, RSC, excellent DX |
| UI Components | shadcn/ui | Customizable, Tailwind-based |
| Charts | Recharts or Tremor | React-native, customizable |
| Infrastructure | Azure Container Apps | Simpler than AKS, auto-scale |
| IaC | Terraform | Multi-cloud, version-controlled |
| CI/CD | GitHub Actions | Free, Azure integration |
| Agent Framework | LangChain | Most mature, tool integration |

---

## Part 6: What's NOT Being Built

- Custom ETL pipelines (Prefect/Airflow) - Using Fivetran
- Azure Synapse - Using Snowflake
- Complex Kubernetes (AKS) - Container Apps sufficient
- Separate APIs per dashboard - Unified metrics API
- Custom auth system - JWT + OAuth standards
- Real-time streaming - Daily/hourly batch sufficient
- Raw SQL queries - Repository pattern with PyPika

---

## Part 7: Reference Documents

| Document | Path | Purpose |
|----------|------|---------|
| Project Standards | `docs/PROJECT_STANDARDS.md` | Coding rules (ALWAYS follow) |
| Dashboard Specs | `docs/AGENT_DASHBOARD_MAPPING.md` | 18 dashboards with metrics |
| Architecture | `docs/ARCHITECTURE_FIVETRAN.md` | Detailed architecture |
| App DB Schema | `database/app_db/schema.sql` | PostgreSQL tables |

---

## Part 8: Next Steps

1. **Approve this plan** - Review and confirm approach
2. **Start with DBT** - Data foundation first (21 dims + 22 facts)
3. **Then Backend** - APIs need data to query
4. **Then Frontend** - UI needs APIs to call
5. **Finally Deploy** - Infrastructure last (can develop locally)
