{{
    config(
        materialized='incremental',
        unique_key='demographics_sk',
        tags=['facts', 'daily', 'ga4']
    )
}}

/*
    Demographics Daily Fact Table
    Grain: Age/Gender × Date
    Source: GA4.DEMOGRAPHIC_AGE_REPORT, GA4.DEMOGRAPHIC_GENDER_REPORT
*/

with age_data as (
    select
        date as date_day,
        property,
        user_age_bracket as age_bracket,
        null as gender,
        'age' as demographic_type,
        engaged_sessions,
        engagement_rate,
        new_users,
        event_count,
        total_users,
        key_events as conversions,
        total_revenue as revenue,
        _fivetran_synced as last_synced
    from {{ source('ga4', 'demographic_age_report') }}
    {% if is_incremental() %}
    where _fivetran_synced > (select max(last_synced) from {{ this }})
    {% endif %}
),

gender_data as (
    select
        date as date_day,
        property,
        null as age_bracket,
        user_gender as gender,
        'gender' as demographic_type,
        engaged_sessions,
        engagement_rate,
        new_users,
        event_count,
        total_users,
        key_events as conversions,
        total_revenue as revenue,
        _fivetran_synced as last_synced
    from {{ source('ga4', 'demographic_gender_report') }}
    {% if is_incremental() %}
    where _fivetran_synced > (select max(last_synced) from {{ this }})
    {% endif %}
),

combined as (
    select * from age_data
    union all
    select * from gender_data
)

select
    {{ dbt_utils.generate_surrogate_key(['date_day', 'property', 'demographic_type', 'age_bracket', 'gender']) }} as demographics_sk,
    'ga4' as platform,
    date_day,
    property,
    demographic_type,
    age_bracket,
    gender,

    -- Metrics
    engaged_sessions,
    engagement_rate,
    new_users,
    total_users,
    event_count,
    conversions,
    revenue,

    -- Calculated metrics
    case when total_users > 0 then conversions / total_users else 0 end as conversion_rate,
    case when total_users > 0 then revenue / total_users else 0 end as revenue_per_user,

    last_synced
from combined
