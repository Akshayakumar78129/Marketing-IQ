# Marketing IQ - Dashboard Specifications

## 13 Dashboards Total
- **7 Metric-Category Dashboards** (Consolidated AI-powered analytics)
- **6 Platform Dashboards** (Data source views)

---

# Metric-Category Dashboards (7)

---

## Dashboard 1: Core Performance Metrics (A)

**Purpose:** Primary KPIs to determine if campaigns are winning/losing

### Metrics
| Metric |
|--------|
| Conversions |
| Conversion Rate (CVR) |
| Cost per Conversion (CPA) |
| Conversion Value |
| Return on Ad Spend (ROAS) |
| Click-Through Rate (CTR) |
| Cost per Click (CPC) |
| Impressions |
| Spend |
| Revenue |

### Filters
| Filter | Type | Options |
|--------|------|---------|
| Date Range | Calendar Picker | Custom date range |
| Period Comparison | Date Selector | Current vs previous |
| Campaigns | Multi-select | Campaign list |
| Channels | Multi-select | Paid Search, Paid Social, Email, etc. |
| Forecast Period | Dropdown | 7d, 30d, 60d, 90d, 365d |
| Priority Level | Dropdown | Critical, High, Medium, Low |

### Graphs
| Graph | Type | Description |
|-------|------|-------------|
| KPI Summary Cards | Card Grid | Key metrics at a glance |
| Revenue Trend | Area Chart | Daily revenue over time |
| CTR Analysis | Area Chart | CTR trends over time |
| Trend Comparison | Line Chart | Current vs previous period |
| Revenue by Channel | Pie Chart | Channel distribution |
| CTR Forecast | Area Chart + Confidence Bands | Predictive CTR with bounds |
| Deviation Alerts | Alert Cards | Threshold indicators |
| Prioritized Action List | Data Table | Sorted by ROI impact |

---

## Dashboard 2: Spend & Budget Control (B)

**Purpose:** Track spending, budget allocation, and ROI optimization

### Metrics
| Metric |
|--------|
| Total Spend |
| Spend by Campaign |
| Spend by Ad Group |
| Spend by Keyword |
| Daily Budget Assigned |
| Daily Budget Utilized |
| Overspend/Underspend |
| Bid Strategy Type |
| Marketing ROI |
| Blended CAC |

### Filters
| Filter | Type | Options |
|--------|------|---------|
| Date Range | Calendar Picker | Custom date range |
| Budget Range | Dropdown | $0-$10k, $10k-$25k, $25k-$50k, $50k+ |
| Forecast Period | Dropdown | 7d, 30d, 60d, 90d, 365d |
| Channels | Multi-select | Paid Search, Paid Social, etc. |
| Campaigns | Multi-select | Campaign list |
| Ad Groups | Multi-select | Ad group list |

### Graphs
| Graph | Type | Description |
|-------|------|-------------|
| Channel Performance | Grouped Bar Chart | Performance by channel |
| CAC vs Target | Grouped Bar Chart | Actual vs target CAC per channel |
| Revenue by Channel | Bar Chart | Revenue distribution |
| Channel Efficiency Table | Data Table | With status badges |
| Budget Utilization | Progress Bars | Daily budget used vs assigned |
| Spend Over Time | Area Chart | Daily/weekly spend trends |
| ROI by Campaign | Bar Chart | Campaign-level ROI |

---

## Dashboard 3: Audience & Behavioral (C)

**Purpose:** Understand user behavior, demographics, and page interactions

### Metrics
| Metric |
|--------|
| Users/Sessions |
| New vs Returning |
| Device Type |
| Country/Region |
| Time on Page |
| Engagement Rate |
| Non-Engagement Rate (Bounce Proxy) |
| Entrance Page |
| Referrer / Traffic Source |
| Page Conversion Rate |

### Filters
| Filter | Type | Options |
|--------|------|---------|
| Date Range | Calendar Picker | Custom date range |
| Geography | Multi-select | Regions/Countries |
| Device Type | Dropdown | Desktop, Mobile, Tablet |
| Traffic Source | Multi-select | Organic, Paid, Social, etc. |
| Time Period | Dropdown | 7d, 30d, 90d |
| Page Type | Multi-select | Landing, Product, Form |

### Graphs
| Graph | Type | Description |
|-------|------|-------------|
| Top Converting Pages | Bar Chart | Pages by submissions |
| Page Engagement | Multi-Line Chart | Engagement rate vs conversion rate |
| All Pages Table | Data Table | Sortable page listing |
| Geographic Heatmap | Map | Users by location |
| Device Breakdown | Donut Chart | Device distribution |
| User Flow | Sankey Diagram | Navigation paths |

---

## Dashboard 4: Funnel & Attribution (D)

**Purpose:** Critical to detect tracking leaks & broken journeys

### Metrics
| Metric |
|--------|
| Session-to-Add-to-Cart Rate |
| Session-to-Lead Form Start Rate |
| Lead Form Completion Rate |
| Purchase Conversion Event Count |
| UTM Parameters Coverage % |
| Conversion Attribution Path |
| Missing Conversion Events |
| Pixel Firing Success Rate |
| Attribution Revenue |
| Pipeline Value |

### Filters
| Filter | Type | Options |
|--------|------|---------|
| Date Range | Calendar Picker | Custom date range |
| Forecast Period (Pipeline) | Dropdown | 7d, 30d, 60d, 90d, 365d |
| Attribution Model | Dropdown | First-touch, Last-touch, Linear, Time-decay |
| Tracking Status | Dropdown | Healthy, Warning, Critical |
| Source | Multi-select | Organic, Paid, Email, etc. |

### Graphs
| Graph | Type | Description |
|-------|------|-------------|
| Attribution Chart | Stacked Bar Chart | Multi-touch attribution models |
| Pipeline by Source | Pie Chart | Marketing/Sales/Partner distribution |
| Attribution Revenue | Pie Chart | Revenue by attribution model |
| Pipeline Value Breakdown | Progress Bars | Value per source |
| Tracking Health Dashboard | Gauge Charts | Status indicators |
| Conversion Funnel | Funnel Chart | Visitor -> Lead -> Customer |

---

## Dashboard 5: Creative & Messaging (E)

**Purpose:** Decide which ads are winners or losers, detect fatigue

### Metrics
| Metric |
|--------|
| Headline |
| Description |
| Creative Asset ID |
| Creative Type (img/video/rs) |
| Impressions per Creative |
| CTR per Creative |
| CVR per Creative |
| Asset Fatigue Score |
| CTR Decay Rate |
| A/B Test Lift |

### Filters
| Filter | Type | Options |
|--------|------|---------|
| Date Range | Calendar Picker | Custom date range |
| Creative Type | Multi-select | Image, Video, Responsive |
| Performance Status | Dropdown | Winner, Loser, Testing, Fatigued, Active, New |
| Content Type | Multi-select | Headlines, Descriptions, CTAs |
| Sentiment | Dropdown | Positive, Neutral, Negative |

### Graphs
| Graph | Type | Description |
|-------|------|-------------|
| Performance by Asset Type | Pie Chart | Revenue by creative type |
| Top Performing Creatives | Bar Chart | Top 5 by revenue |
| A/B Test Results | Data Table | With lift indicators |
| Creative Library | Data Table | Asset listing with metrics |
| Sentiment Trends | Line Chart | Sentiment over time |
| Brand Risk Monitoring | Risk Score Cards | Alert list |

---

## Dashboard 6: Search Intent & Keyword (F)

**Purpose:** Scale search campaigns smartly with keyword intelligence

### Metrics
| Metric |
|--------|
| Keyword Text |
| Match Type |
| Search Term |
| Search Volume |
| Click Share |
| Impression Share |
| Top of Page Rate |
| Search Lost IS (Budget) |
| Search Lost IS (Rank) |
| Impression Share Lost to Competitors |

### Filters
| Filter | Type | Options |
|--------|------|---------|
| Date Range | Calendar Picker | Custom date range |
| Match Type | Multi-select | Exact, Phrase, Broad |
| Performance | Dropdown | High, Medium, Low |
| Competition Level | Dropdown | High, Medium, Low |
| Competitor | Multi-select | Competitor list |
| Time Period | Dropdown | 7d, 30d, 90d |

### Graphs
| Graph | Type | Description |
|-------|------|-------------|
| Keyword Analysis | Bar Charts + Tables | Performance by keyword |
| Keyword Research Table | Data Table | With metrics |
| SEO Keyword Tracker | Line Charts | Rank changes over time |
| Competitor Keyword Comparison | Comparison Bar Charts | Gap analysis |
| Competitor Keyword Gap | Bar Chart | Keywords they rank for |
| Market Position Trends | Line Chart | Position over time |

---

## Dashboard 7: Revenue & LTV (G)

**Purpose:** For segmentation & scaling high-value audiences

### Metrics
| Metric |
|--------|
| Revenue per User |
| First Purchase Value |
| Repeat Purchase Rate |
| CLV/LTV |
| Time to 2nd Purchase |
| Customer Cohort Labels |
| LTV/CAC Ratio |
| Churn Rate |
| Lead Conversion Rate |
| Seasonality Index |

### Filters
| Filter | Type | Options |
|--------|------|---------|
| Date Range | Calendar Picker | Custom date range |
| Lead Quality | Dropdown | Hot, Warm, Cold, MQL Only, SQL Only |
| Geography | Multi-select | Regions/Countries |
| Customer Segment | Multi-select | High-value, At-risk, New |
| Forecast Period | Dropdown | 7d, 30d, 60d, 90d, 365d |
| Cohort Selectors | Dropdown | By acquisition date |

### Graphs
| Graph | Type | Description |
|-------|------|-------------|
| Conversion Funnel | Funnel Chart | Visitor -> Lead -> MQL -> SQL -> Customer |
| LTV/CAC Chart | Bar Chart | Side-by-side comparison |
| Retention Cohort | Heatmap Grid | Retention by month cohort |
| Churn Analysis | Line Chart | Churn rate trends |
| Trend Comparison | Line Chart | Current vs previous period |
| Seasonal Heatmap | Heatmap Grid | Performance by month/week |

---

# Platform Dashboards (6)

---

## Dashboard 8: Google Analytics 4 (GA4)

**Purpose:** Website traffic, user behavior, and conversion analytics from GA4

### Metrics
| Metric | Source | Description |
|--------|--------|-------------|
| Total Users | GA4 | Unique users visiting the site |
| Sessions | GA4 | Total sessions count |
| Engagement Rate | GA4 | Engaged sessions / total sessions |
| Avg Session Duration | GA4 | Average time per session |
| Non-Engagement Rate | GA4 | Proxy for bounce rate (1 - engagement_rate) |
| Page Views | GA4 | Total page views |
| Conversions (Key Events) | GA4 | Total conversion events |
| Conversion Rate | GA4 | Conversions / sessions |
| Revenue | GA4 | E-commerce revenue |
| Avg Order Value | GA4 | Revenue / transactions |

### Filters
| Filter | Type | Options |
|--------|------|---------|
| Date Range | Calendar Picker | Custom date range |
| Source/Medium | Multi-select | Traffic sources |
| Country/Region | Multi-select | Geographic filter |
| Device Category | Dropdown | Desktop, Mobile, Tablet |
| Landing Page | Multi-select | Entry pages |

### Graphs
| Graph | Type | Description |
|-------|------|-------------|
| Users Over Time | Line Chart | Daily/weekly user trends |
| Traffic by Source | Pie Chart | Source distribution |
| Top Pages | Bar Chart | Most viewed pages |
| Conversion Funnel | Funnel Chart | User journey stages |
| Geographic Heatmap | Map | Users by location |
| Device Breakdown | Donut Chart | Desktop vs Mobile vs Tablet |

---

## Dashboard 9: Google Ads

**Purpose:** Paid search and display advertising performance from Google Ads

### Metrics
| Metric | Source | Description |
|--------|--------|-------------|
| Impressions | GAds | Ad impressions count |
| Clicks | GAds | Total clicks |
| CTR | GAds | Click-through rate |
| CPC | GAds | Cost per click |
| Spend | GAds | Total ad spend |
| Conversions | GAds | Conversion count |
| Conversion Value | GAds | Revenue from conversions |
| Cost per Conversion | GAds | Spend / conversions |
| ROAS | GAds | Return on ad spend |
| Impression Share | GAds | Share of available impressions |

### Filters
| Filter | Type | Options |
|--------|------|---------|
| Date Range | Calendar Picker | Custom date range |
| Campaign | Multi-select | Campaign list |
| Ad Group | Multi-select | Ad group list |
| Campaign Type | Dropdown | Search, Display, Shopping, Video |
| Device | Dropdown | Desktop, Mobile, Tablet |
| Network | Dropdown | Search, Display, YouTube |

### Graphs
| Graph | Type | Description |
|-------|------|-------------|
| Spend vs Conversions | Dual-axis Line Chart | Spend and conversion trends |
| Campaign Performance | Bar Chart | Top campaigns by ROAS |
| CTR by Device | Grouped Bar | Device comparison |
| Keyword Performance | Data Table | Top keywords with metrics |
| Hourly Performance | Heatmap | Performance by hour/day |
| Search Terms | Word Cloud | Top search queries |

---

## Dashboard 10: Meta Ads (Facebook/Instagram)

**Purpose:** Social media advertising performance from Meta Ads platform

### Metrics
| Metric | Source | Description |
|--------|--------|-------------|
| Impressions | Meta | Ad impressions |
| Reach | Meta | Unique users reached |
| Frequency | Meta | Avg impressions per user |
| Clicks | Meta | Link clicks |
| CTR | Meta | Click-through rate |
| CPC | Meta | Cost per click |
| Spend | Meta | Total ad spend |
| Conversions | Meta | Conversion events |
| Cost per Conversion | Meta | Spend / conversions |
| ROAS | Meta | Return on ad spend |

### Filters
| Filter | Type | Options |
|--------|------|---------|
| Date Range | Calendar Picker | Custom date range |
| Campaign | Multi-select | Campaign list |
| Ad Set | Multi-select | Ad set list |
| Objective | Dropdown | Conversions, Traffic, Awareness, etc. |
| Placement | Multi-select | Facebook, Instagram, Audience Network |
| Platform | Dropdown | Facebook, Instagram, Both |

### Graphs
| Graph | Type | Description |
|-------|------|-------------|
| Reach vs Frequency | Dual-axis Chart | Audience saturation |
| Performance by Placement | Stacked Bar | Facebook vs Instagram |
| Ad Creative Performance | Bar Chart | Top ads by ROAS |
| Audience Demographics | Pie Charts | Age, gender breakdown |
| Funnel by Objective | Funnel Chart | Awareness to conversion |
| Spend Distribution | Treemap | Budget allocation |

---

## Dashboard 11: Klaviyo (Email Marketing)

**Purpose:** Email marketing performance and customer engagement from Klaviyo

### Metrics
| Metric | Source | Description |
|--------|--------|-------------|
| Emails Sent | Klaviyo | Total emails sent |
| Delivered | Klaviyo | Successfully delivered |
| Delivery Rate | Klaviyo | Delivered / sent |
| Opens | Klaviyo | Email opens |
| Open Rate | Klaviyo | Opens / delivered |
| Clicks | Klaviyo | Link clicks |
| Click Rate | Klaviyo | Clicks / delivered |
| Revenue | Klaviyo | Attributed revenue |
| Placed Orders | Klaviyo | Orders from email |
| Active Subscribers | Klaviyo | Engaged list size |

### Filters
| Filter | Type | Options |
|--------|------|---------|
| Date Range | Calendar Picker | Custom date range |
| Campaign Type | Dropdown | Campaign, Flow, All |
| Flow Name | Multi-select | Automation flows |
| Segment | Multi-select | Subscriber segments |
| List | Multi-select | Email lists |

### Graphs
| Graph | Type | Description |
|-------|------|-------------|
| Email Performance Over Time | Line Chart | Open/click rate trends |
| Campaign vs Flow Revenue | Stacked Bar | Revenue by type |
| Top Performing Campaigns | Bar Chart | By revenue |
| Flow Performance | Funnel Chart | Flow conversion rates |
| Subscriber Growth | Area Chart | List growth over time |
| Engagement Heatmap | Heatmap | Best send times |

---

## Dashboard 12: Magento (E-commerce)

**Purpose:** E-commerce store performance and order data from Magento (Future Integration)

*Note: Data integration pending - placeholder for future implementation*

### Metrics
| Metric | Source | Description |
|--------|--------|-------------|
| Total Revenue | Magento | Gross revenue |
| Net Revenue | Magento | Revenue after returns |
| Orders | Magento | Total order count |
| Average Order Value | Magento | Revenue / orders |
| Items Sold | Magento | Total units sold |
| Customers | Magento | Unique customers |
| New Customers | Magento | First-time buyers |
| Repeat Customer Rate | Magento | Returning customers % |
| Cart Abandonment Rate | Magento | Abandoned / initiated carts |
| Add to Cart Rate | Magento | Add to cart / views |

### Filters
| Filter | Type | Options |
|--------|------|---------|
| Date Range | Calendar Picker | Custom date range |
| Store View | Dropdown | Store/website selector |
| Category | Multi-select | Product categories |
| Customer Group | Dropdown | B2B, B2C, Wholesale |
| Payment Method | Multi-select | Payment types |
| Order Status | Multi-select | Pending, Complete, Cancelled |

### Graphs
| Graph | Type | Description |
|-------|------|-------------|
| Revenue Trend | Area Chart | Daily revenue |
| Top Products | Bar Chart | Best sellers by revenue |
| Category Performance | Treemap | Sales by category |
| Customer Cohort | Heatmap | Retention by cohort |
| Order Funnel | Funnel Chart | Browse to purchase |
| Geographic Sales | Map | Sales by region |

---

## Dashboard 13: Overall Performance

**Purpose:** Unified cross-platform marketing performance overview

### Metrics
| Metric | Source | Description |
|--------|--------|-------------|
| Total Marketing Spend | All Platforms | Combined ad spend |
| Total Revenue | GA4 + Magento | Combined revenue |
| Blended ROAS | Calc | Revenue / total spend |
| Blended CPA | Calc | Spend / total conversions |
| Total Conversions | All Platforms | Combined conversions |
| Total Impressions | GAds + Meta | Combined reach |
| Total Clicks | All Platforms | Combined clicks |
| Blended CTR | Calc | Clicks / impressions |
| Total Users | GA4 | Website visitors |
| Marketing Efficiency Ratio | Calc | Revenue / total marketing cost |

### Filters
| Filter | Type | Options |
|--------|------|---------|
| Date Range | Calendar Picker | Custom date range |
| Platform | Multi-select | GA4, Google Ads, Meta, Klaviyo, Magento |
| Channel | Multi-select | Paid Search, Paid Social, Email, Organic |
| Campaign | Multi-select | Cross-platform campaigns |

### Graphs
| Graph | Type | Description |
|-------|------|-------------|
| Revenue by Platform | Stacked Area Chart | Platform contribution over time |
| Spend vs Revenue | Dual-axis Line | Efficiency tracking |
| Channel Performance | Grouped Bar | Compare all channels |
| Platform ROAS Comparison | Bar Chart | ROAS by platform |
| Marketing Mix | Pie Chart | Spend distribution |
| Cross-Platform Funnel | Sankey Diagram | User journey across platforms |
| KPI Summary Cards | Card Grid | Key metrics at a glance |

---

## Data Sources Required

| Source | Tables Needed |
|--------|---------------|
| Google Ads | CAMPAIGN_STATS, AD_GROUP_STATS, AD_STATS, KEYWORD_STATS, SEARCH_TERM_STATS, *_HISTORY |
| Facebook Ads | BASIC_*, DEMOGRAPHICS_*, DELIVERY_*, ACTION_* |
| GA4 | TRAFFIC_*, CONVERSIONS_REPORT, EVENTS_REPORT, DEMOGRAPHIC_*, PAGES_* |
| Klaviyo | EVENT, CAMPAIGN, FLOW, PERSON, SEGMENT |
| CRM/Pipeline | External integration needed |
| SEO Tools | External integration needed |
