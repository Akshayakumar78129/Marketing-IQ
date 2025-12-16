{{
    config(
        materialized='incremental',
        unique_key='ga4_traffic_sk',
        tags=['facts', 'daily', 'ga4']
    )
}}

/*
    GA4 Traffic Daily Fact Table
    Grain: Source/Medium × Date
    Source: GA4.TRAFFIC_ACQUISITION_SESSION_SOURCE_MEDIUM_REPORT
*/

with traffic_data as (
    select
        date as date_day,
        property,
        session_source as source,
        session_medium as medium,
        sessions,
        engaged_sessions,
        engagement_rate,
        events_per_session,
        user_engagement_duration,
        key_events as conversions,
        total_users,
        event_count,
        total_revenue as revenue,
        _fivetran_synced as last_synced
    from {{ source('ga4', 'traffic_acquisition_session_source_medium_report') }}
    {% if is_incremental() %}
    where _fivetran_synced > (select max(last_synced) from {{ this }})
    {% endif %}
)

select
    {{ dbt_utils.generate_surrogate_key(['date_day', 'property', 'source', 'medium']) }} as ga4_traffic_sk,
    'ga4' as platform,
    date_day,
    property,
    source,
    medium,
    coalesce(source, '(direct)') || ' / ' || coalesce(medium, '(none)') as source_medium,

    -- Metrics
    sessions,
    engaged_sessions,
    total_users,
    event_count,
    conversions,
    revenue,

    -- Engagement metrics
    engagement_rate,
    events_per_session,
    user_engagement_duration,

    -- Calculated metrics
    case when sessions > 0 then engaged_sessions::float / sessions else 0 end as calculated_engagement_rate,
    case when total_users > 0 then sessions::float / total_users else 0 end as sessions_per_user,

    last_synced
from traffic_data
