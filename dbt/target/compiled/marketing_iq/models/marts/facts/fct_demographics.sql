

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
    from CLIENT_RARE_SEEDS_DB.GA4.demographic_age_report
    
    where _fivetran_synced > (select max(last_synced) from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_demographics)
    
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
    from CLIENT_RARE_SEEDS_DB.GA4.demographic_gender_report
    
    where _fivetran_synced > (select max(last_synced) from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_demographics)
    
),

combined as (
    select * from age_data
    union all
    select * from gender_data
)

select
    md5(cast(coalesce(cast(date_day as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(property as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(demographic_type as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(age_bracket as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(gender as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as demographics_sk,
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