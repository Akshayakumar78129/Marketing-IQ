# Marketing IQ - DBT Project

Data transformations for the Marketing IQ analytics platform.

## Overview

This DBT project uses Fivetran pre-built packages to transform raw marketing data into unified analytics tables.

### Data Sources (Fivetran)
- **Google Ads** → Campaign, Ad Group, Ad, Keyword reports
- **Facebook Ads** → Campaign, Ad Set, Ad reports

### Output Tables
- **2 Fact Tables** - Unified cross-platform performance
- **2 Dimension Tables** - Date and Platform lookups

## Project Structure

```
dbt/
├── models/
│   └── marts/
│       ├── core/
│       │   ├── fct_campaign_performance.sql  # Unified campaigns
│       │   └── fct_ad_performance.sql        # Unified ads
│       ├── dimensions/
│       │   ├── dim_date.sql                  # Date dimension
│       │   └── dim_platform.sql              # Platform lookup
│       └── schema.yml                        # Tests & docs
├── seeds/
│   └── seed_platforms.csv                    # Platform definitions
├── dbt_packages/                             # Fivetran packages
├── dbt_project.yml
├── profiles.yml
└── packages.yml
```

## Quick Start

```bash
# 1. Set environment variables (or use .env file)
export SNOWFLAKE_ACCOUNT=your_account
export SNOWFLAKE_USER=your_user
export SNOWFLAKE_PASSWORD=your_password
export SNOWFLAKE_WAREHOUSE=COMPUTE_WH
export SNOWFLAKE_ROLE=TRANSFORMER

# 2. Install dependencies
dbt deps

# 3. Test connection
dbt debug

# 4. Run seeds
dbt seed

# 5. Run all models
dbt run

# 6. Run tests
dbt test
```

## Output Tables

### Fact Tables (PUBLIC_ANALYTICS schema)
| Table | Rows | Description |
|-------|------|-------------|
| fct_campaign_performance | 24K+ | Google Ads + Meta campaigns unified |
| fct_ad_performance | 37K+ | Google Ads + Meta ads unified |

### Dimension Tables
| Table | Rows | Description |
|-------|------|-------------|
| dim_date | 1,443 | Calendar (2023-2026) |
| dim_platform | 5 | Platform lookup |

### Fivetran Package Tables (also available)
- `google_ads__campaign_report`, `google_ads__ad_report`, etc.
- `facebook_ads__campaign_report`, `facebook_ads__ad_report`, etc.

## Calculated Metrics

The fact tables include these calculated fields:
- `ctr` - Click-through rate
- `cpc` - Cost per click
- `cpm` - Cost per 1000 impressions
- `roas` - Return on ad spend
- `cpa` - Cost per acquisition

## Commands

```bash
# Run all models
dbt run

# Run specific model
dbt run --select fct_campaign_performance

# Run tests
dbt test

# Generate documentation
dbt docs generate && dbt docs serve
```
