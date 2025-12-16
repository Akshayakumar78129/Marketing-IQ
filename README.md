# Marketing IQ

AI-enabled multi-tenant marketing analytics platform with 18 dashboards (12 AI agents + 6 platform views).

## Technology Stack

| Layer | Technology |
|-------|------------|
| **Data Extraction** | Fivetran (managed ETL) |
| **Data Warehouse** | Snowflake |
| **Transformations** | DBT (21 dimensions + 22 facts) |
| **Backend** | FastAPI + Python 3.11 |
| **App Database** | PostgreSQL (Supabase) |
| **Cache** | Redis |
| **Frontend** | Next.js 14 + React + TypeScript + Tailwind |
| **Infrastructure** | Azure Container Apps + Terraform |
| **AI (Future)** | LangChain / CrewAI |

## Project Structure

```
marketing-iq/
├── backend/              # FastAPI application
│   ├── app/
│   │   ├── api/v1/       # API endpoints
│   │   ├── services/     # Business logic
│   │   ├── repositories/ # Data access (PyPika)
│   │   ├── cache/        # Redis caching
│   │   └── db/           # Database connections
│   └── tests/
├── dbt/                  # DBT transformations
│   ├── models/
│   │   ├── staging/      # Clean Fivetran data
│   │   ├── intermediate/ # Business logic
│   │   └── marts/        # Fact & Dimension tables
│   └── tests/
├── frontend/             # Next.js 14 app
│   ├── src/
│   │   ├── app/          # App router
│   │   ├── components/   # UI components
│   │   └── hooks/        # Custom hooks
├── database/             # PostgreSQL schemas
├── terraform/            # Infrastructure as Code
├── docs/                 # Documentation
└── docker-compose.yml    # Local development
```

## Data Sources

| Platform | Coverage | Data |
|----------|----------|------|
| Google Ads | 98% | Campaigns, Ad Groups, Ads, Keywords, Search Terms |
| Facebook Ads | 95% | Campaigns, Ad Sets, Ads, Video, Reactions |
| GA4 | 85% | Traffic, Conversions, E-commerce |
| Klaviyo | 98% | Campaigns, Flows, Segments, Lists |

## Quick Start (Local Development)

```bash
# 1. Start local services (Postgres, Redis)
docker-compose up -d

# 2. Set up backend
cd backend
python -m venv venv
.\venv\Scripts\activate  # Windows
pip install -r requirements.txt

# 3. Run API
uvicorn app.main:app --reload

# 4. Access API docs
http://localhost:8000/api/docs

# 5. Run DBT (requires Snowflake connection)
cd ../dbt
dbt run
```

## Documentation

| Document | Description |
|----------|-------------|
| `docs/PROJECT_STANDARDS.md` | Coding rules - MUST follow |
| `docs/IMPLEMENTATION_PLAN.md` | Implementation phases |
| `docs/AGENT_DASHBOARD_MAPPING.md` | 18 dashboards specs |
| `docs/ARCHITECTURE_FIVETRAN.md` | Detailed architecture |

## Dashboards (18 Total)

**AI Agent Dashboards (12):**
1. Performance Anomaly Detection
2. CTR/CVR Prediction
3. Budget Optimizer
4. Creative Testing
5. Audience & LTV Analysis
6. Action Ranker
7. Ad Copy Refresh
8. Keyword Expansion
9. Landing Page Intelligence
10. Tracking & Attribution Health
11. Competitor Watch
12. Seasonal Predictor

**Platform Dashboards (6):**
13. GA4 Dashboard
14. Google Ads Dashboard
15. Meta Ads Dashboard
16. Klaviyo Dashboard
17. Magento Dashboard
18. Overall Dashboard

## Key Architecture Decisions

- **No raw SQL in app code** - Use Repository Pattern + PyPika
- **No custom ETL** - Fivetran handles all data ingestion
- **DBT for transformations** - Version-controlled, testable
- **Unified API** - Single `/api/v1/metrics` endpoint for all dashboards
- **Tenant isolation** - Every query filtered by tenant_id

## Environments

| Environment | Infrastructure |
|-------------|----------------|
| Local | Docker-compose (Postgres, Redis) |
| Staging | Azure Container Apps |
| Production | Azure Container Apps |

## Contributing

1. Create feature branch
2. Follow `docs/PROJECT_STANDARDS.md`
3. Test locally
4. Create Pull Request
5. Merge to main
