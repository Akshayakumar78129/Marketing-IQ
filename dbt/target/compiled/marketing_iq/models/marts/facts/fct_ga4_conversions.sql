

/*
    GA4 Conversions Daily Fact Table
    Grain: Conversion Event × Date
    Source: GA4.CONVERSIONS_REPORT
*/

with conversions_data as (
    select
        date as date_day,
        property,
        event_name as conversion_event,
        total_users,
        key_events as conversions,
        total_revenue as revenue,
        _fivetran_synced as last_synced
    from CLIENT_RARE_SEEDS_DB.GA4.conversions_report
    
    where _fivetran_synced > (select max(last_synced) from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_ga4_conversions)
    
)

select
    md5(cast(coalesce(cast(date_day as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(property as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(conversion_event as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as ga4_conversion_sk,
    'ga4' as platform,
    date_day,
    property,
    conversion_event,

    -- Metrics
    total_users,
    conversions,
    revenue,

    -- Calculated metrics
    case when total_users > 0 then conversions / total_users else 0 end as conversion_rate,
    case when conversions > 0 then revenue / conversions else 0 end as revenue_per_conversion,

    last_synced
from conversions_data