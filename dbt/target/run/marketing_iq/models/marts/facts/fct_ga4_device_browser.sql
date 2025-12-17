
  
    

create or replace transient table CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_ga4_device_browser
    
    
    
    as (

/*
    GA4 Device & Browser Distribution Fact Table
    Traffic and engagement metrics by device category, browser, and platform
    Source: GA4.TECH_DEVICE_CATEGORY_REPORT, TECH_BROWSER_REPORT, TECH_PLATFORM_REPORT
*/

with device_data as (
    select
        date as date_day,
        property as ga4_property,
        device_category,
        null as browser,
        null as platform,
        'device' as dimension_type,
        total_users as users,
        new_users,
        engaged_sessions,
        engagement_rate,
        event_count as events,
        key_events as conversions,
        total_revenue as revenue,
        _fivetran_synced as last_synced
    from CLIENT_RARE_SEEDS_DB.GA4.tech_device_category_report
    
),

browser_data as (
    select
        date as date_day,
        property as ga4_property,
        null as device_category,
        browser,
        null as platform,
        'browser' as dimension_type,
        total_users as users,
        new_users,
        engaged_sessions,
        engagement_rate,
        event_count as events,
        key_events as conversions,
        total_revenue as revenue,
        _fivetran_synced as last_synced
    from CLIENT_RARE_SEEDS_DB.GA4.tech_browser_report
    
),

platform_data as (
    select
        date as date_day,
        property as ga4_property,
        null as device_category,
        null as browser,
        platform,
        'platform' as dimension_type,
        total_users as users,
        new_users,
        engaged_sessions,
        engagement_rate,
        event_count as events,
        key_events as conversions,
        total_revenue as revenue,
        _fivetran_synced as last_synced
    from CLIENT_RARE_SEEDS_DB.GA4.tech_platform_report
    
),

combined as (
    select * from device_data
    union all
    select * from browser_data
    union all
    select * from platform_data
)

select
    md5(cast(coalesce(cast(date_day as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(ga4_property as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(dimension_type as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(device_category as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(browser as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(platform as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as device_browser_sk,
    'ga4' as source_platform,
    date_day,
    date_trunc('week', date_day)::date as date_week,
    date_trunc('month', date_day)::date as date_month,
    ga4_property,

    -- Dimension info
    dimension_type,
    coalesce(device_category, browser, platform) as dimension_value,
    device_category,
    browser,
    platform,

    -- Friendly device names
    case
        when device_category = 'desktop' then 'Desktop'
        when device_category = 'mobile' then 'Mobile'
        when device_category = 'tablet' then 'Tablet'
        when device_category = 'smart_tv' then 'Smart TV'
        else device_category
    end as device_category_display,

    -- Browser grouping
    case
        when lower(browser) like '%chrome%' then 'Chrome'
        when lower(browser) like '%safari%' then 'Safari'
        when lower(browser) like '%firefox%' then 'Firefox'
        when lower(browser) like '%edge%' then 'Edge'
        when lower(browser) like '%samsung%' then 'Samsung Internet'
        when lower(browser) in ('android webview', 'webview') then 'WebView'
        else coalesce(browser, 'Other')
    end as browser_group,

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


  