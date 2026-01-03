# Marketing IQ - Technical Architecture

> Enterprise-grade AI-powered marketing intelligence platform

---

## Table of Contents

1. [System Overview](#1-system-overview)
2. [Technology Stack](#2-technology-stack)
3. [Infrastructure Layer](#3-infrastructure-layer)
4. [Data Layer](#4-data-layer)
5. [Knowledge Graph Architecture](#5-knowledge-graph-architecture)
6. [AI/Agent Layer](#6-aiagent-layer)
7. [Application Layer](#7-application-layer)
8. [Data Flow Pipelines](#8-data-flow-pipelines)
9. [Security Architecture](#9-security-architecture)
10. [Deployment Architecture](#10-deployment-architecture)
11. [Cost Estimation](#11-cost-estimation)
12. [Performance & Testing Strategy](#12-performance--testing-strategy)

---

## 1. System Overview

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              MARKETING IQ PLATFORM                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                        PRESENTATION LAYER                            │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐   │    │
│  │  │   Next.js    │  │ Video Agent  │  │   Real-time WebSocket    │   │    │
│  │  │  Dashboard   │  │   Interface  │  │       Updates            │   │    │
│  │  └──────────────┘  └──────────────┘  └──────────────────────────┘   │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                    │                                         │
│                                    ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                         APPLICATION LAYER                            │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐   │    │
│  │  │   FastAPI    │  │    Redis     │  │     Authentication       │   │    │
│  │  │   Backend    │  │    Cache     │  │     (OAuth/JWT/RBAC)     │   │    │
│  │  └──────────────┘  └──────────────┘  └──────────────────────────┘   │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                    │                                         │
│                                    ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                        INTELLIGENCE LAYER                            │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐   │    │
│  │  │  Knowledge   │  │ Claude Agent │  │    Thought Processor     │   │    │
│  │  │    Graph     │  │     SDK      │  │    (Threshold Engine)    │   │    │
│  │  └──────────────┘  └──────────────┘  └──────────────────────────┘   │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                    │                                         │
│                                    ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                           DATA LAYER                                 │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐   │    │
│  │  │   Snowflake  │  │     dbt      │  │       Fivetran           │   │    │
│  │  │  Warehouse   │  │  Transform   │  │         ETL              │   │    │
│  │  └──────────────┘  └──────────────┘  └──────────────────────────┘   │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                    │                                         │
│                                    ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                         DATA SOURCES                                 │    │
│  │  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐            │    │
│  │  │  GA4   │ │ Google │ │  Meta  │ │Klaviyo │ │Magento │            │    │
│  │  │        │ │  Ads   │ │  Ads   │ │        │ │        │            │    │
│  │  └────────┘ └────────┘ └────────┘ └────────┘ └────────┘            │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Technology Stack

| Layer | Technology | Version | Purpose |
|-------|------------|---------|---------|
| **Frontend** | Next.js | 14.x | React-based SSR dashboard |
| **UI Components** | Tailwind CSS + shadcn/ui | Latest | Component library |
| **Charts** | Recharts / Apache ECharts | Latest | Data visualization |
| **Backend** | FastAPI | 0.100+ | Python async API |
| **Operational DB** | PostgreSQL | 16.x | Users, sessions, audit logs |
| **ORM** | SQLModel | Latest | PostgreSQL ORM (no raw SQL) |
| **Analytical DB** | Snowflake | Enterprise | Metrics data warehouse |
| **Vector DB** | Pinecone / Weaviate | Latest | Video agent Q&A, semantic search |
| **Cache** | Redis | 7.x | Session, query, rate limiting |
| **ETL** | Fivetran | Managed | Data ingestion (3-4x daily) |
| **Transform** | dbt Core | 1.7+ | SQL transformations + API views |
| **AI (Thoughts)** | Anthropic Python SDK | Latest | Deterministic thought generation |
| **AI (Video Q&A)** | Claude Agent SDK | Latest | Interactive agent with tools |
| **Video Avatar** | D-ID / HeyGen | TBD | AI avatar rendering |
| **TTS** | ElevenLabs | Latest | Text-to-speech |
| **Auth** | NextAuth.js + PostgreSQL | Latest | Authentication + session |
| **Queue** | Redis Streams / Celery | Latest | Background jobs |
| **Monitoring** | Prometheus + Grafana | Latest | Observability |

### Database Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    THREE-DATABASE ARCHITECTURE                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │   PostgreSQL    │  │    Snowflake    │  │   Vector DB     │  │
│  │  (Operational)  │  │   (Analytical)  │  │   (Semantic)    │  │
│  ├─────────────────┤  ├─────────────────┤  ├─────────────────┤  │
│  │ - Users         │  │ - Metrics data  │  │ - Embeddings    │  │
│  │ - Sessions      │  │ - Fact tables   │  │ - Q&A context   │  │
│  │ - Preferences   │  │ - Dim tables    │  │ - Semantic      │  │
│  │ - Action logs   │  │ - dbt views     │  │   search index  │  │
│  │ - Audit trail   │  │ - Historical    │  │ - Agent memory  │  │
│  │ - Thought state │  │                 │  │                 │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
│         │                     │                     │            │
│         └─────────────────────┼─────────────────────┘            │
│                               ▼                                  │
│                    ┌─────────────────┐                          │
│                    │   FastAPI       │                          │
│                    │   Backend       │                          │
│                    └─────────────────┘                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Infrastructure Layer

### 3.1 Multi-Tenant Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     TENANT ISOLATION MODEL                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │   Tenant A      │  │   Tenant B      │  │   Tenant C      │  │
│  │   (Client 1)    │  │   (Client 2)    │  │   (Client 3)    │  │
│  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘  │
│           │                    │                    │            │
│           ▼                    ▼                    ▼            │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │              SHARED APPLICATION LAYER                        ││
│  │  ┌─────────────────────────────────────────────────────────┐││
│  │  │  Tenant Context Middleware (JWT tenant_id claim)        │││
│  │  └─────────────────────────────────────────────────────────┘││
│  └─────────────────────────────────────────────────────────────┘│
│           │                    │                    │            │
│           ▼                    ▼                    ▼            │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                    SNOWFLAKE (Data Layer)                    ││
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          ││
│  │  │ TENANT_A_DB │  │ TENANT_B_DB │  │ TENANT_C_DB │          ││
│  │  │  - GA4      │  │  - GA4      │  │  - GA4      │          ││
│  │  │  - GADS     │  │  - GADS     │  │  - GADS     │          ││
│  │  │  - META     │  │  - META     │  │  - META     │          ││
│  │  │  - KLAVIYO  │  │  - KLAVIYO  │  │  - KLAVIYO  │          ││
│  │  └─────────────┘  └─────────────┘  └─────────────┘          ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Isolation Strategy:**
- Database-per-tenant in Snowflake (e.g., `CLIENT_RARE_SEEDS_DB`, `CLIENT_ACME_DB`)
- Row-level security (RLS) for shared tables
- Tenant ID propagated via JWT claims
- Separate Fivetran connectors per tenant

### 3.2 Redis Caching Strategy

```python
# Cache Layer Architecture
CACHE_TIERS = {
    "L1_SESSION": {
        "ttl": "30 minutes",
        "purpose": "User session, preferences",
        "key_pattern": "session:{tenant_id}:{user_id}"
    },
    "L2_QUERY": {
        "ttl": "5 minutes",
        "purpose": "Dashboard query results",
        "key_pattern": "query:{tenant_id}:{dashboard_id}:{hash}"
    },
    "L3_METRIC": {
        "ttl": "1 minute",
        "purpose": "Real-time metric values",
        "key_pattern": "metric:{tenant_id}:{metric_id}:{date}"
    },
    "L4_THOUGHT": {
        "ttl": "15 minutes",
        "purpose": "AI-generated thoughts cache",
        "key_pattern": "thought:{tenant_id}:{thought_id}"
    }
}
```

**Cache Invalidation Triggers:**
- ETL job completion (Fivetran webhook)
- Manual data refresh
- Threshold breach detection
- User-initiated refresh

---

## 4. Data Layer

### 4.1 Fivetran ETL Pipelines

```
┌─────────────────────────────────────────────────────────────────┐
│                     FIVETRAN CONNECTORS                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────┐     ┌────────────────────────────────────────┐  │
│  │   GA4      │────▶│  GA4_FIVETRAN Schema                   │  │
│  │  (API)     │     │  - TRAFFIC_SOURCE, CONVERSIONS_REPORT  │  │
│  └────────────┘     │  - EVENTS_REPORT, DEMOGRAPHIC_*        │  │
│                     └────────────────────────────────────────┘  │
│                                                                  │
│  ┌────────────┐     ┌────────────────────────────────────────┐  │
│  │ Google Ads │────▶│  GOOGLE_ADS_FIVETRAN Schema            │  │
│  │  (API)     │     │  - CAMPAIGN_STATS, AD_GROUP_STATS      │  │
│  └────────────┘     │  - KEYWORD_STATS, SEARCH_TERM_STATS    │  │
│                     └────────────────────────────────────────┘  │
│                                                                  │
│  ┌────────────┐     ┌────────────────────────────────────────┐  │
│  │  Meta Ads  │────▶│  META_ADS_FIVETRAN Schema              │  │
│  │  (API)     │     │  - BASIC_AD, BASIC_CAMPAIGN            │  │
│  └────────────┘     │  - DEMOGRAPHICS_*, DELIVERY_*          │  │
│                     └────────────────────────────────────────┘  │
│                                                                  │
│  ┌────────────┐     ┌────────────────────────────────────────┐  │
│  │  Klaviyo   │────▶│  KLAVIYO_FIVETRAN Schema               │  │
│  │  (API)     │     │  - EVENT, CAMPAIGN, FLOW, PERSON       │  │
│  └────────────┘     └────────────────────────────────────────┘  │
│                                                                  │
│  ┌────────────┐     ┌────────────────────────────────────────┐  │
│  │  Magento   │────▶│  MAGENTO_FIVETRAN Schema (Future)      │  │
│  │ (MySQL)    │     │  - sales_order, catalog_product_entity │  │
│  └────────────┘     └────────────────────────────────────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Sync Schedule (3-4x daily):**
- Google Ads: Every 6 hours
- Meta Ads: Every 6 hours
- GA4: Every 6-8 hours
- Klaviyo: Every 6 hours
- Magento: Every 4 hours (transactional)

**Event-Driven Processing:**
```
Fivetran Sync Complete
        │
        ▼
┌───────────────────┐
│ Fivetran Webhook  │──▶ Triggers dbt run
└───────────────────┘
        │
        ▼
┌───────────────────┐
│ dbt Run Complete  │──▶ Triggers threshold evaluation
└───────────────────┘
        │
        ▼
┌───────────────────┐
│ Threshold Engine  │──▶ Generates thoughts (max 2x/day)
└───────────────────┘
        │
        ▼
┌───────────────────┐
│ Cache Invalidation│──▶ Redis keys refreshed
└───────────────────┘
```

**Key Rules:**
- Actions/recommendations updated max 2x per day (not real-time)
- If data insufficient for analysis → keep existing recommendations
- Avoids unnecessary recalculations and API costs

### 4.2 Snowflake Schema Architecture

```
CLIENT_[TENANT]_DB
├── RAW (Fivetran landing zone)
│   ├── GA4_FIVETRAN
│   ├── GOOGLE_ADS_FIVETRAN
│   ├── META_ADS_FIVETRAN
│   ├── KLAVIYO_FIVETRAN
│   └── MAGENTO_FIVETRAN
│
├── PUBLIC (dbt transformed)
│   ├── Dimensions (24 tables)
│   │   ├── dim_date
│   │   ├── dim_campaign
│   │   ├── dim_ad_group
│   │   ├── dim_keyword
│   │   ├── dim_ad
│   │   ├── dim_audience
│   │   ├── dim_geography
│   │   └── ... (17 more)
│   │
│   ├── Facts (42 tables)
│   │   ├── fct_campaign_performance
│   │   ├── fct_keyword_performance
│   │   ├── fct_ad_performance
│   │   ├── fct_conversions
│   │   ├── fct_email_performance
│   │   └── ... (37 more)
│   │
│   └── Aggregates
│       ├── agg_daily_performance
│       ├── agg_weekly_rollup
│       └── agg_monthly_rollup
│
└── ANALYTICS (API-ready views)
    ├── v_dashboard_core_metrics
    ├── v_dashboard_budget
    └── v_dashboard_audience
```

### 4.3 dbt Transformation Layer

```yaml
# dbt project structure
dbt/
├── models/
│   ├── staging/           # Raw data cleanup
│   │   ├── stg_google_ads/
│   │   ├── stg_meta_ads/
│   │   ├── stg_ga4/
│   │   └── stg_klaviyo/
│   │
│   ├── marts/             # Business logic
│   │   ├── dimensions/    # dim_* tables
│   │   ├── facts/         # fct_* tables
│   │   └── core/          # Core metrics
│   │
│   └── analytics/         # API-ready aggregates
│
├── macros/                # Reusable SQL
├── tests/                 # Data quality tests
└── seeds/                 # Reference data
```

**Key dbt Features Used:**
- `dbt_utils.generate_surrogate_key()` for dimension keys
- Incremental models for large fact tables
- Snapshots for SCD Type 2 (campaign history)
- Tests for data quality (unique, not_null, relationships)

---

## 5. Knowledge Graph Architecture

### 5.1 Graph Structure

```
┌─────────────────────────────────────────────────────────────────┐
│                     KNOWLEDGE GRAPH MODEL                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  NODES (Entities)                                                │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐             │
│  │ METRIC  │  │THOUGHTLET│  │ THOUGHT │  │ ACTION  │             │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘             │
│       │            │            │            │                   │
│  EDGES (Relationships)                                           │
│       │            │            │            │                   │
│       ▼            ▼            ▼            ▼                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ BELONGS_TO    : Metric → Thoughtlet                         ││
│  │ COMPOSES      : Metric → Thought                            ││
│  │ AFFECTS       : Metric → Metric (cross-domain)              ││
│  │ TRIGGERS      : Thought → Action                            ││
│  │ CASCADES_TO   : Thought → Thought (future)                  ││
│  │ HAS_THRESHOLD : Metric → Threshold                          ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 5.2 Metric Node Schema

```json
{
  "metric_id": "cpc_google_ads",
  "name": "Cost Per Click",
  "domain": "marketing",
  "subdomain": "paid_search",
  "source": "google_ads",
  "thoughtlet_ids": ["dashboard_1", "dashboard_2", "dashboard_9"],
  "formula": "spend / clicks",
  "unit": "currency",
  "direction": "lower_is_better",
  "thresholds": {
    "warning": { "operator": ">", "value": 2.50 },
    "critical": { "operator": ">", "value": 5.00 }
  },
  "affects": [
    { "metric_id": "roas", "relationship": "inverse", "weight": 0.8 },
    { "metric_id": "cpa", "relationship": "direct", "weight": 0.9 },
    { "metric_id": "budget_utilization", "relationship": "direct", "weight": 0.5 }
  ],
  "affected_by": [
    { "metric_id": "quality_score", "relationship": "inverse", "weight": 0.7 },
    { "metric_id": "competition_level", "relationship": "direct", "weight": 0.6 }
  ]
}
```

### 5.3 Thought Node Schema

```json
{
  "thought_id": "ad_efficiency_declining",
  "name": "Ad Spend Efficiency Declining",
  "description": "Multiple signals indicate decreasing return on ad investment",
  "priority": "high",
  "category": "performance",
  "trigger_conditions": {
    "operator": "AND",
    "conditions": [
      { "metric_id": "roas", "operator": "<", "value": 3.0, "lookback_days": 7 },
      { "metric_id": "cpc", "operator": ">", "value": 2.0, "change_pct": 20 },
      { "metric_id": "spend", "operator": ">", "value": 10000 }
    ]
  },
  "component_metrics": [
    "spend", "roas", "cpc", "ctr", "cvr", "impressions"
  ],
  "blast_radius": {
    "internal": ["budget_utilization", "revenue", "profit_margin"],
    "external": ["finance.marketing_budget", "finance.cash_flow"]
  },
  "recommended_actions": [
    "pause_underperforming_campaigns",
    "reduce_bids_high_cpc_keywords",
    "reallocate_budget_to_top_performers"
  ]
}
```

### 5.4 Blast Radius Computation

```
                    ┌─────────────────┐
                    │  Ad Spend +25%  │
                    │   (Trigger)     │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
       ┌──────────┐   ┌──────────┐   ┌──────────┐
       │   CPC    │   │  Budget  │   │Impression│
       │   +15%   │   │   Used   │   │  Share   │
       └────┬─────┘   └────┬─────┘   └────┬─────┘
            │              │              │
       ┌────┼──────────────┼──────────────┼────┐
       ▼    ▼              ▼              ▼    ▼
   ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐
   │ ROAS │ │ CPA  │ │Profit│ │ Rev  │ │Market│
   │ -10% │ │ +12% │ │Margin│ │Target│ │Share │
   └──────┘ └──────┘ │ -5%  │ │ Gap  │ │ +3%  │
                     └──────┘ └──────┘ └──────┘
                         │
                         ▼
               ┌─────────────────┐
               │ FINANCE DOMAIN  │
               │ Cash Flow Impact│
               └─────────────────┘
```

### 5.5 Threshold Configuration

**Threshold Types:**
```python
THRESHOLD_TYPES = {
    "absolute": {
        # Fixed value comparison
        "example": "CPC > $5.00",
        "config": {"operator": ">", "value": 5.00}
    },
    "relative": {
        # Percentage change from baseline
        "example": "CTR dropped 20% vs last week",
        "config": {"operator": "change_pct", "value": -20, "baseline": "7d_ago"}
    },
    "trend": {
        # Consistent direction over time
        "example": "CPC increasing for 3 consecutive days",
        "config": {"operator": "trend", "direction": "increasing", "periods": 3}
    },
    "compound": {
        # Multiple conditions (AND/OR)
        "example": "CPC > $3 AND ROAS < 2",
        "config": {
            "operator": "AND",
            "conditions": [
                {"metric": "cpc", "operator": ">", "value": 3},
                {"metric": "roas", "operator": "<", "value": 2}
            ]
        }
    }
}
```

### 5.6 Blast Radius Calculator

```python
class BlastRadiusCalculator:
    """
    Traverse knowledge graph to find metrics affected by a change.
    Uses weighted relationships to estimate propagated impact.
    """
    def __init__(self, knowledge_graph):
        self.kg = knowledge_graph

    def calculate(self, trigger_metric: str, change_pct: float) -> BlastRadius:
        affected = []
        visited = set()

        def traverse(metric_id: str, depth: int, propagated_impact: float):
            if metric_id in visited or depth > 3:  # Max 3 levels deep
                return
            visited.add(metric_id)

            metric = self.kg.get_metric(metric_id)
            for rel in metric.affects:
                target_id = rel["metric_id"]
                weight = rel["weight"]  # 0-1 strength
                direction = rel["relationship"]  # "direct" or "inverse"

                # Calculate propagated impact
                impact = propagated_impact * weight
                if direction == "inverse":
                    impact = -impact

                affected.append({
                    "metric_id": target_id,
                    "estimated_impact_pct": round(impact, 2),
                    "depth": depth,
                    "relationship": direction
                })

                traverse(target_id, depth + 1, impact)

        traverse(trigger_metric, 0, change_pct)
        return BlastRadius(trigger=trigger_metric, affected=affected)
```

**Example Blast Radius:**
```
Trigger: Ad Spend +25%
├── CPC +15% (direct, weight 0.6)
│   ├── ROAS -12% (inverse, weight 0.8)
│   └── CPA +10% (direct, weight 0.7)
├── Budget Utilization +25% (direct, weight 1.0)
│   └── Impression Share +5% (direct, weight 0.2)
└── [Cross-Domain] Cash Flow -$X (future)
```

### 5.7 Storage Implementation (Snowflake JSON)

```sql
-- Metrics with relationships
CREATE TABLE knowledge_graph.metrics (
    metric_id VARCHAR PRIMARY KEY,
    name VARCHAR NOT NULL,
    source VARCHAR,  -- 'google_ads', 'meta_ads', etc.
    domain VARCHAR DEFAULT 'marketing',
    subdomain VARCHAR,
    dbt_view VARCHAR,  -- Pre-built view name
    unit VARCHAR,  -- 'currency', 'percentage', 'count'
    direction VARCHAR,  -- 'higher_is_better', 'lower_is_better'
    thresholds VARIANT,  -- {"warning": {...}, "critical": {...}}
    affects VARIANT,  -- [{"metric_id": "roas", "weight": 0.8, "relationship": "inverse"}]
    affected_by VARIANT,
    thoughtlet_ids ARRAY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

-- Thought definitions (fixed for MVP)
CREATE TABLE knowledge_graph.thoughts (
    thought_id VARCHAR PRIMARY KEY,
    name VARCHAR NOT NULL,
    category VARCHAR,  -- 'performance', 'budget', 'creative', etc.
    priority VARCHAR,  -- 'critical', 'high', 'medium', 'low'
    trigger_conditions VARIANT,  -- {"operator": "AND", "conditions": [...]}
    component_metric_ids ARRAY,
    blast_radius_config VARIANT,
    recommended_action_ids ARRAY,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);

-- Action templates
CREATE TABLE knowledge_graph.actions (
    action_id VARCHAR PRIMARY KEY,
    name VARCHAR NOT NULL,
    description VARCHAR,
    impact_level VARCHAR,  -- 'low', 'medium', 'high', 'critical'
    requires_approval BOOLEAN DEFAULT FALSE,
    integration_type VARCHAR,  -- 'manual', 'api', 'webhook'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
);
```

---

## 6. AI/Agent Layer

### 6.1 Agent Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     AGENT ORCHESTRATION                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                    VIDEO AGENT (Primary)                     ││
│  │  ┌──────────────────────────────────────────────────────┐   ││
│  │  │ Responsibilities:                                     │   ││
│  │  │ - Daily briefing narration                           │   ││
│  │  │ - Interactive Q&A with user                          │   ││
│  │  │ - Voice + video avatar rendering                     │   ││
│  │  │ - Context-aware responses                            │   ││
│  │  └──────────────────────────────────────────────────────┘   ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                   │
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                 SPECIALIZED SUB-AGENTS                       ││
│  │                                                              ││
│  │  ┌────────────┐  ┌────────────┐  ┌────────────────────────┐ ││
│  │  │  Thought   │  │  Action    │  │   Insight Generator    │ ││
│  │  │ Processor  │  │ Recommender│  │   (Pattern Detection)  │ ││
│  │  └────────────┘  └────────────┘  └────────────────────────┘ ││
│  │                                                              ││
│  │  ┌────────────┐  ┌────────────┐  ┌────────────────────────┐ ││
│  │  │  Anomaly   │  │ Forecaster │  │   Natural Language     │ ││
│  │  │  Detector  │  │            │  │   Query Handler        │ ││
│  │  └────────────┘  └────────────┘  └────────────────────────┘ ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 6.2 Thought Processing Pipeline

```python
# Pseudo-code for thought processing
class ThoughtProcessor:
    def __init__(self, knowledge_graph, agent_sdk):
        self.kg = knowledge_graph
        self.agent = agent_sdk

    def process_metric_change(self, metric_id: str, old_value: float, new_value: float):
        """
        1. Check if threshold breached
        2. Identify affected thoughts
        3. Calculate blast radius
        4. Generate AI analysis
        5. Create recommendations
        """
        # Step 1: Threshold check
        metric = self.kg.get_metric(metric_id)
        breach = self.check_threshold(metric, new_value)

        if not breach:
            return None

        # Step 2: Find related thoughts
        thoughts = self.kg.get_thoughts_containing_metric(metric_id)

        # Step 3: Calculate blast radius for each thought
        affected_metrics = []
        for thought in thoughts:
            radius = self.calculate_blast_radius(thought, metric_id, new_value)
            affected_metrics.extend(radius)

        # Step 4: Build context for agent
        context = {
            "trigger_metric": metric,
            "breach_type": breach.severity,
            "change_pct": ((new_value - old_value) / old_value) * 100,
            "affected_thoughts": thoughts,
            "blast_radius": affected_metrics,
            "historical_data": self.get_historical_context(metric_id)
        }

        # Step 5: Generate AI analysis
        analysis = self.agent.analyze(
            prompt=self.build_analysis_prompt(context),
            tools=["recommend_action", "forecast", "explain"]
        )

        return {
            "thought": thought,
            "analysis": analysis.explanation,
            "recommendations": analysis.actions,
            "priority": analysis.urgency
        }
```

### 6.3 SDK Usage Pattern

**Two SDK Approach:**
| Use Case | SDK | Why |
|----------|-----|-----|
| Thought Generation | Anthropic Python SDK | Deterministic flow, you control context |
| Video Agent Q&A | Claude Agent SDK | Interactive, multi-step reasoning |

**Anthropic Python SDK (Thought Generation):**
```python
from anthropic import Anthropic

class ThoughtGenerator:
    """
    Used for: Generating thoughts when thresholds are breached
    Flow: Build context → Single API call → Parse response
    Cost: 1 API call per thought (predictable)
    """
    def __init__(self):
        self.client = Anthropic()

    def generate_thought_analysis(self, context: dict) -> ThoughtAnalysis:
        # YOU control exactly what goes in
        prompt = self.build_prompt(context)

        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2048,
            messages=[{
                "role": "user",
                "content": prompt
            }],
            system="""You are a marketing analytics expert. Analyze the
            provided metrics data and generate actionable insights.
            Always explain the 'why' behind changes.
            Return structured JSON with: analysis, recommendations, priority."""
        )

        return self.parse_response(response)
```

**Claude Agent SDK (Video Agent Q&A):**
```python
from anthropic import Agent, Tool

class VideoAgentService:
    """
    Used for: Interactive Q&A with video agent
    Flow: User asks → Agent decides tools → Multi-step reasoning → Response
    Cost: Variable (agent may loop multiple times)
    """
    def __init__(self, metric_service, knowledge_graph):
        self.tools = [
            Tool(
                name="query_metrics",
                description="Query current and historical metric values",
                function=metric_service.query
            ),
            Tool(
                name="get_blast_radius",
                description="Calculate which metrics are affected by a change",
                function=knowledge_graph.get_blast_radius
            ),
            Tool(
                name="compare_periods",
                description="Compare metrics across time periods",
                function=metric_service.compare
            )
        ]

        self.agent = Agent(
            model="claude-sonnet-4-20250514",
            tools=self.tools,
            max_iterations=5,  # Cost control
            system_prompt="""You are a helpful marketing analytics assistant.
            Answer questions about campaign performance, metrics, and trends.
            Use tools to fetch real data before answering."""
        )

    async def chat(self, user_message: str, context: dict) -> str:
        # Agent decides what to do
        return await self.agent.run(user_message, context=context)
```

### 6.4 Agent Hallucination Prevention

**Five Layers of Protection:**

| Layer | Strategy | Implementation |
|-------|----------|----------------|
| 1 | Constrain Input | Pre-fetch verified data, don't let agent query freely |
| 2 | Structured Output | Force JSON schema responses, not free-form text |
| 3 | Confidence Scoring | Agent must declare confidence, validate against data |
| 4 | Human-in-the-Loop | High-impact actions require user approval |
| 5 | Audit Trail | Log all decisions, data used, outcomes |

**Layer 1: Constrain What Agent Sees**
```python
# DON'T: Let agent make up data
agent.run("Why did ROAS drop?")  # Risky - agent might hallucinate

# DO: Pre-fetch verified data, give agent ONLY facts
context = {
    "roas_current": 2.8,        # From Snowflake (verified)
    "roas_previous": 3.5,       # From Snowflake (verified)
    "change_pct": -20,          # Calculated by us
    "top_campaigns": [...],     # From Snowflake (verified)
    "date_range": "2024-12-12 to 2024-12-19"
}
response = generate_analysis(context)  # Agent analyzes, doesn't fetch
```

**Layer 2: Structured Output Schema**
```python
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    messages=[{"role": "user", "content": prompt}],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "thought_analysis",
            "schema": {
                "type": "object",
                "properties": {
                    "summary": {"type": "string", "maxLength": 200},
                    "root_cause": {
                        "type": "string",
                        "enum": [  # Constrained options
                            "increased_competition",
                            "budget_exhaustion",
                            "creative_fatigue",
                            "audience_saturation",
                            "seasonal_trend",
                            "unknown"
                        ]
                    },
                    "confidence": {"type": "number", "minimum": 0, "maximum": 1},
                    "recommendations": {"type": "array", "maxItems": 3}
                },
                "required": ["summary", "root_cause", "confidence"]
            }
        }
    }
)
```

**Layer 3: Validation & Confidence**
```python
class ThoughtValidator:
    def validate(self, thought: ThoughtAnalysis, source_data: dict) -> bool:
        # Check 1: Direction match
        if thought.claims_increase and source_data["change"] < 0:
            return False  # Hallucination detected

        # Check 2: Values mentioned exist in source
        for value in thought.mentioned_values:
            if not self.value_exists_in_source(value, source_data):
                thought.confidence *= 0.5  # Reduce confidence

        # Check 3: Sample size vs confidence
        if source_data["sample_size"] < 100 and thought.confidence > 0.8:
            thought.confidence = 0.6  # Cap confidence

        return True
```

**Layer 4: Approval Matrix**
```
┌─────────────────┬──────────────┬─────────────────────┐
│ Impact Level    │ Confidence   │ Approval Required   │
├─────────────────┼──────────────┼─────────────────────┤
│ Low (info only) │ Any          │ None                │
│ Medium          │ > 0.7        │ None                │
│ Medium          │ < 0.7        │ User confirmation   │
│ High (spend)    │ Any          │ User confirmation   │
│ Critical        │ Any          │ Admin approval      │
└─────────────────┴──────────────┴─────────────────────┘
```

**Layer 5: Audit Trail**
```sql
CREATE TABLE audit.action_logs (
    id SERIAL PRIMARY KEY,
    thought_id VARCHAR,
    action_id VARCHAR,
    recommended_by VARCHAR,  -- 'ai' or 'human'
    confidence FLOAT,
    source_data_hash VARCHAR,  -- Hash of data used
    user_approved BOOLEAN,
    executed_at TIMESTAMP,
    outcome VARCHAR,  -- 'success', 'failed', 'reverted'
    outcome_metrics JSONB  -- What happened after
);
```

---

### 6.5 Video Agent Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    VIDEO AGENT PIPELINE                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  User Query ──▶ Speech-to-Text ──▶ Intent Recognition           │
│                                           │                      │
│                                           ▼                      │
│                          ┌────────────────────────────┐          │
│                          │    Claude Agent SDK        │          │
│                          │  (Process & Generate)      │          │
│                          └────────────────────────────┘          │
│                                           │                      │
│                                           ▼                      │
│                          ┌────────────────────────────┐          │
│                          │   Text-to-Speech (TTS)     │          │
│                          └────────────────────────────┘          │
│                                           │                      │
│                                           ▼                      │
│                          ┌────────────────────────────┐          │
│                          │   AI Avatar Rendering      │          │
│                          │   (Lip-sync + Gestures)    │          │
│                          └────────────────────────────┘          │
│                                           │                      │
│                                           ▼                      │
│                          ┌────────────────────────────┐          │
│                          │   WebRTC Stream to Client  │          │
│                          └────────────────────────────┘          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Video Agent Components:**
- **Speech Recognition**: Whisper API or browser Web Speech API
- **AI Avatar**: D-ID, Synthesia, or HeyGen integration
- **TTS**: ElevenLabs or Azure Speech Services
- **Streaming**: WebRTC for low-latency delivery

---

## 7. Application Layer

### 7.1 Next.js Frontend Architecture

```
frontend/
├── app/                      # Next.js 14 App Router
│   ├── (auth)/              # Auth routes group
│   │   ├── login/
│   │   └── register/
│   ├── (dashboard)/         # Dashboard routes group
│   │   ├── layout.tsx       # Dashboard shell
│   │   ├── page.tsx         # Landing page (Video Agent)
│   │   ├── thoughtlets/     # Dashboard pages
│   │   │   ├── [id]/page.tsx
│   │   ├── thoughts/        # Thought detail pages
│   │   └── actions/         # Action management
│   └── api/                 # API routes (BFF pattern)
│
├── components/
│   ├── ui/                  # shadcn/ui components
│   ├── charts/              # Visualization components
│   ├── video-agent/         # Video agent components
│   ├── thoughtlets/         # Dashboard components
│   ├── thoughts/            # Thought cards
│   └── actions/             # Action buttons
│
├── lib/
│   ├── api/                 # API client
│   ├── hooks/               # Custom React hooks
│   ├── stores/              # Zustand state stores
│   └── utils/               # Utilities
│
└── styles/                  # Global styles
```

### 7.2 FastAPI Backend Architecture

```
backend/
├── app/
│   ├── main.py              # FastAPI app entry
│   ├── config.py            # Configuration
│   │
│   ├── api/
│   │   ├── v1/
│   │   │   ├── endpoints/
│   │   │   │   ├── metrics.py
│   │   │   │   ├── thoughtlets.py
│   │   │   │   ├── thoughts.py
│   │   │   │   ├── actions.py
│   │   │   │   └── agent.py
│   │   │   └── router.py
│   │   └── deps.py          # Dependencies
│   │
│   ├── core/
│   │   ├── security.py      # Auth logic
│   │   ├── cache.py         # Redis integration
│   │   └── events.py        # Event handlers
│   │
│   ├── services/
│   │   ├── snowflake.py     # DB queries
│   │   ├── knowledge_graph.py
│   │   ├── thought_processor.py
│   │   └── agent_service.py
│   │
│   ├── models/              # Pydantic models
│   └── schemas/             # API schemas
│
├── tests/
└── alembic/                 # Migrations (if using PostgreSQL)
```

### 7.3 API Design (Hybrid REST)

**Design Principles:**
1. Individual endpoints for knowledge graph queries
2. Batch endpoints for dashboard data (avoid N+1 problem)
3. Metric Registry as single source of truth
4. dbt views encapsulate SQL complexity - API queries simple views

### 7.3.1 Single-Source Metric Pattern

**Problem:** Same metrics are needed by both Thoughtlets (grouped) and Knowledge Graph (individual with relationships). Don't want to write query logic twice.

**Solution:** One metric definition → One query → Multiple consumers

```
┌─────────────────────────────────────────────────────────────────┐
│              ONE METRIC → MULTIPLE CONSUMERS                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                   METRIC REGISTRY                            ││
│  │  (Single source: definition + thresholds + relationships)   ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                   │
│              ┌───────────────┼───────────────┐                  │
│              ▼               ▼               ▼                  │
│      ┌─────────────┐ ┌─────────────┐ ┌─────────────┐           │
│      │ THOUGHTLET  │ │  KNOWLEDGE  │ │  THRESHOLD  │           │
│      │  (10 metrics│ │    GRAPH    │ │   ENGINE    │           │
│      │   grouped)  │ │(1 + related)│ │ (1 + rules) │           │
│      └──────┬──────┘ └──────┬──────┘ └──────┬──────┘           │
│             │               │               │                   │
│             └───────────────┼───────────────┘                   │
│                             ▼                                    │
│              ┌─────────────────────────────┐                    │
│              │      MetricService          │                    │
│              │    get_metric() - CORE      │                    │
│              └──────────────┬──────────────┘                    │
│                             ▼                                    │
│              ┌─────────────────────────────┐                    │
│              │   dbt View (query once)     │                    │
│              │  v_metric_{metric_id}       │                    │
│              └─────────────────────────────┘                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Metric Registry Structure:**
```python
METRIC_REGISTRY = {
    "cpc_google_ads": MetricDefinition(
        id="cpc_google_ads",
        name="Cost Per Click",
        source="google_ads",
        dbt_view="v_metric_cpc_google_ads",  # Query logic lives here
        unit="currency",
        direction="lower_is_better",

        # For Thoughtlets - which dashboards show this metric
        thoughtlet_ids=["core_performance", "budget_control", "google_ads"],

        # For Threshold Engine
        thresholds={
            "warning": {"operator": ">", "value": 2.50},
            "critical": {"operator": ">", "value": 5.00}
        },

        # For Knowledge Graph / Blast Radius
        affects=[{"metric_id": "roas", "weight": 0.8, "relationship": "inverse"}],
        affected_by=[{"metric_id": "quality_score", "weight": 0.7}]
    )
}
```

**Service Layer - Core Method Used By All:**
```python
class MetricService:
    # CORE METHOD - everyone uses this
    async def get_metric(self, metric_id: str, tenant_id: str) -> MetricData:
        definition = self.registry.get(metric_id)
        df = await self.sf.query(f"SELECT * FROM {definition.dbt_view}")
        return MetricData(..., affects=definition.affects, ...)

    # FOR THOUGHTLETS - batch fetch
    async def get_metrics_for_thoughtlet(self, thoughtlet_id: str, tenant_id: str):
        metric_ids = [m.id for m in self.registry.all() if thoughtlet_id in m.thoughtlet_ids]
        return await asyncio.gather(*[self.get_metric(mid, tenant_id) for mid in metric_ids])

    # FOR KNOWLEDGE GRAPH - single with relationships
    async def get_metric_with_graph(self, metric_id: str, tenant_id: str):
        metric = await self.get_metric(metric_id, tenant_id)
        return MetricWithGraph(**metric.dict(), related_metrics=[...])
```

```yaml
# Core API Structure
/api/v1:
  /metrics:
    GET /                        # List all metric definitions
    GET /{metric_id}             # Single metric (for knowledge graph)
    GET /{metric_id}/history     # Time series data
    GET /{metric_id}/relationships  # Affected/affected-by metrics
    POST /batch                  # Batch fetch multiple metrics
    # Body: { "metric_ids": ["cpc", "ctr"], "date_range": "7d" }

  /thoughtlets:
    GET /                        # List all dashboards
    GET /{id}                    # Get dashboard with ALL metrics (single call)
    GET /{id}/config             # Dashboard configuration only

  /thoughts:
    GET /                        # List active thoughts
    GET /{id}                    # Thought details + blast radius
    POST /{id}/dismiss           # Dismiss thought
    POST /{id}/snooze            # Snooze for X hours

  /actions:
    GET /                        # List pending actions
    POST /{id}/execute           # Execute action
    POST /{id}/schedule          # Schedule action
    GET /{id}/status             # Check execution status

  /agent:
    POST /chat                   # Send message to video agent
    GET /briefing                # Get daily briefing content
    POST /briefing/regenerate    # Force regenerate briefing
    WS /stream                   # WebSocket for real-time updates

  /knowledge-graph:
    GET /metrics                 # All metrics with relationships
    GET /metrics/{id}/blast-radius  # Calculate blast radius
    GET /thoughts                # All thought definitions
```

**Metric Registry Pattern:**
```python
# Single source of truth for all metrics
# Used by: API, dbt, Knowledge Graph, Threshold Engine, Frontend

METRIC_REGISTRY = {
    "cpc_google_ads": {
        "id": "cpc_google_ads",
        "name": "Cost Per Click",
        "source": "google_ads",
        "dbt_view": "v_metric_cpc_google_ads",  # Pre-built in dbt
        "unit": "currency",
        "direction": "lower_is_better",
        "thoughtlets": ["core_performance", "budget_control"],
        "thresholds": {...},
        "relationships": {...}
    }
}
```

### 7.4 WebSocket Real-time Updates

```python
# WebSocket manager for real-time updates
from fastapi import WebSocket
from typing import Dict, List

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, tenant_id: str):
        await websocket.accept()
        if tenant_id not in self.active_connections:
            self.active_connections[tenant_id] = []
        self.active_connections[tenant_id].append(websocket)

    async def broadcast_thought(self, tenant_id: str, thought: dict):
        """Broadcast new thought to all tenant users"""
        if tenant_id in self.active_connections:
            for connection in self.active_connections[tenant_id]:
                await connection.send_json({
                    "type": "new_thought",
                    "data": thought
                })

    async def broadcast_metric_update(self, tenant_id: str, metric: dict):
        """Broadcast metric change to all tenant users"""
        if tenant_id in self.active_connections:
            for connection in self.active_connections[tenant_id]:
                await connection.send_json({
                    "type": "metric_update",
                    "data": metric
                })
```

---

## 8. Data Flow Pipelines

### 8.1 ETL to Dashboard Flow

```
┌──────────────────────────────────────────────────────────────────────────┐
│                        DATA PIPELINE FLOW                                 │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐│
│  │ Source  │───▶│Fivetran │───▶│Snowflake│───▶│   dbt   │───▶│  API    ││
│  │  APIs   │    │   ETL   │    │   RAW   │    │Transform│    │ Layer   ││
│  └─────────┘    └─────────┘    └─────────┘    └─────────┘    └─────────┘│
│       │              │              │              │              │      │
│       ▼              ▼              ▼              ▼              ▼      │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐│
│  │ GA4     │    │Schedule │    │ Landing │    │ Staging │    │ Redis   ││
│  │ G.Ads   │    │ 6 hrs   │    │  Zone   │    │ → Marts │    │ Cache   ││
│  │ Meta    │    │         │    │         │    │         │    │         ││
│  │ Klaviyo │    │         │    │         │    │         │    │         ││
│  └─────────┘    └─────────┘    └─────────┘    └─────────┘    └─────────┘│
│                                                      │              │    │
│                                                      ▼              ▼    │
│                                                 ┌─────────┐    ┌─────────┐│
│                                                 │Knowledge│    │ Next.js ││
│                                                 │  Graph  │    │Frontend ││
│                                                 └─────────┘    └─────────┘│
│                                                                           │
└──────────────────────────────────────────────────────────────────────────┘
```

### 8.2 Thought Generation Flow

```
┌──────────────────────────────────────────────────────────────────────────┐
│                      THOUGHT GENERATION PIPELINE                          │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  ┌─────────────────┐                                                     │
│  │ Metric Change   │  (dbt run completes, new data available)            │
│  │ Detected        │                                                     │
│  └────────┬────────┘                                                     │
│           │                                                               │
│           ▼                                                               │
│  ┌─────────────────┐                                                     │
│  │ Threshold Check │  (Compare against defined thresholds)               │
│  │                 │                                                     │
│  └────────┬────────┘                                                     │
│           │                                                               │
│     ┌─────┴─────┐                                                        │
│     ▼           ▼                                                        │
│  ┌──────┐   ┌──────────────────┐                                         │
│  │ Pass │   │ Breach Detected  │                                         │
│  │(skip)│   └────────┬─────────┘                                         │
│  └──────┘            │                                                   │
│                      ▼                                                    │
│           ┌─────────────────┐                                            │
│           │ Query Knowledge │  (Find thoughts containing this metric)    │
│           │ Graph           │                                            │
│           └────────┬────────┘                                            │
│                    │                                                      │
│                    ▼                                                      │
│           ┌─────────────────┐                                            │
│           │ Calculate Blast │  (Traverse graph for affected metrics)     │
│           │ Radius          │                                            │
│           └────────┬────────┘                                            │
│                    │                                                      │
│                    ▼                                                      │
│           ┌─────────────────┐                                            │
│           │ Build Context   │  (Historical data, related metrics)        │
│           │ Package         │                                            │
│           └────────┬────────┘                                            │
│                    │                                                      │
│                    ▼                                                      │
│           ┌─────────────────┐                                            │
│           │ Agent SDK       │  (Claude processes context)                │
│           │ Processing      │                                            │
│           └────────┬────────┘                                            │
│                    │                                                      │
│                    ▼                                                      │
│           ┌─────────────────┐                                            │
│           │ Generate Output │                                            │
│           │ - Analysis      │                                            │
│           │ - Recommendations│                                           │
│           │ - Priority      │                                            │
│           └────────┬────────┘                                            │
│                    │                                                      │
│                    ▼                                                      │
│           ┌─────────────────┐                                            │
│           │ Store & Notify  │  (Save to DB, WebSocket broadcast)         │
│           └─────────────────┘                                            │
│                                                                           │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## 9. Security Architecture

### 9.1 Authentication & Authorization

```
┌─────────────────────────────────────────────────────────────────┐
│                    SECURITY LAYERS                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Layer 1: Authentication (Identity)                              │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │  OAuth 2.0 / OpenID Connect                                 ││
│  │  - Google Workspace SSO                                     ││
│  │  - Microsoft Entra ID                                       ││
│  │  - Email/Password (fallback)                                ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                   │
│                              ▼                                   │
│  Layer 2: Session Management                                     │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │  JWT Tokens                                                  ││
│  │  - Access Token (15 min expiry)                             ││
│  │  - Refresh Token (7 day expiry, Redis storage)              ││
│  │  - Claims: user_id, tenant_id, roles[], permissions[]       ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                   │
│                              ▼                                   │
│  Layer 3: Authorization (RBAC)                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │  Roles:                                                      ││
│  │  - ADMIN: Full access, user management                      ││
│  │  - ANALYST: View all, edit dashboards                       ││
│  │  - VIEWER: Read-only access                                 ││
│  │  - API_USER: Programmatic access only                       ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                   │
│                              ▼                                   │
│  Layer 4: Tenant Isolation                                       │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │  - Database-level isolation (Snowflake)                     ││
│  │  - API middleware validates tenant_id                       ││
│  │  - Redis key prefixes by tenant                             ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 9.2 Data Security

```yaml
# Security Controls
encryption:
  at_rest:
    - Snowflake: AES-256 (automatic)
    - Redis: TLS + encryption at rest
    - Backups: Encrypted
  in_transit:
    - TLS 1.3 for all connections
    - Certificate pinning for APIs

secrets_management:
  - Environment variables (dev)
  - AWS Secrets Manager / HashiCorp Vault (prod)
  - No secrets in code or git

data_protection:
  - PII masking in logs
  - Data retention policies (configurable)
  - GDPR compliance (right to deletion)
  - SOC 2 Type II controls

api_security:
  - Rate limiting (Redis-based)
  - Request validation (Pydantic)
  - CORS configuration
  - OWASP Top 10 mitigations
```

### 9.3 Additional Security Layers

```
┌─────────────────────────────────────────────────────────────────┐
│                    SECURITY LAYERS (5-7)                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Layer 5: Input Validation                                       │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │  - Pydantic strict mode for all API inputs                  ││
│  │  - SQL injection prevention (parameterized queries)          ││
│  │  - XSS prevention (sanitize user-generated content)          ││
│  │  - File upload validation (type, size, content)              ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                   │
│                              ▼                                   │
│  Layer 6: Rate Limiting & DDoS Protection                        │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │  - Redis-based rate limiting per user/tenant                 ││
│  │  - CloudFront/WAF for DDoS mitigation                        ││
│  │  - API throttling: 100 req/min per user                      ││
│  │  - Agent API: 10 req/min (cost protection)                   ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                   │
│                              ▼                                   │
│  Layer 7: Audit & Compliance                                     │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │  - Complete audit trail (who, what, when)                    ││
│  │  - Action logging with outcome tracking                      ││
│  │  - Data access logging for compliance                        ││
│  │  - Retention policies (GDPR, SOC 2)                          ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 9.4 Security Implementation Details

```python
# Rate Limiting Configuration
RATE_LIMITS = {
    "default": {
        "requests_per_minute": 100,
        "requests_per_hour": 1000
    },
    "agent_api": {
        "requests_per_minute": 10,  # Cost protection
        "requests_per_hour": 100
    },
    "auth": {
        "login_attempts_per_minute": 5,
        "password_reset_per_hour": 3
    }
}

# Audit Log Schema
class AuditLog(BaseModel):
    timestamp: datetime
    tenant_id: str
    user_id: str
    action: str  # 'view', 'create', 'update', 'delete', 'execute'
    resource_type: str  # 'thought', 'action', 'dashboard', 'metric'
    resource_id: str
    ip_address: str
    user_agent: str
    outcome: str  # 'success', 'failure', 'denied'
    metadata: dict  # Additional context
```

---

## 10. Deployment Architecture

### 10.1 Cloud Infrastructure

```
┌─────────────────────────────────────────────────────────────────┐
│                    CLOUD DEPLOYMENT (AWS)                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                     CDN (CloudFront)                         ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                   │
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                  Load Balancer (ALB)                         ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                   │
│         ┌────────────────────┼────────────────────┐             │
│         ▼                    ▼                    ▼             │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐      │
│  │  Next.js    │      │  FastAPI    │      │   Worker    │      │
│  │ (Vercel or  │      │  (ECS/EKS)  │      │  (Celery)   │      │
│  │  ECS)       │      │             │      │             │      │
│  └─────────────┘      └─────────────┘      └─────────────┘      │
│         │                    │                    │             │
│         └────────────────────┼────────────────────┘             │
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                                                              ││
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          ││
│  │  │   Redis     │  │  Snowflake  │  │   S3        │          ││
│  │  │ (ElastiCache│  │  (Managed)  │  │  (Assets)   │          ││
│  │  │  Cluster)   │  │             │  │             │          ││
│  │  └─────────────┘  └─────────────┘  └─────────────┘          ││
│  │                                                              ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 10.2 CI/CD Pipeline

```yaml
# GitHub Actions Workflow
name: Deploy Marketing IQ

on:
  push:
    branches: [main, staging]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run tests
        run: |
          pytest backend/tests/
          npm test --prefix frontend/

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Build Docker images
        run: docker build -t marketing-iq-api .
      - name: Push to ECR
        run: aws ecr push ...

  deploy-staging:
    needs: build
    if: github.ref == 'refs/heads/staging'
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to staging
        run: kubectl apply -f k8s/staging/

  deploy-prod:
    needs: build
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to production
        run: kubectl apply -f k8s/prod/
      - name: Run dbt
        run: dbt run --target prod
```

---

## 11. Cost Estimation

### 11.1 MVP Cost Breakdown (Single Tenant)

| Service | Tier | Monthly Cost | Notes |
|---------|------|--------------|-------|
| **Snowflake** | Standard | $50-100 | ~10 credits/day, auto-suspend |
| **Fivetran** | Standard | $100-200 | 5 connectors (GA4, GAds, Meta, Klaviyo, Magento) |
| **Vercel** | Pro | $20 | Frontend hosting, edge functions |
| **Railway/Render** | Starter | $25-50 | FastAPI backend |
| **Redis Cloud** | Essentials | $0-10 | 30MB free tier |
| **Pinecone** | Starter | $0-70 | 1M vectors free, then $70/mo |
| **Anthropic API** | Pay-as-go | $20-50 | ~1000 thought generations/month |
| **ElevenLabs** | Starter | $5-22 | TTS for video agent |
| **D-ID/HeyGen** | Starter | $0-50 | Video avatar (trial/starter) |
| **Domain + SSL** | - | $15 | Annual, amortized |

**Total MVP (Monthly): $235-595**

### 11.2 Production Cost Breakdown (Multi-Tenant, 10 Clients)

| Service | Tier | Monthly Cost | Notes |
|---------|------|--------------|-------|
| **Snowflake** | Enterprise | $300-500 | ~100 credits/day, multi-tenant |
| **Fivetran** | Business | $400-600 | 50 connectors, 10 clients × 5 sources |
| **AWS ECS/EKS** | Production | $150-300 | 2-4 containers, auto-scaling |
| **AWS ElastiCache** | r6g.large | $100-150 | Redis cluster |
| **AWS RDS PostgreSQL** | db.t3.medium | $50-80 | Operational database |
| **Pinecone** | Standard | $70-200 | 5-20M vectors |
| **Anthropic API** | Pay-as-go | $100-300 | ~10K thought generations/month |
| **ElevenLabs** | Creator | $22-50 | Higher usage |
| **D-ID/HeyGen** | Business | $100-200 | Higher video minutes |
| **AWS CloudFront** | Standard | $20-50 | CDN for frontend |
| **Monitoring (DataDog)** | Pro | $50-100 | APM + logs |

**Total Production (Monthly): $1,362-2,530**

### 11.3 Cost Optimization Strategies

```yaml
optimization_strategies:
  snowflake:
    - Auto-suspend after 1 minute idle
    - Use XS warehouse for most queries
    - Schedule heavy dbt runs during off-peak
    - Materialized views for dashboard queries

  fivetran:
    - Sync 3-4x daily (not hourly)
    - Use incremental syncs where possible
    - Archive unused connectors

  ai_costs:
    - Cache repeated thought patterns
    - Batch similar queries
    - Use Haiku for classification, Sonnet for generation
    - Max 2x/day action updates (not real-time)

  infrastructure:
    - Spot instances for workers
    - Right-size containers based on usage
    - CDN caching for static assets
    - Redis key expiration policies
```

---

## 12. Performance & Testing Strategy

### 12.1 Caching Strategy

```
┌─────────────────────────────────────────────────────────────────┐
│                    CACHING LAYERS                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ L1: Browser Cache (Client)                                  ││
│  │   - Static assets: 1 year                                   ││
│  │   - API responses: stale-while-revalidate                   ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                   │
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ L2: CDN Cache (CloudFront/Vercel Edge)                      ││
│  │   - Dashboard HTML: 5 min                                   ││
│  │   - API: pass-through with cache headers                    ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                   │
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ L3: Redis Cache (Application)                               ││
│  │   - Session: 30 min                                         ││
│  │   - Metric values: 1-5 min                                  ││
│  │   - Thoughtlet data: 5 min                                  ││
│  │   - AI responses: 15 min                                    ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                   │
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ L4: Snowflake Result Cache                                  ││
│  │   - Automatic query result caching                          ││
│  │   - Valid until underlying data changes                     ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 12.2 Performance Targets

| Metric | Target | Measurement |
|--------|--------|-------------|
| Dashboard load (P95) | < 2s | Time to interactive |
| API response (P95) | < 500ms | For cached queries |
| API response (P95) | < 2s | For Snowflake queries |
| AI thought generation | < 5s | From trigger to complete |
| Video agent response | < 3s | First word spoken |
| WebSocket latency | < 100ms | Message delivery |

### 12.3 Testing Pyramid

```
                    ┌─────────────┐
                    │   E2E (10%) │  Playwright, Cypress
                    │   UI Tests  │  Critical user journeys
                    └──────┬──────┘
                           │
                    ┌──────┴──────┐
                    │ Integration │  API + DB tests
                    │   (20%)     │  pytest + testcontainers
                    └──────┬──────┘
                           │
              ┌────────────┴────────────┐
              │      Unit Tests (70%)   │  pytest, vitest
              │  Services, Utils, Hooks │  Mock external deps
              └─────────────────────────┘
```

### 12.4 Test Categories

```python
# Unit Tests (Fast, Isolated)
tests/
├── unit/
│   ├── services/
│   │   ├── test_metric_service.py
│   │   ├── test_threshold_engine.py
│   │   └── test_blast_radius.py
│   ├── utils/
│   └── models/

# Integration Tests (With Real DBs)
├── integration/
│   ├── test_snowflake_queries.py
│   ├── test_redis_cache.py
│   ├── test_api_endpoints.py
│   └── test_thought_generation.py

# E2E Tests (Full System)
├── e2e/
│   ├── test_login_flow.py
│   ├── test_dashboard_navigation.py
│   ├── test_video_agent_chat.py
│   └── test_action_execution.py

# Data Quality Tests (dbt)
dbt/tests/
├── schema_tests.yml          # not_null, unique, relationships
├── custom/
│   ├── test_no_negative_spend.sql
│   ├── test_date_continuity.sql
│   └── test_metric_bounds.sql
```

### 12.5 Load Testing

```yaml
# k6 Load Test Configuration
scenarios:
  dashboard_load:
    executor: ramping-vus
    stages:
      - duration: 1m, target: 10    # Warm up
      - duration: 5m, target: 50    # Normal load
      - duration: 2m, target: 100   # Peak load
      - duration: 1m, target: 0     # Cool down

  api_stress:
    executor: constant-arrival-rate
    rate: 100                        # 100 RPS
    duration: 5m
    preAllocatedVUs: 50

thresholds:
  http_req_duration: ['p(95)<2000']  # 95% under 2s
  http_req_failed: ['rate<0.01']     # <1% error rate
```

### 12.6 Monitoring & Alerting

```yaml
# Key Metrics to Monitor
application:
  - request_latency_p95
  - error_rate
  - active_users
  - thought_generation_time
  - cache_hit_ratio

infrastructure:
  - cpu_utilization
  - memory_usage
  - redis_connections
  - snowflake_credit_usage

business:
  - daily_active_users
  - thoughts_generated
  - actions_executed
  - agent_conversations

# Alert Thresholds
alerts:
  - name: High Error Rate
    condition: error_rate > 5%
    severity: critical

  - name: Slow API Response
    condition: p95_latency > 3s
    severity: warning

  - name: Snowflake Credit Spike
    condition: credits_used > 50/day
    severity: warning
```

---

## Appendix

### A. Database Connection Strings

```bash
# Snowflake (via environment variables)
SNOWFLAKE_ACCOUNT=xxx.us-east-1
SNOWFLAKE_USER=SERVICE_ACCOUNT
SNOWFLAKE_PASSWORD=<from-secrets-manager>
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
SNOWFLAKE_DATABASE=CLIENT_${TENANT}_DB
SNOWFLAKE_SCHEMA=PUBLIC

# Redis
REDIS_URL=redis://elasticache-cluster:6379/0

# API Keys
ANTHROPIC_API_KEY=<from-secrets-manager>
FIVETRAN_API_KEY=<from-secrets-manager>
```

### B. Related Documentation

- [Product Requirements](./PRODUCT_REQUIREMENTS.md) - Functional specifications
- [Dashboard Mapping](./AGENT_DASHBOARD_MAPPING.md) - Dashboard definitions
- [dbt Schema](../dbt/models/marts/schema.yml) - Data model definitions

---

## Appendix C: Key Architecture Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Operational DB | PostgreSQL + SQLModel | Fast lookups, no raw SQL, type-safe ORM |
| Analytical DB | Snowflake + dbt views | Complex queries encapsulated in dbt, API queries simple views |
| Vector DB | Pinecone/Weaviate | Video agent Q&A, semantic search for MVP |
| API Design | Hybrid REST + Batch | Individual endpoints for KG, batch for dashboards |
| Auth | NextAuth.js + PostgreSQL | Native Next.js integration, session in DB |
| Thought Generation | Anthropic Python SDK | Deterministic, predictable cost, you control context |
| Video Agent Q&A | Claude Agent SDK | Interactive, multi-step reasoning with tools |
| Data Refresh | 3-4x daily via Fivetran | Event-driven: Fivetran → dbt → Threshold → Thought |
| Action Updates | Max 2x/day | Avoid unnecessary AI calls, cost control |
| Multi-tenant | Single-tenant MVP | Simplify first, add tenant isolation later |

---

*Last Updated: December 2024*
*Version: 1.3 - Added cost estimation, performance/testing strategy, 7-layer security model, single-source metric pattern*
