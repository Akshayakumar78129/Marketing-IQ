
  
    

create or replace transient table CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_ga4_geo
    
    
    
    as (

/*
    GA4 Geographic Traffic Fact Table
    Traffic and engagement metrics by country, region, and city
    Source: GA4.DEMOGRAPHIC_COUNTRY_REPORT, DEMOGRAPHIC_REGION_REPORT, DEMOGRAPHIC_CITY_REPORT
*/

with country_data as (
    select
        date as date_day,
        property as ga4_property,
        country as location_value,
        'country' as geo_level,
        total_users as users,
        new_users,
        engaged_sessions,
        engagement_rate,
        event_count as events,
        key_events as conversions,
        total_revenue as revenue,
        _fivetran_synced as last_synced
    from CLIENT_RARE_SEEDS_DB.GA4.demographic_country_report
    
),

region_data as (
    select
        date as date_day,
        property as ga4_property,
        region as location_value,
        'region' as geo_level,
        total_users as users,
        new_users,
        engaged_sessions,
        engagement_rate,
        event_count as events,
        key_events as conversions,
        total_revenue as revenue,
        _fivetran_synced as last_synced
    from CLIENT_RARE_SEEDS_DB.GA4.demographic_region_report
    
),

city_data as (
    select
        date as date_day,
        property as ga4_property,
        city as location_value,
        'city' as geo_level,
        total_users as users,
        new_users,
        engaged_sessions,
        engagement_rate,
        event_count as events,
        key_events as conversions,
        total_revenue as revenue,
        _fivetran_synced as last_synced
    from CLIENT_RARE_SEEDS_DB.GA4.demographic_city_report
    
),

combined as (
    select * from country_data
    union all
    select * from region_data
    union all
    select * from city_data
)

select
    md5(cast(coalesce(cast(date_day as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(ga4_property as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(geo_level as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(location_value as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as ga4_geo_sk,
    'ga4' as source_platform,
    date_day,
    date_trunc('week', date_day)::date as date_week,
    date_trunc('month', date_day)::date as date_month,
    ga4_property,

    -- Geographic info
    geo_level,
    coalesce(location_value, '(not set)') as location_value,

    -- Region classification (for country level)
    case
        when geo_level = 'country' then
            case
                when location_value in ('United States', 'US') then 'Domestic'
                when location_value in ('Canada', 'CA') then 'North America'
                when location_value in ('United Kingdom', 'Germany', 'France', 'Netherlands', 'Sweden', 'Switzerland', 'Ireland', 'Spain', 'Italy') then 'Europe'
                when location_value in ('Australia', 'New Zealand') then 'APAC'
                else 'International'
            end
        else null
    end as region_classification,

    -- Metrics
    users,
    new_users,
    engaged_sessions,
    engagement_rate,
    events,
    conversions,
    revenue,

    -- Calculated metrics
    case when users > 0 then new_users::float / users else 0 end as new_user_rate,
    case when users > 0 then engaged_sessions::float / users else 0 end as engaged_sessions_per_user,
    case when users > 0 then conversions::float / users else 0 end as conversion_rate,
    case when users > 0 then revenue / users else 0 end as revenue_per_user,
    case when conversions > 0 then revenue / conversions else 0 end as revenue_per_conversion,

    last_synced
from combined
    )
;


  