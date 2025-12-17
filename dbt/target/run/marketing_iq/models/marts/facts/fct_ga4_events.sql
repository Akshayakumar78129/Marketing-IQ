
  
    

create or replace transient table CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_ga4_events
    
    
    
    as (

/*
    GA4 Events Fact Table
    Event-level aggregated metrics
    Source: GA4.EVENTS_REPORT
*/

with events as (
    select
        date as date_day,
        property as ga4_property,
        event_name,
        event_count,
        total_users as users,
        event_count_per_user,
        total_revenue as revenue,
        _fivetran_synced as last_synced
    from CLIENT_RARE_SEEDS_DB.GA4.events_report
    
)

select
    md5(cast(coalesce(cast(date_day as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(ga4_property as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(event_name as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as ga4_event_sk,
    'ga4' as platform,
    date_day,
    ga4_property,
    event_name,

    -- Event category
    case
        when event_name in ('purchase', 'add_to_cart', 'begin_checkout', 'add_payment_info', 'add_shipping_info') then 'Ecommerce'
        when event_name in ('page_view', 'scroll', 'click', 'view_item', 'view_item_list') then 'Engagement'
        when event_name in ('sign_up', 'login', 'generate_lead') then 'Conversion'
        when event_name in ('session_start', 'first_visit', 'user_engagement') then 'Session'
        when event_name like 'video%' then 'Video'
        when event_name like 'file%' then 'File'
        else 'Other'
    end as event_category,

    -- Is this a key/conversion event?
    case
        when event_name in ('purchase', 'generate_lead', 'sign_up', 'begin_checkout') then true
        else false
    end as is_key_event,

    -- Metrics
    event_count,
    users,
    event_count_per_user,
    revenue,

    -- Calculated metrics
    case when users > 0 then revenue / users else 0 end as revenue_per_user,
    case when event_count > 0 then revenue / event_count else 0 end as revenue_per_event,

    last_synced
from events
    )
;


  