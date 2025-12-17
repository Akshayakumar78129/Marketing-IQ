
  
    

create or replace transient table CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_budget_utilization
    
    
    
    as (

/*
    Budget Utilization Fact Table
    Tracks daily budget vs actual spend for Google Ads campaigns
    Source: GOOGLE_ADS.CAMPAIGN_BUDGET_HISTORY, GOOGLE_ADS.CAMPAIGN_STATS
*/

with budget_history as (
    select
        campaign_id,
        id as budget_id,
        amount_micros / 1000000.0 as daily_budget,
        delivery_method,
        period,
        status as budget_status,
        type as budget_type,
        has_recommended_budget,
        recommended_budget_amount_micros / 1000000.0 as recommended_budget,
        _fivetran_start as valid_from,
        _fivetran_end as valid_to,
        _fivetran_active as is_current
    from CLIENT_RARE_SEEDS_DB.GOOGLE_ADS.campaign_budget_history
),

-- Get current budgets for each campaign
current_budgets as (
    select
        campaign_id,
        budget_id,
        daily_budget,
        delivery_method,
        period,
        budget_status,
        budget_type,
        has_recommended_budget,
        recommended_budget
    from budget_history
    where is_current = true
),

-- Daily campaign spend
daily_spend as (
    select
        date as date_day,
        id as campaign_id,
        customer_id as account_id,
        sum(cost_micros) / 1000000.0 as daily_spend,
        sum(impressions) as impressions,
        sum(clicks) as clicks,
        sum(conversions) as conversions,
        sum(conversions_value) as conversion_value
    from CLIENT_RARE_SEEDS_DB.GOOGLE_ADS.campaign_stats
    group by date, id, customer_id
),

-- Campaign info
campaign_info as (
    select
        id as campaign_id,
        customer_id as account_id,
        name as campaign_name,
        status as campaign_status,
        advertising_channel_type as campaign_type
    from CLIENT_RARE_SEEDS_DB.GOOGLE_ADS.campaign_history
    where _fivetran_active = true
),

-- Join budget with spend
budget_utilization as (
    select
        s.date_day,
        s.account_id,
        s.campaign_id,
        c.campaign_name,
        c.campaign_status,
        c.campaign_type,

        -- Budget info
        b.budget_id,
        b.daily_budget,
        b.delivery_method,
        b.period as budget_period,
        b.budget_status,
        b.budget_type,
        b.has_recommended_budget,
        b.recommended_budget,

        -- Spend info
        s.daily_spend,
        s.impressions,
        s.clicks,
        s.conversions,
        s.conversion_value
    from daily_spend s
    left join current_budgets b on s.campaign_id = b.campaign_id
    left join campaign_info c on s.campaign_id = c.campaign_id
)

select
    md5(cast(coalesce(cast(date_day as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(campaign_id as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as budget_utilization_sk,
    'google_ads' as platform,
    date_day,
    date_trunc('week', date_day)::date as date_week,
    date_trunc('month', date_day)::date as date_month,

    -- Identifiers
    account_id,
    campaign_id,
    budget_id,
    campaign_name,
    campaign_status,
    campaign_type,

    -- Budget configuration
    daily_budget,
    delivery_method,
    budget_period,
    budget_status,
    budget_type,
    has_recommended_budget,
    recommended_budget,

    -- Actual spend
    daily_spend,

    -- Utilization metrics
    case
        when daily_budget > 0 then round((daily_spend / daily_budget) * 100, 2)
        else null
    end as utilization_pct,

    -- Utilization flags
    case
        when daily_budget > 0 and daily_spend > daily_budget then true
        else false
    end as is_overspend,

    case
        when daily_budget > 0 and daily_spend < daily_budget * 0.8 then true
        else false
    end as is_underspend,

    -- Over/under spend amount
    case
        when daily_budget > 0 then round(daily_spend - daily_budget, 2)
        else null
    end as spend_variance,

    -- Utilization category
    case
        when daily_budget is null or daily_budget = 0 then 'No Budget Set'
        when daily_spend >= daily_budget * 1.2 then 'Significantly Overspent (>120%)'
        when daily_spend > daily_budget then 'Overspent (100-120%)'
        when daily_spend >= daily_budget * 0.8 then 'On Track (80-100%)'
        when daily_spend >= daily_budget * 0.5 then 'Underspent (50-80%)'
        else 'Significantly Underspent (<50%)'
    end as utilization_category,

    -- Performance metrics
    impressions,
    clicks,
    conversions,
    conversion_value,

    -- Efficiency metrics
    case when clicks > 0 then round(daily_spend / clicks, 2) else 0 end as cpc,
    case when impressions > 0 then round(clicks::float / impressions * 100, 4) else 0 end as ctr,
    case when daily_spend > 0 then round(conversion_value / daily_spend, 2) else 0 end as roas,

    -- Budget efficiency (conversions per budget dollar)
    case
        when daily_budget > 0 then round(conversions / daily_budget, 4)
        else null
    end as conversions_per_budget_dollar,

    -- Recommended budget gap
    case
        when has_recommended_budget and recommended_budget > 0
        then round(recommended_budget - daily_budget, 2)
        else null
    end as recommended_budget_gap

from budget_utilization
where daily_spend > 0 or daily_budget > 0
    )
;


  