# Marketing IQ - Star Schema Design Plan

## Overview
Design a comprehensive star schema data warehouse for marketing analytics, unifying data from Google Ads, Facebook Ads, and GA4 stored in Snowflake (CLIENT_RARE_SEEDS_DB).

## Requirements
- **Grain**: Both daily and hourly (where available)
- **Unification**: Both platform-specific AND unified cross-platform views
- **Metrics**: All KPIs - ROAS, CPA, Conversions, Engagement, Traffic
- **History**: Full SCD Type 2 tracking for all dimension changes

---

## Source Data Summary

### Google Ads (88 tables, 62 with data)
| Table Type | Tables | Grain | Key Metrics |
|------------|--------|-------|-------------|
| Stats | CAMPAIGN_STATS, AD_GROUP_STATS, AD_STATS | Daily | impressions, clicks, cost_micros, conversions, conversions_value |
| Hourly Stats | CAMPAIGN_HOURLY_STATS, AD_GROUP_HOURLY_STATS | Hourly | Same + CTR, CPC, CPM pre-calculated |
| History | CAMPAIGN_HISTORY, AD_GROUP_HISTORY, AD_HISTORY, ACCOUNT_HISTORY | SCD2 | _FIVETRAN_START/_END/_ACTIVE |

### Facebook Ads (97 tables, all with data)
| Table Type | Tables | Grain | Key Metrics |
|------------|--------|-------|-------------|
| Stats | BASIC_AD, BASIC_CAMPAIGN, BASIC_AD_SET | Daily | impressions, reach, spend, inline_link_clicks, cpc, cpm, ctr, frequency |
| Actions | BASIC_AD_ACTIONS, BASIC_CAMPAIGN_ACTIONS | Daily | action_type, value, 7d_click, 1d_view |
| History | CAMPAIGN_HISTORY, AD_SET_HISTORY, AD_HISTORY, ACCOUNT_HISTORY | SCD2 | UPDATED_TIME versioning |

### GA4 (52 tables, all with data)
| Table Type | Tables | Grain | Key Metrics |
|------------|--------|-------|-------------|
| Traffic | TRAFFIC_ACQUISITION_SESSION_SOURCE_MEDIUM_REPORT | Daily | sessions, users, engaged_sessions, revenue |
| Conversions | CONVERSIONS_REPORT, EVENTS_REPORT | Daily | key_events, total_revenue, event_count |
| Demographics | DEMOGRAPHIC_COUNTRY_REPORT, DEMOGRAPHIC_REGION_REPORT | Daily | users, sessions by geo |
| Metadata | PROPERTIES, ACCOUNTS, CONVERSION_EVENTS | Reference | property config |

---

## Star Schema Design

### Dimension Tables

#### 1. dim_date (Create New)
```sql
- date_key (YYYYMMDD integer) -- Primary Key
- full_date (DATE)
- day_of_week (1-7)
- day_name (Monday, Tuesday...)
- day_of_month (1-31)
- day_of_year (1-366)
- week_of_year (1-53)
- month_number (1-12)
- month_name (January...)
- quarter (1-4)
- year (YYYY)
- is_weekend (boolean)
- fiscal_year, fiscal_quarter (if needed)
```

#### 2. dim_hour (Create New)
```sql
- hour_key (0-23) -- Primary Key
- hour_12 (1-12)
- am_pm (AM/PM)
- hour_bucket (Morning, Afternoon, Evening, Night)
```

#### 3. dim_platform (Create New)
```sql
- platform_key (surrogate) -- Primary Key
- platform_code (GOOGLE_ADS, FACEBOOK_ADS, GA4)
- platform_name (Google Ads, Facebook Ads, Google Analytics 4)
```

#### 4. dim_account (SCD Type 2)
```sql
- account_key (surrogate) -- Primary Key
- platform_account_id (original ID)
- platform_key (FK to dim_platform)
- account_name
- currency_code
- timezone
-- Google specific
- is_manager_account
-- Facebook specific
- business_name
-- SCD2 tracking
- effective_from (TIMESTAMP)
- effective_to (TIMESTAMP)
- is_current (BOOLEAN)
```
**Source**: GOOGLE_ADS.ACCOUNT_HISTORY, FACEBOOK_ADS.ACCOUNT_HISTORY, GA4.ACCOUNTS

#### 5. dim_campaign (SCD Type 2)
```sql
- campaign_key (surrogate) -- Primary Key
- platform_campaign_id (original ID)
- platform_key (FK to dim_platform)
- account_key (FK to dim_account)
- campaign_name
- campaign_status (ENABLED, PAUSED, REMOVED/ACTIVE, ARCHIVED)
-- Google specific
- advertising_channel_type (SEARCH, DISPLAY, SHOPPING, VIDEO)
- advertising_channel_subtype
-- Facebook specific
- objective (CONVERSIONS, TRAFFIC, AWARENESS...)
- bid_strategy
- buying_type
- daily_budget
- lifetime_budget
-- SCD2 tracking
- effective_from (TIMESTAMP)
- effective_to (TIMESTAMP)
- is_current (BOOLEAN)
```
**Source**: GOOGLE_ADS.CAMPAIGN_HISTORY, FACEBOOK_ADS.CAMPAIGN_HISTORY

#### 6. dim_ad_group (SCD Type 2)
*Note: Maps to Google Ads "Ad Groups" and Facebook "Ad Sets"*
```sql
- ad_group_key (surrogate) -- Primary Key
- platform_ad_group_id (original ID)
- platform_key (FK to dim_platform)
- campaign_key (FK to dim_campaign)
- ad_group_name
- ad_group_status
- ad_group_type
-- Facebook specific (Ad Set)
- optimization_goal
- billing_event
- targeting_json (VARIANT - store complex targeting as JSON)
-- SCD2 tracking
- effective_from (TIMESTAMP)
- effective_to (TIMESTAMP)
- is_current (BOOLEAN)
```
**Source**: GOOGLE_ADS.AD_GROUP_HISTORY, FACEBOOK_ADS.AD_SET_HISTORY

#### 7. dim_ad (SCD Type 2)
```sql
- ad_key (surrogate) -- Primary Key
- platform_ad_id (original ID)
- platform_key (FK to dim_platform)
- ad_group_key (FK to dim_ad_group)
- ad_name
- ad_status
- ad_type (RESPONSIVE_SEARCH, RESPONSIVE_DISPLAY, IMAGE, VIDEO...)
-- Google specific
- ad_strength
- final_urls
-- Facebook specific
- creative_id
-- SCD2 tracking
- effective_from (TIMESTAMP)
- effective_to (TIMESTAMP)
- is_current (BOOLEAN)
```
**Source**: GOOGLE_ADS.AD_HISTORY, FACEBOOK_ADS.AD_HISTORY

#### 8. dim_device (Create New - Conformed)
```sql
- device_key (surrogate) -- Primary Key
- device_code (MOBILE, DESKTOP, TABLET, CONNECTED_TV, OTHER)
- device_name
```

#### 9. dim_ad_network (Google Ads Specific)
```sql
- ad_network_key (surrogate) -- Primary Key
- ad_network_type (SEARCH, DISPLAY, YOUTUBE_WATCH, YOUTUBE_SEARCH, SHOPPING...)
```

#### 10. dim_geography (Conformed)
```sql
- geography_key (surrogate) -- Primary Key
- country_code
- country_name
- region_code
- region_name
- city_name (if available)
- dma_region (Facebook DMA)
```
**Source**: GOOGLE_ADS.GEO_TARGET, GA4 demographics, Facebook demographics

#### 11. dim_source_medium (GA4)
```sql
- source_medium_key (surrogate) -- Primary Key
- source (google, facebook, direct...)
- medium (cpc, organic, referral, email...)
- source_medium_combined (source / medium)
- default_channel_grouping
```

#### 12. dim_ga4_property
```sql
- property_key (surrogate) -- Primary Key
- property_id (original GA4 property ID)
- property_name
- account_id
- timezone
- currency_code
- industry_category
```
**Source**: GA4.PROPERTIES

#### 13. dim_conversion_action (Conformed)
```sql
- conversion_key (surrogate) -- Primary Key
- platform_key (FK to dim_platform)
- action_type_code (purchase, add_to_cart, lead, page_view...)
- action_type_name
- is_primary_conversion (BOOLEAN)
```
**Source**: GA4.CONVERSION_EVENTS, Facebook action_types, Google conversion actions

---

### Fact Tables

#### 1. fact_campaign_performance_daily (Unified Cross-Platform)
```sql
-- Keys
- date_key (FK to dim_date)
- platform_key (FK to dim_platform)
- account_key (FK to dim_account)
- campaign_key (FK to dim_campaign)
- device_key (FK to dim_device)

-- Metrics (common across platforms)
- impressions (NUMBER)
- clicks (NUMBER)
- spend (FLOAT) -- Normalized to dollars
- conversions (FLOAT)
- conversion_value (FLOAT)
- reach (NUMBER) -- FB only, NULL for Google
- frequency (FLOAT) -- FB only, NULL for Google

-- Calculated fields (derived at load time)
- ctr (FLOAT) -- clicks/impressions
- cpc (FLOAT) -- spend/clicks
- cpm (FLOAT) -- spend/impressions * 1000
- conversion_rate (FLOAT) -- conversions/clicks
- roas (FLOAT) -- conversion_value/spend
- cost_per_conversion (FLOAT) -- spend/conversions
```
**Source**: GOOGLE_ADS.CAMPAIGN_STATS + FACEBOOK_ADS.BASIC_CAMPAIGN

#### 2. fact_ad_group_performance_daily (Unified)
```sql
-- Keys
- date_key (FK to dim_date)
- platform_key (FK to dim_platform)
- campaign_key (FK to dim_campaign)
- ad_group_key (FK to dim_ad_group)
- device_key (FK to dim_device)
- ad_network_key (FK to dim_ad_network) -- Google only, NULL for FB

-- Same metrics as campaign level
- impressions, clicks, spend, conversions, conversion_value
- reach, frequency -- FB only
- ctr, cpc, cpm, conversion_rate, roas, cost_per_conversion
```
**Source**: GOOGLE_ADS.AD_GROUP_STATS + FACEBOOK_ADS.BASIC_AD_SET

#### 3. fact_ad_performance_daily (Unified)
```sql
-- Keys
- date_key (FK to dim_date)
- platform_key (FK to dim_platform)
- campaign_key (FK to dim_campaign)
- ad_group_key (FK to dim_ad_group)
- ad_key (FK to dim_ad)
- device_key (FK to dim_device)

-- Same metrics as campaign level
- impressions, clicks, spend, conversions, conversion_value
- reach, frequency -- FB only
- ctr, cpc, cpm, conversion_rate, roas, cost_per_conversion
```
**Source**: GOOGLE_ADS.AD_STATS + FACEBOOK_ADS.BASIC_AD

#### 4. fact_campaign_performance_hourly (Google Ads Only)
```sql
-- Keys
- date_key (FK to dim_date)
- hour_key (FK to dim_hour)
- platform_key (FK to dim_platform)
- campaign_key (FK to dim_campaign)
- device_key (FK to dim_device)

-- Same metrics
- impressions, clicks, spend, conversions, conversion_value
- ctr, cpc, cpm, conversion_rate, roas, cost_per_conversion
```
**Source**: GOOGLE_ADS.CAMPAIGN_HOURLY_STATS
*Note: Facebook doesn't provide hourly data in Fivetran export*

#### 5. fact_ad_group_performance_hourly (Google Ads Only)
```sql
-- Keys
- date_key (FK to dim_date)
- hour_key (FK to dim_hour)
- platform_key (FK to dim_platform)
- campaign_key (FK to dim_campaign)
- ad_group_key (FK to dim_ad_group)
- device_key (FK to dim_device)

-- Same metrics
- impressions, clicks, spend, conversions, conversion_value
- ctr, cpc, cpm, conversion_rate, roas, cost_per_conversion
```
**Source**: GOOGLE_ADS.AD_GROUP_HOURLY_STATS

#### 6. fact_conversions_daily (Platform-Specific Detail)
```sql
-- Keys
- date_key (FK to dim_date)
- platform_key (FK to dim_platform)
- account_key (FK to dim_account)
- campaign_key (FK to dim_campaign)
- ad_group_key (FK to dim_ad_group) -- nullable
- ad_key (FK to dim_ad) -- nullable
- conversion_key (FK to dim_conversion_action)

-- Metrics
- conversions (FLOAT)
- conversion_value (FLOAT)
- view_through_conversions (NUMBER) -- Google only
- click_7d_conversions (FLOAT) -- Facebook 7-day click attribution
- view_1d_conversions (FLOAT) -- Facebook 1-day view attribution
```
**Source**: GOOGLE_ADS conversion data, FACEBOOK_ADS.BASIC_*_ACTIONS

#### 7. fact_ga4_sessions_daily
```sql
-- Keys
- date_key (FK to dim_date)
- property_key (FK to dim_ga4_property)
- source_medium_key (FK to dim_source_medium)
- geography_key (FK to dim_geography) -- nullable

-- Metrics
- sessions (NUMBER)
- total_users (NUMBER)
- new_users (NUMBER)
- engaged_sessions (NUMBER)
- engagement_rate (FLOAT)
- event_count (NUMBER)
- events_per_session (FLOAT)
- user_engagement_duration (FLOAT) -- seconds
- total_revenue (FLOAT)
- key_events (FLOAT)
```
**Source**: GA4.TRAFFIC_ACQUISITION_SESSION_SOURCE_MEDIUM_REPORT + demographics

#### 8. fact_ga4_conversions_daily
```sql
-- Keys
- date_key (FK to dim_date)
- property_key (FK to dim_ga4_property)
- conversion_key (FK to dim_conversion_action)

-- Metrics
- total_users (NUMBER)
- key_events (FLOAT)
- total_revenue (FLOAT)
```
**Source**: GA4.CONVERSIONS_REPORT

---

## Implementation Phases

### Phase 1: Foundation - Dimension Tables
Create all dimension tables with proper surrogate keys and SCD Type 2 structure.

**Order of creation:**
1. dim_date (no dependencies)
2. dim_hour (no dependencies)
3. dim_platform (no dependencies)
4. dim_device (no dependencies)
5. dim_ad_network (no dependencies)
6. dim_account (depends on dim_platform)
7. dim_campaign (depends on dim_platform, dim_account)
8. dim_ad_group (depends on dim_campaign)
9. dim_ad (depends on dim_ad_group)
10. dim_geography (no dependencies)
11. dim_source_medium (no dependencies)
12. dim_ga4_property (no dependencies)
13. dim_conversion_action (depends on dim_platform)

### Phase 2: Core Fact Tables
Create the main performance fact tables.

**Order of creation:**
1. fact_campaign_performance_daily
2. fact_ad_group_performance_daily
3. fact_ad_performance_daily

### Phase 3: Hourly & Specialized Facts
1. fact_campaign_performance_hourly
2. fact_ad_group_performance_hourly
3. fact_conversions_daily

### Phase 4: GA4 Integration
1. fact_ga4_sessions_daily
2. fact_ga4_conversions_daily

### Phase 5: Views & Reporting Layer
Create unified views that join fact + dimension tables for easy querying.

---

## Schema Location
All tables will be created in: `CLIENT_RARE_SEEDS_DB.ANALYTICS` (new schema)

## Implementation Approach (Confirmed)
- **Schema**: `CLIENT_RARE_SEEDS_DB.ANALYTICS`
- **Method**: Create SQL files in `database/` folder AND execute them in Snowflake
- **Rollout**: Full schema at once (all dimensions, facts, and views)

## Key Design Decisions

1. **Surrogate Keys**: All dimension tables use integer surrogate keys for joins (faster than varchar)

2. **Cost Normalization**: Google Ads stores COST_MICROS (divide by 1,000,000), Facebook stores SPEND directly - normalize to dollars

3. **SCD Type 2**: Using effective_from/effective_to/is_current pattern for history tracking

4. **Conformed Dimensions**: dim_date, dim_device, dim_platform shared across all facts

5. **NULL handling**: Platform-specific metrics (reach, frequency for FB) will be NULL for other platforms

6. **Grain consistency**: Daily facts are strictly one row per entity per day per relevant dimensions

---

## Files to Create

```
database/
├── schemas/
│   └── analytics_schema.sql          -- CREATE SCHEMA
├── dimensions/
│   ├── dim_date.sql
│   ├── dim_hour.sql
│   ├── dim_platform.sql
│   ├── dim_device.sql
│   ├── dim_ad_network.sql
│   ├── dim_account.sql
│   ├── dim_campaign.sql
│   ├── dim_ad_group.sql
│   ├── dim_ad.sql
│   ├── dim_geography.sql
│   ├── dim_source_medium.sql
│   ├── dim_ga4_property.sql
│   └── dim_conversion_action.sql
├── facts/
│   ├── fact_campaign_performance_daily.sql
│   ├── fact_ad_group_performance_daily.sql
│   ├── fact_ad_performance_daily.sql
│   ├── fact_campaign_performance_hourly.sql
│   ├── fact_ad_group_performance_hourly.sql
│   ├── fact_conversions_daily.sql
│   ├── fact_ga4_sessions_daily.sql
│   └── fact_ga4_conversions_daily.sql
└── views/
    ├── v_campaign_performance_unified.sql
    ├── v_daily_spend_by_platform.sql
    └── v_roas_by_campaign.sql
```

---

## Entity Relationship Diagram

```
                    ┌─────────────────┐
                    │   dim_date      │
                    └────────┬────────┘
                             │
┌─────────────────┐          │          ┌─────────────────┐
│   dim_hour      │          │          │  dim_platform   │
└────────┬────────┘          │          └────────┬────────┘
         │                   │                   │
         │    ┌──────────────┼──────────────┐    │
         │    │              │              │    │
         ▼    ▼              ▼              ▼    ▼
    ┌─────────────────────────────────────────────────┐
    │          FACT TABLES (Daily & Hourly)           │
    │  fact_campaign_performance_daily                │
    │  fact_ad_group_performance_daily                │
    │  fact_ad_performance_daily                      │
    │  fact_campaign_performance_hourly               │
    │  fact_ad_group_performance_hourly               │
    │  fact_conversions_daily                         │
    │  fact_ga4_sessions_daily                        │
    │  fact_ga4_conversions_daily                     │
    └─────────────────────────────────────────────────┘
         ▲    ▲              ▲              ▲    ▲
         │    │              │              │    │
         │    └──────────────┼──────────────┘    │
         │                   │                   │
┌────────┴────────┐          │          ┌───────┴─────────┐
│   dim_device    │          │          │  dim_ad_network │
└─────────────────┘          │          └─────────────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
        ┌──────────┐   ┌──────────┐   ┌──────────┐
        │dim_account│──▶│dim_campaign│──▶│dim_ad_group│──▶ dim_ad
        └──────────┘   └──────────┘   └──────────┘

        ┌─────────────────┐    ┌─────────────────────┐
        │ dim_geography   │    │ dim_conversion_action│
        └─────────────────┘    └─────────────────────┘

        ┌─────────────────┐    ┌─────────────────────┐
        │dim_source_medium│    │   dim_ga4_property  │
        └─────────────────┘    └─────────────────────┘
```

---

## Data Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                         SOURCE LAYER                            │
│  (Fivetran-synced raw data in GA4, GOOGLE_ADS, FACEBOOK_ADS)   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      STAGING/TRANSFORM                          │
│        (SQL transformations to normalize & unify data)          │
│                                                                 │
│  • Normalize cost (COST_MICROS / 1M → dollars)                 │
│  • Map platform IDs to surrogate keys                          │
│  • Apply SCD Type 2 logic for dimensions                       │
│  • Calculate derived metrics (CTR, CPC, ROAS)                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    ANALYTICS SCHEMA                             │
│              (Star Schema in ANALYTICS schema)                  │
│                                                                 │
│   ┌─────────────┐        ┌─────────────┐                       │
│   │ DIMENSIONS  │        │    FACTS    │                       │
│   │ (13 tables) │───────▶│ (8 tables)  │                       │
│   └─────────────┘        └─────────────┘                       │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      REPORTING VIEWS                            │
│          (Pre-joined views for easy consumption)                │
│                                                                 │
│  • v_campaign_performance_unified                              │
│  • v_daily_spend_by_platform                                   │
│  • v_roas_by_campaign                                          │
└─────────────────────────────────────────────────────────────────┘
```
