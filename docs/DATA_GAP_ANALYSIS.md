# Marketing IQ - Data Gap Analysis

## Overview

This document analyzes whether the existing DBT fact and dimension tables can provide all data required for the 13 dashboards defined in `AGENT_DASHBOARD_MAPPING.md`.

---

## Available Data Model

### Dimension Tables (21)
| Table | Description | Key Columns |
|-------|-------------|-------------|
| dim_date | Date dimension | date_day, day_of_week, month, quarter, year |
| dim_platform | Platform dimension | platform_name |
| dim_campaign | Google/Meta campaigns | campaign_id, campaign_name, status, daily_budget, objective |
| dim_ad_group | Google ad groups | ad_group_id, ad_group_name, status |
| dim_ad_set | Meta ad sets | ad_set_id, ad_set_name, status |
| dim_ad | Unified ads | ad_id, ad_name, ad_type, creative_id |
| dim_keyword | Google keywords | keyword_id, keyword_text, match_type, quality_score |
| dim_hour | Hour dimension | hour |
| dim_device | Device dimension | device_type, device_category |
| dim_geography | Geographic dimension | country, region, city |
| dim_source_medium | Traffic sources | source, medium, channel_grouping |
| dim_email_campaign | Klaviyo campaigns | campaign_id, campaign_name, subject_line |
| dim_email_flow | Klaviyo flows | flow_id, flow_name, trigger_type |
| dim_email_template | Email templates | template_id |
| dim_segment | Klaviyo segments | segment_id, segment_name |
| dim_list | Klaviyo lists | list_id, list_name, member_count |
| dim_audience | GA4 audiences | audience_name |
| dim_video | Video metadata | video_id, video_title, video_length |
| dim_account | Account dimension | account_id |
| dim_conversion_action | Conversion actions | conversion_action_id |
| dim_bidding_strategy | Bidding strategies | bidding_strategy_type |

### Fact Tables (22)
| Table | Grain | Key Metrics |
|-------|-------|-------------|
| fct_campaign_performance | Campaign × Date × Device | impressions, clicks, spend, conversions, conversion_value, ctr, cpc, roas, cpa |
| fct_ad_performance | Ad × Date × Device | impressions, clicks, spend, conversions, conversion_value |
| fct_ad_group_performance | Ad Group × Date × Device | impressions, clicks, spend, conversions, view_through_conversions |
| fct_ad_set_performance | Ad Set × Date | impressions, reach, clicks, spend, frequency |
| fct_keyword_performance | Keyword × Date × Device | impressions, clicks, spend, conversions, ctr, roas |
| fct_search_term | Search Term × Date | search_term, impressions, clicks, spend, top_impression_percentage |
| fct_campaign_hourly | Campaign × Hour × Date | hourly impressions, clicks, spend, conversions |
| fct_ga4_traffic | Source/Medium × Date | sessions, engaged_sessions, total_users, revenue, engagement_rate |
| fct_ga4_conversions | Conversion Event × Date | conversions, revenue, conversion_rate |
| fct_ecommerce_item | Item × Date | items_viewed, items_added_to_cart, items_purchased, revenue |
| fct_email_campaign | Campaign × Date | sent, opens, clicks, bounces, open_rate, click_rate |
| fct_email_flow | Flow × Date | sent, opens, clicks, conversions |
| fct_segment_membership | Segment × Person | membership status |
| fct_list_membership | List × Person | joined_at, is_active |
| fct_video_performance | Video | total_views, post_views |
| fct_ad_reactions | Ad × Date | impressions, reach, clicks |
| fct_demographics | Age/Gender × Date | total_users, new_users, conversions, revenue |
| fct_audience_performance | Audience × Date | sessions, new_users, active_users, revenue |
| fct_campaign_settings_history | Campaign changes | settings history |
| fct_ad_group_settings_history | Ad group changes | settings history |
| fct_bidding_changes | Bidding changes | strategy changes |
| fct_budget_changes | Budget changes | budget_amount, change_date |

---

## Dashboard-by-Dashboard Analysis

### Legend
- ✅ **Available** - Data exists in current tables
- ⚠️ **Partial** - Can be calculated or approximated
- ❌ **Missing** - Data not available, requires new integration

---

## Dashboard 1: Core Performance Metrics (A)

### Metrics Coverage
| Metric | Status | Source Table | Notes |
|--------|--------|--------------|-------|
| Conversions | ✅ | fct_campaign_performance | Available |
| Conversion Rate (CVR) | ✅ | Calculated | conversions / clicks |
| Cost per Conversion (CPA) | ✅ | fct_campaign_performance.cpa | Available |
| Conversion Value | ✅ | fct_campaign_performance.conversion_value | Available |
| Return on Ad Spend (ROAS) | ✅ | fct_campaign_performance.roas | Available |
| Click-Through Rate (CTR) | ✅ | fct_campaign_performance.ctr | Available |
| Cost per Click (CPC) | ✅ | fct_campaign_performance.cpc | Available |
| Impressions | ✅ | fct_campaign_performance.impressions | Available |
| Spend | ✅ | fct_campaign_performance.spend | Available |
| Revenue | ✅ | fct_ga4_conversions.revenue | Available |

### Filters Coverage
| Filter | Status | Source |
|--------|--------|--------|
| Date Range | ✅ | dim_date |
| Period Comparison | ✅ | dim_date (calculated) |
| Campaigns | ✅ | dim_campaign |
| Channels | ✅ | dim_source_medium.channel_grouping |
| Forecast Period | ⚠️ | Requires forecasting model |
| Priority Level | ❌ | Not available - requires business logic |

### Status: ✅ GOOD (90% coverage)

---

## Dashboard 2: Spend & Budget Control (B)

### Metrics Coverage
| Metric | Status | Source Table | Notes |
|--------|--------|--------------|-------|
| Total Spend | ✅ | fct_campaign_performance.spend | Available |
| Spend by Campaign | ✅ | fct_campaign_performance | Group by campaign |
| Spend by Ad Group | ✅ | fct_ad_group_performance.spend | Available |
| Spend by Keyword | ✅ | fct_keyword_performance.spend | Available |
| Daily Budget Assigned | ✅ | dim_campaign.daily_budget, fct_budget_changes | Available |
| Daily Budget Utilized | ✅ | Calculated from spend | Available |
| Overspend/Underspend | ✅ | Calculated | spend - budget |
| Bid Strategy Type | ✅ | dim_bidding_strategy | Available |
| Marketing ROI | ⚠️ | Calculated | Needs consistent revenue source |
| Blended CAC | ❌ | Not available | Requires customer count from Magento/CRM |

### Status: ✅ GOOD (85% coverage)

**Gap:** Blended CAC requires customer acquisition data from Magento

---

## Dashboard 3: Audience & Behavioral (C)

### Metrics Coverage
| Metric | Status | Source Table | Notes |
|--------|--------|--------------|-------|
| Users/Sessions | ✅ | fct_ga4_traffic | total_users, sessions |
| New vs Returning | ⚠️ | fct_demographics.new_users | Returning not explicit |
| Device Type | ✅ | dim_device | Available |
| Country/Region | ✅ | dim_geography | Available |
| Time on Page | ⚠️ | fct_ga4_traffic.user_engagement_duration | Session-level, not page-level |
| Bounce Rate | ⚠️ | Calculated | 1 - engagement_rate (GA4 proxy) |
| Scroll Depth % | ❌ | Not available | Requires GA4 enhanced events |
| Entrance Page | ❌ | Not available | Need landing page report |
| Referrer / Traffic Source | ✅ | dim_source_medium | Available |
| Page Conversion Rate | ❌ | Not available | Need page-level conversion data |

### Status: ⚠️ PARTIAL (60% coverage)

**Gaps:**
1. Scroll Depth - Requires GA4 scroll events (enhanced measurement)
2. Entrance/Landing Page - Need `pages_report` or `landing_page_report` from GA4
3. Page Conversion Rate - Need page-level data joined with conversions

---

## Dashboard 4: Funnel & Attribution (D)

### Metrics Coverage
| Metric | Status | Source Table | Notes |
|--------|--------|--------------|-------|
| Session-to-Add-to-Cart Rate | ✅ | fct_ecommerce_item.cart_to_view_rate | Available |
| Session-to-Lead Form Start Rate | ❌ | Not available | Requires form event tracking |
| Lead Form Completion Rate | ❌ | Not available | Requires form event tracking |
| Purchase Conversion Event Count | ✅ | fct_ga4_conversions | Available |
| UTM Parameters Coverage % | ❌ | Not available | Requires UTM audit logic |
| Conversion Attribution Path | ❌ | Not available | No multi-touch attribution |
| Missing Conversion Events | ❌ | Not available | Requires tracking audit |
| Pixel Firing Success Rate | ❌ | Not available | Requires pixel monitoring |
| Attribution Revenue | ⚠️ | fct_ga4_conversions.revenue | No attribution model breakdown |
| Pipeline Value | ❌ | Not available | Requires CRM integration |

### Status: ❌ MAJOR GAPS (30% coverage)

**Critical Gaps:**
1. Multi-touch attribution - Not available in current data sources
2. Lead form tracking - Requires custom GA4 event setup
3. Pixel/tracking health - Requires external monitoring tool
4. Pipeline data - Requires CRM/Salesforce integration

---

## Dashboard 5: Creative & Messaging (E)

### Metrics Coverage
| Metric | Status | Source Table | Notes |
|--------|--------|--------------|-------|
| Headline | ❌ | Not available | Ad copy text not stored |
| Description | ❌ | Not available | Ad copy text not stored |
| Creative Asset ID | ✅ | dim_ad.creative_id | Meta only |
| Creative Type (img/video/rs) | ⚠️ | dim_ad.ad_type | Google Ads only |
| Impressions per Creative | ✅ | fct_ad_performance.impressions | Available |
| CTR per Creative | ✅ | fct_ad_performance.ctr | Available |
| CVR per Creative | ⚠️ | Calculated | conversions/clicks |
| Asset Fatigue Score | ❌ | Not available | Requires ML model |
| CTR Decay Rate | ❌ | Not available | Requires time-series calc |
| A/B Test Lift | ❌ | Not available | No A/B test framework |

### Status: ⚠️ PARTIAL (40% coverage)

**Gaps:**
1. Ad copy (headlines/descriptions) - Not in Fivetran schema by default
2. Fatigue scoring - Requires custom ML/calculation
3. A/B testing framework - Not available

---

## Dashboard 6: Search Intent & Keyword (F)

### Metrics Coverage
| Metric | Status | Source Table | Notes |
|--------|--------|--------------|-------|
| Keyword Text | ✅ | dim_keyword.keyword_text | Available |
| Match Type | ✅ | dim_keyword.match_type | Available |
| Search Term | ✅ | fct_search_term.search_term | Available |
| Search Volume | ❌ | Not available | Requires SEO tool (SEMrush/Ahrefs) |
| Click Share | ❌ | Not available | Not in Fivetran Google Ads |
| Impression Share | ❌ | Not available | Need campaign.search_impression_share |
| Top of Page Rate | ✅ | fct_search_term.top_impression_percentage | Available |
| Search Lost IS (Budget) | ❌ | Not available | Need search_budget_lost_* fields |
| Search Lost IS (Rank) | ❌ | Not available | Need search_rank_lost_* fields |
| Impression Share Lost to Competitors | ❌ | Not available | Competitive data |

### Status: ⚠️ PARTIAL (40% coverage)

**Gaps:**
1. Impression Share metrics - Need to verify if available in Google Ads source tables
2. Search Volume - External SEO tool required
3. Competitive metrics - Not available in standard Fivetran

---

## Dashboard 7: Revenue & LTV (G)

### Metrics Coverage
| Metric | Status | Source Table | Notes |
|--------|--------|--------------|-------|
| Revenue per User | ⚠️ | fct_audience_performance.revenue_per_user | Available but limited |
| First Purchase Value | ❌ | Not available | Requires Magento order history |
| Repeat Purchase Rate | ❌ | Not available | Requires Magento customer data |
| CLV/LTV | ❌ | Not available | Requires customer modeling |
| Time to 2nd Purchase | ❌ | Not available | Requires order history |
| Customer Cohort Labels | ❌ | Not available | Requires cohort logic |
| LTV/CAC Ratio | ❌ | Not available | No LTV or customer count |
| Churn Rate | ❌ | Not available | Requires subscription data |
| Lead Conversion Rate | ❌ | Not available | Requires CRM data |
| Seasonality Index | ⚠️ | Calculated | Can derive from historical data |

### Status: ❌ MAJOR GAPS (15% coverage)

**Critical Gaps:**
- **Magento Integration Required** - Most metrics need e-commerce order/customer data
- **CRM Integration Required** - Lead and pipeline metrics
- **Customer Data Platform** - LTV calculations need unified customer view

---

## Dashboard 8: Google Analytics 4 (GA4)

### Metrics Coverage
| Metric | Status | Source Table | Notes |
|--------|--------|--------------|-------|
| Total Users | ✅ | fct_ga4_traffic.total_users | Available |
| Sessions | ✅ | fct_ga4_traffic.sessions | Available |
| Engagement Rate | ✅ | fct_ga4_traffic.engagement_rate | Available |
| Avg Session Duration | ⚠️ | Calculated | user_engagement_duration / sessions |
| Bounce Rate | ⚠️ | Calculated | 1 - engagement_rate (GA4 proxy) |
| Page Views | ⚠️ | fct_ga4_traffic.event_count | Proxy metric |
| Conversions (Key Events) | ✅ | fct_ga4_conversions.conversions | Available |
| Conversion Rate | ✅ | fct_ga4_conversions.conversion_rate | Available |
| Revenue | ✅ | fct_ga4_conversions.revenue | Available |
| Avg Order Value | ⚠️ | Calculated | revenue / conversions |

### Filters Coverage
| Filter | Status | Source |
|--------|--------|--------|
| Date Range | ✅ | dim_date |
| Source/Medium | ✅ | dim_source_medium |
| Country/Region | ✅ | dim_geography |
| Device Category | ✅ | dim_device |
| Landing Page | ❌ | Not available |

### Status: ✅ GOOD (80% coverage)

**Gap:** Landing page filter requires additional GA4 report

---

## Dashboard 9: Google Ads

### Metrics Coverage
| Metric | Status | Source Table | Notes |
|--------|--------|--------------|-------|
| Impressions | ✅ | fct_campaign_performance | Available |
| Clicks | ✅ | fct_campaign_performance | Available |
| CTR | ✅ | fct_campaign_performance.ctr | Available |
| CPC | ✅ | fct_campaign_performance.cpc | Available |
| Spend | ✅ | fct_campaign_performance.spend | Available |
| Conversions | ✅ | fct_campaign_performance.conversions | Available |
| Conversion Value | ✅ | fct_campaign_performance.conversion_value | Available |
| Cost per Conversion | ✅ | fct_campaign_performance.cpa | Available |
| ROAS | ✅ | fct_campaign_performance.roas | Available |
| Impression Share | ❌ | Not available | Need campaign_stats.search_impression_share |

### Status: ✅ GOOD (90% coverage)

**Gap:** Impression Share - Check if available in source Google Ads tables

---

## Dashboard 10: Meta Ads (Facebook/Instagram)

### Metrics Coverage
| Metric | Status | Source Table | Notes |
|--------|--------|--------------|-------|
| Impressions | ✅ | fct_ad_set_performance | Available |
| Reach | ✅ | fct_ad_set_performance.reach | Available |
| Frequency | ✅ | fct_ad_set_performance.frequency | Available |
| Clicks | ✅ | fct_ad_set_performance.clicks | Available |
| CTR | ✅ | fct_ad_set_performance.ctr | Available |
| CPC | ✅ | fct_ad_set_performance.cpc | Available |
| Spend | ✅ | fct_ad_set_performance.spend | Available |
| Conversions | ⚠️ | fct_campaign_performance | Currently NULL for Meta |
| Cost per Conversion | ⚠️ | Calculated | Depends on conversions |
| ROAS | ⚠️ | Calculated | Depends on conversion value |

### Status: ⚠️ PARTIAL (70% coverage)

**Gap:** Meta conversion tracking needs to pull from Facebook conversion tables (not currently integrated)

---

## Dashboard 11: Klaviyo (Email Marketing)

### Metrics Coverage
| Metric | Status | Source Table | Notes |
|--------|--------|--------------|-------|
| Emails Sent | ✅ | fct_email_campaign.sent | Available |
| Delivered | ⚠️ | Calculated | sent - bounces |
| Delivery Rate | ⚠️ | Calculated | delivered / sent |
| Opens | ✅ | fct_email_campaign.opens | Available |
| Open Rate | ✅ | fct_email_campaign.open_rate | Available |
| Clicks | ✅ | fct_email_campaign.clicks | Available |
| Click Rate | ✅ | fct_email_campaign.click_rate | Available |
| Revenue | ❌ | Not available | Need Klaviyo order/revenue events |
| Placed Orders | ❌ | Not available | Need Klaviyo order events |
| Active Subscribers | ⚠️ | dim_list.member_count | Aggregated list count |

### Status: ⚠️ PARTIAL (65% coverage)

**Gaps:**
1. Revenue attribution - Need to extract revenue from Klaviyo events
2. Placed Orders - Need to identify order events in Klaviyo

---

## Dashboard 12: Magento (E-commerce)

### Metrics Coverage
| Metric | Status | Notes |
|--------|--------|-------|
| Total Revenue | ❌ | Magento integration not built |
| Net Revenue | ❌ | Magento integration not built |
| Orders | ❌ | Magento integration not built |
| Average Order Value | ❌ | Magento integration not built |
| Items Sold | ❌ | Magento integration not built |
| Customers | ❌ | Magento integration not built |
| New Customers | ❌ | Magento integration not built |
| Repeat Customer Rate | ❌ | Magento integration not built |
| Cart Abandonment Rate | ❌ | Magento integration not built |
| Add to Cart Rate | ❌ | Magento integration not built |

### Status: ❌ NOT AVAILABLE (0% coverage)

**Note:** Magento integration is marked as "Future Integration" in dashboard specs

---

## Dashboard 13: Overall Performance

### Metrics Coverage
| Metric | Status | Source Table | Notes |
|--------|--------|--------------|-------|
| Total Marketing Spend | ✅ | Aggregated from all platforms | Available |
| Total Revenue | ⚠️ | fct_ga4_conversions | GA4 revenue only |
| Blended ROAS | ⚠️ | Calculated | revenue / total spend |
| Blended CPA | ⚠️ | Calculated | spend / total conversions |
| Total Conversions | ✅ | Aggregated | Available |
| Total Impressions | ✅ | Aggregated | Available |
| Total Clicks | ✅ | Aggregated | Available |
| Blended CTR | ✅ | Calculated | clicks / impressions |
| Total Users | ✅ | fct_ga4_traffic.total_users | Available |
| Marketing Efficiency Ratio | ⚠️ | Calculated | revenue / total cost |

### Status: ✅ GOOD (80% coverage)

---

## Summary: Coverage by Dashboard

| Dashboard | Coverage | Status |
|-----------|----------|--------|
| 1. Core Performance (A) | 90% | ✅ Good |
| 2. Spend & Budget (B) | 85% | ✅ Good |
| 3. Audience & Behavioral (C) | 60% | ⚠️ Partial |
| 4. Funnel & Attribution (D) | 30% | ❌ Major Gaps |
| 5. Creative & Messaging (E) | 40% | ⚠️ Partial |
| 6. Search & Keyword (F) | 40% | ⚠️ Partial |
| 7. Revenue & LTV (G) | 15% | ❌ Major Gaps |
| 8. GA4 | 80% | ✅ Good |
| 9. Google Ads | 90% | ✅ Good |
| 10. Meta Ads | 70% | ⚠️ Partial |
| 11. Klaviyo | 65% | ⚠️ Partial |
| 12. Magento | 0% | ❌ Not Available |
| 13. Overall Performance | 80% | ✅ Good |

---

## Critical Gaps Requiring New Data Sources

### 1. Magento E-commerce Data (HIGH PRIORITY)
**Impact:** Dashboard 7, Dashboard 12
**Required Tables:**
- Orders (order_id, customer_id, total, created_at)
- Order Items (item details, quantity, price)
- Customers (customer_id, first_order_date, total_orders)
- Cart/Checkout events

### 2. CRM/Pipeline Data (MEDIUM PRIORITY)
**Impact:** Dashboard 4, Dashboard 7
**Required Data:**
- Leads (lead_id, source, status, value)
- Pipeline stages
- Lead-to-customer conversion

### 3. Multi-Touch Attribution (MEDIUM PRIORITY)
**Impact:** Dashboard 4
**Options:**
- GA4 Attribution reports (if available via Fivetran)
- Third-party attribution tool (Northbeam, Triple Whale)

### 4. SEO/Competitive Data (LOW PRIORITY)
**Impact:** Dashboard 6
**Required Data:**
- Search volume (SEMrush, Ahrefs, Google Keyword Planner)
- Competitor keyword rankings

---

## Recommended Actions

### Immediate (Can fix with existing sources)

1. **Add Impression Share to Google Ads models**
   - Check if `search_impression_share`, `search_budget_lost_impression_share`, `search_rank_lost_impression_share` exist in source
   - Add to `fct_campaign_performance` or create new fact table

2. **Add Meta Conversion tracking**
   - Check Facebook Ads `basic_ad` for conversion columns
   - Or pull from `actions` table if available

3. **Extract Klaviyo Revenue**
   - Filter Klaviyo events for `Placed Order` event type
   - Extract revenue from event properties

4. **Add Landing Page data from GA4**
   - Check for `pages_report` or `landing_page_report` in GA4 sources
   - Create new fact table for page-level metrics

### Short-term (New Fivetran connectors needed)

1. **Magento Connector**
   - Set up Fivetran Magento connector
   - Build dimension and fact tables for orders, customers, products

2. **GA4 Enhanced Reports**
   - Enable enhanced measurement in GA4
   - Add scroll depth, file downloads events

### Long-term (Requires additional tools/integrations)

1. **Attribution Platform**
   - Evaluate attribution tools (Northbeam, Triple Whale, Rockerbox)
   - Build integration for multi-touch attribution

2. **SEO Tool Integration**
   - Connect SEMrush or Ahrefs via API
   - Build keyword volume/rank tracking tables

3. **CRM Integration**
   - Connect Salesforce/HubSpot if used
   - Build lead and pipeline fact tables

---

## Next Steps

1. **Verify source data availability** - Check Snowflake source tables for impression share, Meta conversions
2. **Prioritize Magento integration** - Critical for LTV and e-commerce dashboards
3. **Update existing models** - Add missing columns to current fact tables where data exists
4. **Create new fact tables** - For page-level data, Klaviyo revenue
