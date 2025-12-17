
  
    

create or replace transient table CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_ga4_pages
    
    
    
    as (

/*
    GA4 Pages Fact Table
    Page-level performance with engagement metrics
    Source: GA4.PAGES_PATH_REPORT
*/

with pages as (
    select
        date as date_day,
        property as ga4_property,
        page_path,
        screen_page_views as page_views,
        total_users as users,
        new_users,
        event_count as events,
        key_events as conversions,
        user_engagement_duration as engagement_duration_seconds,
        total_revenue as revenue,
        _fivetran_synced as last_synced
    from CLIENT_RARE_SEEDS_DB.GA4.pages_path_report
    
)

select
    md5(cast(coalesce(cast(date_day as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(ga4_property as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(page_path as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as ga4_page_sk,
    'ga4' as platform,
    date_day,
    ga4_property,
    page_path,

    -- Extract page components
    split_part(page_path, '?', 1) as page_path_clean,
    case
        when page_path = '/' then 'Homepage'
        when page_path like '/product%' then 'Product Page'
        when page_path like '/collection%' then 'Collection Page'
        when page_path like '/cart%' then 'Cart'
        when page_path like '/checkout%' then 'Checkout'
        when page_path like '/account%' then 'Account'
        when page_path like '/blog%' then 'Blog'
        when page_path like '/search%' then 'Search'
        else 'Other'
    end as page_type,

    -- Metrics
    page_views,
    users,
    new_users,
    events,
    conversions,
    engagement_duration_seconds,
    revenue,

    -- Calculated metrics
    case when users > 0 then page_views::float / users else 0 end as pages_per_user,
    case when users > 0 then engagement_duration_seconds::float / users else 0 end as avg_engagement_per_user,
    case when users > 0 then conversions::float / users else 0 end as conversion_rate,
    case when users > 0 then revenue / users else 0 end as revenue_per_user,
    case when page_views > 0 then revenue / page_views else 0 end as revenue_per_pageview,

    last_synced
from pages
    )
;


  