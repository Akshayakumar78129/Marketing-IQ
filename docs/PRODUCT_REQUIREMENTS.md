# Marketing IQ - Product Requirements Document

> Transforming marketing data into intelligent, actionable insights

---

## Table of Contents

1. [Product Vision](#1-product-vision)
2. [Core Concepts](#2-core-concepts)
3. [Landing Page Experience](#3-landing-page-experience)
4. [Thoughtlet System (Dashboards)](#4-thoughtlet-system-dashboards)
5. [Thought System](#5-thought-system)
6. [AI Video Agent](#6-ai-video-agent)
7. [Action System](#7-action-system)
8. [User Journeys](#8-user-journeys)
9. [Use Cases & Examples](#9-use-cases--examples)
10. [Future Scope](#10-future-scope)

---

## 1. Product Vision

### 1.1 Mission Statement

**Marketing IQ transforms overwhelming marketing data into clear, actionable intelligence through AI-powered insights that speak to you.**

Instead of dashboards that require interpretation, Marketing IQ:
- **Tells you** what changed and why
- **Shows you** what's connected and affected
- **Recommends** what to do next
- **Lets you ask** questions in natural language

### 1.2 The Problem We Solve

| Traditional Analytics | Marketing IQ |
|----------------------|--------------|
| "Here's your data, figure it out" | "Here's what happened and what you should do" |
| 50 dashboards, 500 metrics | Unified view with intelligent prioritization |
| Manual pattern detection | AI identifies anomalies and trends |
| Siloed platform data | Cross-platform correlation |
| Static reports | Dynamic, conversational insights |

### 1.3 Target Users

| User Type | Needs | How We Help |
|-----------|-------|-------------|
| **Marketing Manager** | Quick daily overview, identify issues | Video briefing + prioritized thoughts |
| **Performance Marketer** | Deep-dive into campaigns, optimization | Thoughtlets + drill-down + recommendations |
| **CMO/Director** | High-level trends, ROI visibility | Cross-platform aggregates + forecasts |
| **Agency** | Multi-client reporting, efficiency | Tenant isolation + templated insights |

### 1.4 Value Proposition

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│   FROM: "We have great data but struggle to act on it"          │
│                                                                  │
│   TO:   "Our AI tells us exactly what's happening and           │
│          what to do about it, every single day"                 │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Core Concepts

### 2.1 Concept Hierarchy

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         CONCEPT HIERARCHY                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  METRICS (Atoms)                                                         │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │  Individual KPIs from data sources                                │   │
│  │  Examples: CPC, CTR, ROAS, Spend, Conversions, Open Rate          │   │
│  │  Count: 100+ metrics across all platforms                         │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                    │                                     │
│                                    ▼                                     │
│  THOUGHTLETS (Molecules) - What we call "Dashboards"                     │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │  Grouped metrics visualized together                              │   │
│  │  Examples: Core Performance, Budget Control, Audience & Behavior  │   │
│  │  Count: 13 thoughtlets (7 category + 6 platform)                  │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                    │                                     │
│                                    ▼                                     │
│  THOUGHTS (Insights)                                                     │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │  Cross-metric patterns that breach defined thresholds             │   │
│  │  Can span MULTIPLE thoughtlets AND domains                        │   │
│  │  Examples: "Ad efficiency declining", "Budget exhaustion risk"    │   │
│  │  Generated when: Thresholds breached, patterns detected           │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                    │                                     │
│                                    ▼                                     │
│  ACTIONS (Recommendations)                                               │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │  AI-generated recommendations with one-click execution            │   │
│  │  Examples: "Pause campaign X", "Increase budget by 20%"           │   │
│  │  Integration: Future API connections to ad platforms              │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Metrics

**Definition:** The fundamental unit of measurement. Every metric has:
- **Source**: Where it comes from (Google Ads, Meta, GA4, Klaviyo)
- **Domain**: What area it belongs to (Marketing, Finance, Operations)
- **Threshold**: When it becomes noteworthy (warning/critical levels)
- **Relationships**: What other metrics it affects

**Example Metrics:**

| Metric | Source | Domain | Threshold (Warning) | Affects |
|--------|--------|--------|---------------------|---------|
| CPC | Google Ads | Marketing/Paid | > $2.50 | ROAS, CPA, Budget |
| ROAS | All Ads | Marketing/Core | < 3.0 | Revenue, Profit |
| Open Rate | Klaviyo | Marketing/Email | < 15% | CTR, Conversions |
| Spend | All Ads | Marketing/Budget | > Daily Budget | Cash Flow |

### 2.3 Thoughtlets (Dashboards)

**Definition:** A visual grouping of related metrics. Each thoughtlet:
- Contains 8-12 core metrics
- Has dedicated visualizations (charts, cards, tables)
- Supports filters and date ranges
- Can be drilled into for detail

**The 13 Thoughtlets:**

| # | Thoughtlet | Category | Purpose |
|---|------------|----------|---------|
| 1 | Core Performance | Metric-Category | KPIs for win/lose determination |
| 2 | Spend & Budget | Metric-Category | Budget tracking and ROI |
| 3 | Audience & Behavioral | Metric-Category | User behavior analytics |
| 4 | Funnel & Attribution | Metric-Category | Conversion path analysis |
| 5 | Creative & Messaging | Metric-Category | Ad creative performance |
| 6 | Search Intent & Keyword | Metric-Category | Search campaign optimization |
| 7 | Revenue & LTV | Metric-Category | Customer value metrics |
| 8 | Google Analytics 4 | Platform | GA4 traffic & behavior |
| 9 | Google Ads | Platform | Paid search performance |
| 10 | Meta Ads | Platform | Social advertising |
| 11 | Klaviyo | Platform | Email marketing |
| 12 | Magento | Platform | E-commerce (future) |
| 13 | Overall Performance | Platform | Cross-platform aggregate |

### 2.4 Thoughts

**Definition:** An intelligent insight formed when metrics breach thresholds. Thoughts:
- **Span multiple metrics** (often across different thoughtlets)
- **Have defined triggers** (threshold + condition combinations)
- **Calculate blast radius** (what else is affected)
- **Generate automatically** when conditions are met

**Key Properties:**
```
Thought = {
  Trigger Condition: "ROAS < 3.0 AND Spend > $50k AND CPC increasing 20%"
  Component Metrics: [ROAS, Spend, CPC, CTR, Impressions]
  Blast Radius: [Budget Utilization, Revenue Target, Profit Margin]
  Priority: Critical/High/Medium/Low
  Recommended Actions: [Pause low performers, Reduce bids, Reallocate budget]
}
```

### 2.5 Actions

**Definition:** Concrete recommendations generated from thoughts. Actions:
- Are prioritized by business impact
- Include execution buttons (current: manual, future: automated)
- Track completion status
- Can be scheduled or dismissed

---

## 3. Landing Page Experience

### 3.1 Layout Structure

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         MARKETING IQ - LANDING PAGE                      │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │                                                                    │  │
│  │                      VIDEO AGENT SECTION                           │  │
│  │                                                                    │  │
│  │    ┌──────────────┐     "Good morning! Here's what happened       │  │
│  │    │              │      overnight: Your Meta campaigns saw        │  │
│  │    │   AI Avatar  │      a 15% spike in CPC. I've identified       │  │
│  │    │              │      3 actions that could save you $2,400..."   │  │
│  │    │   (Video)    │                                                │  │
│  │    │              │     [Ask me anything...]                       │  │
│  │    └──────────────┘                                                │  │
│  │                                                                    │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                                                          │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │                      THREE-SECTION DISPLAY                         │  │
│  │                                                                    │  │
│  │  SECTION 1: THOUGHTLETS                                           │  │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐     │  │
│  │  │  Core   │ │ Budget  │ │Audience │ │ Funnel  │ │Creative │ ... │  │
│  │  │  Perf   │ │ Control │ │Behavior │ │  Attr   │ │ Message │     │  │
│  │  │   (A)   │ │   (B)   │ │   (C)   │ │   (D)   │ │   (E)   │     │  │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘     │  │
│  │                                                                    │  │
│  │  SECTION 2: THOUGHTS (Active Insights)                            │  │
│  │  ┌─────────────────────────────────────────────────────────────┐  │  │
│  │  │ [!] Ad Efficiency Declining                   Priority: HIGH │  │  │
│  │  │     Metrics: ROAS ↓12%, CPC ↑25%, Spend: $52k              │  │  │
│  │  │     Affected: Budget, Revenue, 3 campaigns                  │  │  │
│  │  └─────────────────────────────────────────────────────────────┘  │  │
│  │  ┌─────────────────────────────────────────────────────────────┐  │  │
│  │  │ [!] Email Engagement Drop                    Priority: MEDIUM │  │  │
│  │  │     Metrics: Open Rate ↓8%, CTR ↓15%                        │  │  │
│  │  └─────────────────────────────────────────────────────────────┘  │  │
│  │                                                                    │  │
│  │  SECTION 3: ACTIONS/RECOMMENDATIONS                               │  │
│  │  ┌─────────────────────────────────────────────────────────────┐  │  │
│  │  │ 1. Pause "Holiday Sale" campaign           [Execute] [Later] │  │  │
│  │  │    Impact: Save $450/day, minimal conversion loss            │  │  │
│  │  ├─────────────────────────────────────────────────────────────┤  │  │
│  │  │ 2. Reduce Meta CPC bids by 15%             [Execute] [Later] │  │  │
│  │  │    Impact: Estimated $2,400 savings this week               │  │  │
│  │  ├─────────────────────────────────────────────────────────────┤  │  │
│  │  │ 3. A/B test new email subject lines        [Execute] [Later] │  │  │
│  │  │    Impact: Potential 20% open rate improvement              │  │  │
│  │  └─────────────────────────────────────────────────────────────┘  │  │
│  │                                                                    │  │
│  └───────────────────────────────────────────────────────────────────┘  │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### 3.2 Section Details

#### Section 1: Thoughtlets (Dashboard Cards)
- **Display**: Horizontal scrollable row of cards
- **Each Card Shows**:
  - Thoughtlet name and icon
  - 2-3 key metrics with trend indicators
  - Overall health status (green/yellow/red)
- **Interaction**: Click to enter full thoughtlet dashboard

#### Section 2: Thoughts (Insight Cards)
- **Display**: Vertical stack, sorted by priority
- **Each Card Shows**:
  - Thought title and severity indicator
  - Component metrics with current values and changes
  - Blast radius summary (what's affected)
  - Timestamp (when triggered)
- **Interaction**: Click to expand and see full analysis

#### Section 3: Actions (Recommendation List)
- **Display**: Actionable list with execution buttons
- **Each Item Shows**:
  - Action description
  - Expected impact (quantified when possible)
  - Source thought it came from
  - Execution options: [Execute Now], [Schedule], [Dismiss]
- **Future**: Direct API integration for one-click execution

---

## 4. Thoughtlet System (Dashboards)

### 4.1 Thoughtlet Components

Each thoughtlet contains:

```
┌─────────────────────────────────────────────────────────────────┐
│                    THOUGHTLET ANATOMY                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ HEADER                                                       ││
│  │ [Thoughtlet Name]          [Date Range] [Filters] [Export]   ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ KPI CARDS (Summary Metrics)                                  ││
│  │ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐      ││
│  │ │ Metric │ │ Metric │ │ Metric │ │ Metric │ │ Metric │      ││
│  │ │  $45k  │ │  3.2%  │ │  4.5   │ │  $12   │ │  850   │      ││
│  │ │  ↑12%  │ │  ↓5%   │ │  ↑8%   │ │  →0%   │ │  ↑15%  │      ││
│  │ └────────┘ └────────┘ └────────┘ └────────┘ └────────┘      ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
│  ┌──────────────────────┐ ┌────────────────────────────────────┐│
│  │ PRIMARY CHART        │ │ SECONDARY CHARTS                   ││
│  │                      │ │ ┌────────────┐ ┌────────────┐      ││
│  │  [Line/Area Chart]   │ │ │  Pie Chart │ │  Bar Chart │      ││
│  │                      │ │ └────────────┘ └────────────┘      ││
│  │                      │ │ ┌────────────┐ ┌────────────┐      ││
│  │                      │ │ │  Heatmap   │ │  Funnel    │      ││
│  │                      │ │ └────────────┘ └────────────┘      ││
│  └──────────────────────┘ └────────────────────────────────────┘│
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ DATA TABLE (Drill-down)                                      ││
│  │ [Sortable, Filterable, Exportable]                          ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 4.2 Thoughtlet Reference

See [AGENT_DASHBOARD_MAPPING.md](./AGENT_DASHBOARD_MAPPING.md) for complete specifications including:
- All 13 thoughtlet definitions
- Metrics per thoughtlet
- Filter options
- Visualization types

---

## 5. Thought System

### 5.1 How Thoughts Form

```
                         THOUGHT FORMATION PROCESS

Step 1: METRIC CHANGE DETECTED
        ┌─────────────────────────────────────────┐
        │ CPC increased from $1.80 to $2.50       │
        │ Change: +38.9%                          │
        └─────────────────────────────────────────┘
                              │
                              ▼
Step 2: THRESHOLD CHECK
        ┌─────────────────────────────────────────┐
        │ CPC > $2.00 (warning threshold)    ✓   │
        │ CPC > $3.00 (critical threshold)   ✗   │
        │ Result: WARNING LEVEL BREACH           │
        └─────────────────────────────────────────┘
                              │
                              ▼
Step 3: FIND RELATED THOUGHTS
        ┌─────────────────────────────────────────┐
        │ Thought: "Ad Efficiency Declining"      │
        │ Contains metrics: CPC, ROAS, CTR, CVR   │
        │ This thought is ACTIVATED               │
        └─────────────────────────────────────────┘
                              │
                              ▼
Step 4: EVALUATE ALL CONDITIONS
        ┌─────────────────────────────────────────┐
        │ CPC > $2.00           ✓ (currently $2.50)│
        │ ROAS < 3.0            ✓ (currently 2.8) │
        │ Spend > $10k/week     ✓ (currently $52k)│
        │ All conditions met: THOUGHT TRIGGERS   │
        └─────────────────────────────────────────┘
                              │
                              ▼
Step 5: CALCULATE BLAST RADIUS
        ┌─────────────────────────────────────────┐
        │ Direct Impact:                          │
        │   - Budget Utilization (+15%)           │
        │   - CPA (+22%)                          │
        │                                         │
        │ Indirect Impact (via ROAS):             │
        │   - Revenue Target (at risk)            │
        │   - Profit Margin (-3%)                 │
        │                                         │
        │ Cross-Domain (Finance):                 │
        │   - Cash Flow projection affected       │
        └─────────────────────────────────────────┘
                              │
                              ▼
Step 6: AI AGENT PROCESSING
        ┌─────────────────────────────────────────┐
        │ Agent receives:                         │
        │   - Triggered thought definition        │
        │   - Current metric values               │
        │   - Historical context (7/30/90 days)   │
        │   - Blast radius calculations           │
        │                                         │
        │ Agent generates:                        │
        │   - Natural language explanation        │
        │   - Root cause hypothesis               │
        │   - Prioritized recommendations         │
        │   - Urgency assessment                  │
        └─────────────────────────────────────────┘
                              │
                              ▼
Step 7: THOUGHT PUBLISHED
        ┌─────────────────────────────────────────┐
        │ Thought Card Created                    │
        │ Actions Generated                       │
        │ User Notified (WebSocket/Email)         │
        │ Video Agent Briefing Updated            │
        └─────────────────────────────────────────┘
```

### 5.2 Thought Categories

| Category | Description | Example |
|----------|-------------|---------|
| **Performance** | Campaign/ad efficiency issues | "ROAS declining across Meta campaigns" |
| **Budget** | Spending anomalies | "Daily budget exhausted by 2pm" |
| **Audience** | User behavior changes | "Engagement rate dropped 25% on mobile" |
| **Creative** | Ad fatigue/performance | "Top creative showing CTR decay" |
| **Competition** | Market position changes | "Impression share lost to competitors" |
| **Channel** | Platform-specific issues | "Email deliverability dropping" |
| **Opportunity** | Positive patterns | "High-converting keyword cluster identified" |

### 5.3 Cross-Thoughtlet Thoughts

A single thought can draw from metrics across multiple thoughtlets:

```
┌─────────────────────────────────────────────────────────────────┐
│              CROSS-THOUGHTLET THOUGHT EXAMPLE                    │
│                                                                  │
│  Thought: "Customer Acquisition Getting Expensive"              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Metrics from Thoughtlet 1 (Core Performance):                  │
│    - CPA: $45 (↑30% vs last month)                              │
│    - Conversion Rate: 2.1% (↓15%)                               │
│                                                                  │
│  Metrics from Thoughtlet 2 (Budget):                            │
│    - Total Spend: $125k (at 95% of budget)                      │
│    - Budget Utilization: 98%                                    │
│                                                                  │
│  Metrics from Thoughtlet 3 (Audience):                          │
│    - New User Rate: 45% (↓20%)                                  │
│    - Session Duration: 1:45 (↓25%)                              │
│                                                                  │
│  Metrics from Thoughtlet 7 (Revenue & LTV):                     │
│    - First Purchase Value: $85 (stable)                         │
│    - LTV/CAC Ratio: 2.1 (was 3.2)                              │
│                                                                  │
│  INSIGHT: Rising acquisition costs + lower engagement +         │
│           declining LTV ratio = unsustainable growth path       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 5.4 Cross-Domain Thoughts (Future)

Thoughts can extend beyond marketing into other business domains:

```
┌─────────────────────────────────────────────────────────────────┐
│              CROSS-DOMAIN THOUGHT EXAMPLE                        │
│                                                                  │
│  Thought: "Ad Spend Increase Affecting Cash Flow"               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  MARKETING DOMAIN:                                               │
│    - Ad Spend: $1.2M this month (↑40%)                          │
│    - Revenue from Ads: $3.6M (ROAS 3.0)                         │
│                                                                  │
│  FINANCE DOMAIN:                                                │
│    - Payment Terms: Net 30 (revenue delayed)                    │
│    - Cash Position: $800k                                       │
│    - Projected Shortfall: -$400k in 2 weeks                     │
│                                                                  │
│  OPERATIONS DOMAIN:                                              │
│    - Inventory: Low on 3 top-selling SKUs                       │
│    - Fulfillment Capacity: 92% utilized                         │
│                                                                  │
│  INSIGHT: Aggressive ad spend + revenue lag + inventory         │
│           constraints = potential fulfillment failure           │
│                                                                  │
│  RECOMMENDED: Reduce ad spend 20% until cash position           │
│               improves and inventory restocked                  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 5.5 Threshold Configuration

Thresholds are configured per metric and can be:

| Threshold Type | Description | Example |
|----------------|-------------|---------|
| **Absolute** | Fixed value | CPC > $5.00 |
| **Relative** | Percentage change | CTR drops 20% |
| **Comparative** | Vs benchmark | ROAS below industry avg |
| **Time-based** | Over period | Spend increasing 3 days straight |
| **Compound** | Multiple conditions | CPC > $3 AND CTR < 1% |

---

## 6. AI Video Agent

### 6.1 Agent Personality

```
┌─────────────────────────────────────────────────────────────────┐
│                    VIDEO AGENT PERSONA                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Name: [Customizable per tenant]                                │
│  Tone: Professional, friendly, concise                          │
│  Style: Data-driven, actionable, encouraging                    │
│                                                                  │
│  Communication Principles:                                       │
│  1. Lead with the most important insight                        │
│  2. Quantify impact whenever possible                           │
│  3. Offer clear next steps                                      │
│  4. Acknowledge good performance, not just problems             │
│  5. Use analogies for complex concepts                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 6.2 Daily Briefing Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    DAILY BRIEFING STRUCTURE                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. GREETING (5 seconds)                                        │
│     "Good morning, [Name]! Here's your marketing update         │
│      for [Date]."                                               │
│                                                                  │
│  2. HEADLINE (10 seconds)                                       │
│     "Overall, yesterday was [positive/challenging].             │
│      Your total spend was $X with $Y in revenue."               │
│                                                                  │
│  3. TOP THOUGHTS (30-45 seconds)                                │
│     "I've identified 3 things that need your attention:         │
│      First, [Thought 1 summary]...                              │
│      Second, [Thought 2 summary]...                             │
│      Third, [Thought 3 summary]..."                             │
│                                                                  │
│  4. WINS (15 seconds)                                           │
│     "On the positive side, [Campaign X] hit a record            │
│      ROAS of 5.2, and your email campaigns generated            │
│      $X in revenue."                                            │
│                                                                  │
│  5. RECOMMENDED ACTIONS (15 seconds)                            │
│     "Based on this, I recommend:                                │
│      1. [Action 1]                                              │
│      2. [Action 2]                                              │
│      You can execute these with one click below."               │
│                                                                  │
│  6. HANDOFF (5 seconds)                                         │
│     "Is there anything specific you'd like to explore?          │
│      Just ask me."                                              │
│                                                                  │
│  Total Duration: ~60-90 seconds                                 │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 6.3 Interactive Q&A

The agent can answer questions like:

| Question Type | Example | Agent Response |
|---------------|---------|----------------|
| **Metric Query** | "What's my CTR this week?" | "[Queries data] Your CTR is 3.2%, up 8% from last week." |
| **Comparison** | "How does Meta compare to Google?" | "[Compares platforms] Meta has higher CTR but Google has better ROAS..." |
| **Root Cause** | "Why did CPC spike?" | "[Analyzes data] Looking at your campaigns, it seems competitor X increased bids..." |
| **Recommendation** | "Should I increase budget?" | "[Evaluates] Based on current ROAS of 4.2, yes, a 15% increase could yield..." |
| **Forecast** | "What will revenue be next month?" | "[Predicts] Based on trends, I estimate $X, assuming current spend levels." |

### 6.4 Video Presence

- **Avatar**: AI-generated human avatar (customizable)
- **Background**: Branded or neutral options
- **Expressions**: Matching tone (concerned for problems, pleased for wins)
- **Gestures**: Natural hand movements for emphasis
- **Display**: Seamless integration with data visualizations

---

## 7. Action System

### 7.1 Action Types

| Type | Description | Execution |
|------|-------------|-----------|
| **Informational** | "Review this campaign" | Links to detailed view |
| **Manual** | "Reduce bids by 15%" | User executes in platform |
| **Semi-Automated** | "Pause these 3 campaigns" | One-click with confirmation |
| **Automated** | "Apply bid adjustments" | Executes via API (future) |

### 7.2 Action Card Structure

```
┌─────────────────────────────────────────────────────────────────┐
│                        ACTION CARD                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  [Priority Badge: HIGH]                                         │
│                                                                  │
│  ACTION: Pause underperforming Meta campaigns                   │
│                                                                  │
│  DETAILS:                                                       │
│  - Campaigns: "Summer Sale", "Brand Awareness Q4"               │
│  - Current ROAS: 0.8 (below 1.0 threshold)                      │
│  - Spend to Date: $12,400                                       │
│                                                                  │
│  EXPECTED IMPACT:                                               │
│  - Save: ~$800/day                                              │
│  - Lost Conversions: ~5/day (low-value)                         │
│  - Net Benefit: Positive                                        │
│                                                                  │
│  SOURCE: Thought "Ad Efficiency Declining"                      │
│                                                                  │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐                 │
│  │  EXECUTE   │  │  SCHEDULE  │  │   DISMISS  │                 │
│  │    NOW     │  │   FOR...   │  │            │                 │
│  └────────────┘  └────────────┘  └────────────┘                 │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 7.3 Future Integrations

Actions will integrate with platforms for automated execution:

| Platform | Possible Actions |
|----------|-----------------|
| **Google Ads** | Pause/enable campaigns, adjust bids, update budgets |
| **Meta Ads** | Pause/enable ad sets, modify targeting, adjust spend |
| **Klaviyo** | Start/stop flows, schedule campaigns, update segments |
| **Slack** | Post alerts, send summaries, request approvals |
| **Email** | Send reports, alert stakeholders |

---

## 8. User Journeys

### 8.1 Daily Check-In (5 minutes)

```
USER OPENS APP
       │
       ▼
┌──────────────────┐
│ Video Agent      │
│ plays briefing   │──▶ User watches 60-90 second update
└──────────────────┘
       │
       ▼
┌──────────────────┐
│ Scan Thoughts    │──▶ See 2-3 priority items flagged
└──────────────────┘
       │
       ▼
┌──────────────────┐
│ Review Actions   │──▶ Execute 1-2 quick wins
└──────────────────┘
       │
       ▼
┌──────────────────┐
│ Ask Question     │──▶ "How did email perform yesterday?"
└──────────────────┘
       │
       ▼
   DONE (5 min)
```

### 8.2 Issue Investigation (15 minutes)

```
USER SEES THOUGHT "CPC SPIKE"
       │
       ▼
┌──────────────────┐
│ Click Thought    │──▶ Expand to see full analysis
└──────────────────┘
       │
       ▼
┌──────────────────┐
│ View Blast       │──▶ Understand what else is affected
│ Radius           │
└──────────────────┘
       │
       ▼
┌──────────────────┐
│ Ask Agent        │──▶ "Why did this happen?"
│ for Root Cause   │
└──────────────────┘
       │
       ▼
┌──────────────────┐
│ Drill into       │──▶ Navigate to Core Performance thoughtlet
│ Thoughtlet       │
└──────────────────┘
       │
       ▼
┌──────────────────┐
│ Filter to        │──▶ Identify specific problematic campaigns
│ Problem Area     │
└──────────────────┘
       │
       ▼
┌──────────────────┐
│ Take Action      │──▶ Pause or adjust campaigns
└──────────────────┘
       │
       ▼
   ISSUE ADDRESSED
```

### 8.3 Deep Dive Analysis (30+ minutes)

```
USER WANTS TO UNDERSTAND TRENDS
       │
       ▼
┌──────────────────┐
│ Select           │──▶ Choose Revenue & LTV thoughtlet
│ Thoughtlet       │
└──────────────────┘
       │
       ▼
┌──────────────────┐
│ Set Date Range   │──▶ Last 90 days
└──────────────────┘
       │
       ▼
┌──────────────────┐
│ Apply Filters    │──▶ Channel: All, Segment: High-value
└──────────────────┘
       │
       ▼
┌──────────────────┐
│ Analyze Charts   │──▶ Identify cohort patterns
└──────────────────┘
       │
       ▼
┌──────────────────┐
│ Export Data      │──▶ CSV for further analysis
└──────────────────┘
       │
       ▼
┌──────────────────┐
│ Ask Complex      │──▶ "Which acquisition channels have
│ Questions        │    best 90-day LTV?"
└──────────────────┘
       │
       ▼
┌──────────────────┐
│ Compare Cross-   │──▶ Switch between thoughtlets
│ Thoughtlet       │    to correlate findings
└──────────────────┘
       │
       ▼
   INSIGHTS DOCUMENTED
```

---

## 9. Use Cases & Examples

### 9.1 Use Case: Budget Alert

**Scenario:** It's 2pm and the daily budget is 95% exhausted.

**What Happens:**
1. **Metric Change**: Budget utilization hits 95%
2. **Threshold Breach**: Warning at 80%, Critical at 95%
3. **Thought Triggered**: "Budget Exhaustion Risk"
4. **Blast Radius**: Impression share will drop, conversions will stop
5. **Agent Analysis**: "At current pace, you'll miss ~120 conversions today"
6. **Actions Generated**:
   - Increase daily budget by 20% (if ROAS justifies)
   - Reduce bids to extend coverage
   - Accept lower afternoon coverage

**User Experience:**
- Gets push notification/email
- Video agent mentions in briefing
- Thought card appears prominently
- One-click to increase budget

### 9.2 Use Case: Creative Fatigue

**Scenario:** A top-performing ad's CTR has declined 40% over 2 weeks.

**What Happens:**
1. **Pattern Detected**: CTR decay rate > 5%/week for 14+ days
2. **Thought Triggered**: "Creative Fatigue Detected"
3. **Context Added**:
   - Frequency reached 8.5 (audience seeing ad too often)
   - Originally CTR was 4.2%, now 2.5%
   - Still 35% of spend going to this creative
4. **Actions Generated**:
   - Rotate in new creative variants
   - Reduce budget allocation by 50%
   - Test 2-3 new messages

**Agent Briefing:**
> "Your 'Summer Vibes' creative is showing fatigue. CTR dropped from 4.2% to 2.5%
> over two weeks. I'd recommend rotating in fresh creatives or reducing its
> budget allocation. Want me to show you which variants are available?"

### 9.3 Use Case: Cross-Platform Opportunity

**Scenario:** Email campaigns are driving 40% of revenue but only getting 10% of focus.

**What Happens:**
1. **Pattern Detected**: Email revenue/effort ratio significantly higher than paid
2. **Thought Triggered**: "Underutilized High-Performing Channel"
3. **Data Points**:
   - Email ROAS: 42:1 (vs paid 3:1)
   - Email capacity: 60% utilized
   - Customer overlap: 25% of email list not receiving campaigns
4. **Actions Generated**:
   - Increase email send frequency
   - Launch win-back campaign to inactive
   - Test SMS for highest-value segment

---

## 10. Future Scope

### 10.1 Phase 2: Thought Cascading

When one thought triggers, analyze if it affects other thoughts:

```
Thought A: "CPC Increasing"
    │
    ├──▶ Affects Thought B: "Budget Pressure"
    │         │
    │         └──▶ Affects Thought C: "Cash Flow Risk"
    │
    └──▶ Affects Thought D: "ROAS Declining"
              │
              └──▶ Affects Thought E: "Revenue Target at Risk"
```

### 10.2 Phase 3: Multi-Domain Expansion

| Domain | Data Sources | Example Thoughts |
|--------|--------------|------------------|
| **Finance** | QuickBooks, Xero | Cash flow impact of ad spend |
| **Sales** | Salesforce, HubSpot | Lead quality from marketing |
| **Operations** | Inventory systems | Stock levels vs campaign scale |
| **Customer Success** | Support tickets | Churn indicators from marketing |

### 10.3 Phase 4: Predictive Thoughts

Move from reactive (what happened) to predictive (what will happen):

- "Based on current trends, ROAS will drop below 2.0 in 5 days"
- "Competitor activity suggests CPCs will increase next week"
- "Seasonal patterns indicate email performance will peak in 3 days"

### 10.4 Phase 5: Autonomous Actions

With approval workflows:

```
┌────────────────────────────────────────┐
│ AUTONOMOUS ACTION REQUEST              │
├────────────────────────────────────────┤
│                                        │
│ Action: Pause "Brand Campaign Alpha"   │
│ Reason: ROAS below 0.5 for 7 days     │
│ Impact: Save $1,200/day               │
│                                        │
│ [APPROVE]  [MODIFY]  [REJECT]         │
│                                        │
│ Auto-approve if no response in 4 hrs  │
│                                        │
└────────────────────────────────────────┘
```

### 10.5 Technical Roadmap

| Phase | Features | Timeline |
|-------|----------|----------|
| **MVP** | 13 thoughtlets, basic thoughts, manual actions | Current |
| **V1.1** | Video agent, natural language Q&A | +2 months |
| **V1.2** | Knowledge graph UI, threshold configuration | +3 months |
| **V2.0** | Cross-domain (Finance), thought cascading | +6 months |
| **V3.0** | Predictive analytics, autonomous actions | +12 months |

---

## Appendix

### A. Glossary

| Term | Definition |
|------|------------|
| **Metric** | A single KPI or measurement (e.g., CPC, CTR) |
| **Thoughtlet** | A dashboard grouping related metrics (formerly "Dashboard") |
| **Thought** | An AI-generated insight triggered by threshold breaches |
| **Action** | A recommended next step generated from a thought |
| **Blast Radius** | The set of metrics affected by a change |
| **Threshold** | A defined limit that triggers thought generation |
| **Knowledge Graph** | The relationship map between all metrics and thoughts |

### B. Related Documents

- [Technical Architecture](./TECHNICAL_ARCHITECTURE.md)
- [Dashboard Specifications](./AGENT_DASHBOARD_MAPPING.md)
- [Data Schema](../dbt/models/marts/schema.yml)

---

*Last Updated: December 2024*
*Version: 1.0*
