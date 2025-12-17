{{
    config(
        materialized='table',
        tags=['facts', 'customers', 'cac', 'retention', 'cohort']
    )
}}

/*
    Customer Metrics Fact Table
    Monthly cohort-based customer acquisition, retention, and CAC metrics
    Sources: KLAVIYO.EVENT, KLAVIYO.PERSON, GOOGLE_ADS.CAMPAIGN_STATS, META_ADS.BASIC_CAMPAIGN
*/

with placed_order_metric as (
    select id as metric_id
    from {{ source('klaviyo', 'metric') }}
    where lower(name) = 'placed order'
),

-- Get all orders with customer info
orders as (
    select
        e.person_id,
        date(e.datetime) as order_date,
        e.property_value as order_value
    from {{ source('klaviyo', 'event') }} e
    inner join placed_order_metric m on e.metric_id = m.metric_id
),

-- Calculate customer-level metrics
customer_stats as (
    select
        person_id,
        min(order_date) as first_order_date,
        max(order_date) as last_order_date,
        count(*) as total_orders,
        sum(order_value) as lifetime_value,
        datediff('day', min(order_date), max(order_date)) as customer_lifespan_days
    from orders
    group by person_id
),

-- Cohort assignments
customer_cohorts as (
    select
        person_id,
        date_trunc('month', first_order_date)::date as cohort_month,
        first_order_date,
        last_order_date,
        total_orders,
        lifetime_value,
        customer_lifespan_days,
        case when total_orders > 1 then true else false end as is_repeat_customer,
        -- Retention flags (did they order again within X days?)
        case when datediff('day', first_order_date, last_order_date) >= 30 and total_orders > 1 then true else false end as retained_30d,
        case when datediff('day', first_order_date, last_order_date) >= 60 and total_orders > 1 then true else false end as retained_60d,
        case when datediff('day', first_order_date, last_order_date) >= 90 and total_orders > 1 then true else false end as retained_90d
    from customer_stats
),

-- Aggregate by cohort month
cohort_metrics as (
    select
        cohort_month,
        count(*) as new_customers,
        sum(case when is_repeat_customer then 1 else 0 end) as repeat_customers,
        sum(case when not is_repeat_customer then 1 else 0 end) as one_time_customers,
        sum(total_orders) as total_orders,
        round(sum(lifetime_value), 2) as total_revenue,
        round(avg(lifetime_value), 2) as avg_customer_ltv,
        round(avg(total_orders), 2) as avg_orders_per_customer,
        -- Retention rates
        sum(case when retained_30d then 1 else 0 end) as retained_30d_count,
        sum(case when retained_60d then 1 else 0 end) as retained_60d_count,
        sum(case when retained_90d then 1 else 0 end) as retained_90d_count
    from customer_cohorts
    group by cohort_month
),

-- Google Ads spend by month
google_spend as (
    select
        date_trunc('month', date)::date as spend_month,
        round(sum(cost_micros) / 1000000, 2) as google_ads_spend
    from {{ source('google_ads', 'campaign_stats') }}
    group by spend_month
),

-- Meta Ads spend by month
meta_spend as (
    select
        date_trunc('month', date)::date as spend_month,
        round(sum(spend), 2) as meta_ads_spend
    from {{ source('meta_ads', 'basic_campaign') }}
    group by spend_month
),

-- Combine spend
monthly_spend as (
    select
        coalesce(g.spend_month, m.spend_month) as spend_month,
        coalesce(g.google_ads_spend, 0) as google_ads_spend,
        coalesce(m.meta_ads_spend, 0) as meta_ads_spend,
        coalesce(g.google_ads_spend, 0) + coalesce(m.meta_ads_spend, 0) as total_ad_spend
    from google_spend g
    full outer join meta_spend m on g.spend_month = m.spend_month
)

select
    {{ dbt_utils.generate_surrogate_key(['c.cohort_month']) }} as customer_metrics_sk,
    c.cohort_month,

    -- Customer counts
    c.new_customers,
    c.repeat_customers,
    c.one_time_customers,

    -- Repeat purchase rate
    round(c.repeat_customers::float / nullif(c.new_customers, 0) * 100, 2) as repeat_purchase_rate,

    -- Order metrics
    c.total_orders,
    c.avg_orders_per_customer,

    -- Revenue metrics
    c.total_revenue,
    c.avg_customer_ltv,
    round(c.total_revenue / nullif(c.new_customers, 0), 2) as revenue_per_customer,

    -- Ad spend
    coalesce(s.google_ads_spend, 0) as google_ads_spend,
    coalesce(s.meta_ads_spend, 0) as meta_ads_spend,
    coalesce(s.total_ad_spend, 0) as total_ad_spend,

    -- CAC (Customer Acquisition Cost)
    round(coalesce(s.total_ad_spend, 0) / nullif(c.new_customers, 0), 2) as cac,
    round(coalesce(s.google_ads_spend, 0) / nullif(c.new_customers, 0), 2) as cac_google,
    round(coalesce(s.meta_ads_spend, 0) / nullif(c.new_customers, 0), 2) as cac_meta,

    -- CAC Payback (months to recover CAC from LTV)
    round(coalesce(s.total_ad_spend, 0) / nullif(c.total_revenue, 0), 2) as cac_to_revenue_ratio,

    -- Retention counts
    c.retained_30d_count,
    c.retained_60d_count,
    c.retained_90d_count,

    -- Retention rates
    round(c.retained_30d_count::float / nullif(c.new_customers, 0) * 100, 2) as retention_rate_30d,
    round(c.retained_60d_count::float / nullif(c.new_customers, 0) * 100, 2) as retention_rate_60d,
    round(c.retained_90d_count::float / nullif(c.new_customers, 0) * 100, 2) as retention_rate_90d,

    -- LTV:CAC Ratio (healthy is > 3:1)
    round(c.avg_customer_ltv / nullif(coalesce(s.total_ad_spend, 0) / nullif(c.new_customers, 0), 0), 2) as ltv_cac_ratio

from cohort_metrics c
left join monthly_spend s on c.cohort_month = s.spend_month
order by c.cohort_month desc
