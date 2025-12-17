

/*
    Audience Daily Performance Fact Table
    Grain: Audience × Date
    Source: GA4.AUDIENCES_REPORT
*/

with audience_data as (
    select
        date as date_day,
        property,
        audience_name,
        sessions,
        new_users,
        active_users,
        screen_page_views_per_session,
        average_session_duration,
        total_revenue as revenue,
        _fivetran_synced as last_synced
    from CLIENT_RARE_SEEDS_DB.GA4.audiences_report
)

select
    md5(cast(coalesce(cast(date_day as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(property as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(audience_name as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as audience_performance_sk,
    'ga4' as platform,
    date_day,
    property,
    audience_name,

    -- Metrics
    sessions,
    new_users,
    active_users,
    screen_page_views_per_session,
    average_session_duration,
    revenue,

    -- Calculated metrics
    case when active_users > 0 then sessions::float / active_users else 0 end as sessions_per_user,
    case when active_users > 0 then revenue / active_users else 0 end as revenue_per_user,
    case when sessions > 0 then new_users::float / sessions else 0 end as new_user_rate,

    last_synced
from audience_data