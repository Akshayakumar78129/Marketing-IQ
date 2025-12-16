{{
    config(
        materialized='incremental',
        unique_key='first_touch_sk',
        tags=['facts', 'ga4', 'attribution']
    )
}}

/*
    GA4 First-Touch Attribution Fact Table
    User acquisition metrics with first-touch attribution
    Source: GA4.USER_ACQUISITION_FIRST_USER_SOURCE_MEDIUM_REPORT
*/

with first_touch as (
    select
        date as date_day,
        property as ga4_property,
        first_user_source,
        first_user_medium,
        total_users as users,
        new_users,
        engaged_sessions,
        engagement_rate,
        user_engagement_duration as engagement_duration_seconds,
        event_count as events,
        key_events as conversions,
        total_revenue as revenue,
        _fivetran_synced as last_synced
    from {{ source('ga4', 'user_acquisition_first_user_source_medium_report') }}
    {% if is_incremental() %}
    where _fivetran_synced > (select max(last_synced) from {{ this }})
    {% endif %}
)

select
    {{ dbt_utils.generate_surrogate_key(['date_day', 'ga4_property', 'first_user_source', 'first_user_medium']) }} as first_touch_sk,
    'ga4' as platform,
    date_day,
    ga4_property,
    first_user_source,
    first_user_medium,

    -- Source/Medium combined
    coalesce(first_user_source, '(direct)') || ' / ' || coalesce(first_user_medium, '(none)') as source_medium,

    -- Channel grouping (simplified)
    case
        when first_user_medium = 'organic' then 'Organic Search'
        when first_user_medium in ('cpc', 'ppc', 'paid') then 'Paid Search'
        when first_user_medium in ('cpm', 'display', 'banner') then 'Display'
        when first_user_source like '%facebook%' or first_user_source like '%instagram%' then 'Paid Social'
        when first_user_medium = 'email' then 'Email'
        when first_user_medium = 'referral' then 'Referral'
        when first_user_source = '(direct)' or first_user_medium = '(none)' then 'Direct'
        else 'Other'
    end as channel_grouping,

    -- Metrics
    users,
    new_users,
    engaged_sessions,
    engagement_rate,
    engagement_duration_seconds,
    events,
    conversions,
    revenue,

    -- Calculated metrics
    case when users > 0 then conversions::float / users else 0 end as conversion_rate,
    case when users > 0 then revenue / users else 0 end as revenue_per_user,
    case when new_users > 0 then revenue / new_users else 0 end as revenue_per_new_user,
    case when users > 0 then engagement_duration_seconds::float / users else 0 end as avg_engagement_per_user,

    last_synced
from first_touch
