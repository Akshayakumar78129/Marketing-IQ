
  
    

create or replace transient table CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_meta_device_performance
    
    
    
    as (

/*
    Meta Ads Device & Platform Performance Fact Table
    Performance metrics by device platform and publisher platform
    Source: META_ADS.DELIVERY_PLATFORM_AND_DEVICE
*/

with device_platform_data as (
    select
        account_id,
        date as date_day,
        device_platform,
        publisher_platform,
        impressions,
        reach,
        inline_link_clicks as clicks,
        spend,
        cpm,
        cpc,
        ctr,
        cost_per_inline_link_click,
        frequency,
        _fivetran_synced as last_synced
    from CLIENT_RARE_SEEDS_DB.META_ADS.delivery_platform_and_device
    
)

select
    md5(cast(coalesce(cast(date_day as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(account_id as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(device_platform as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(publisher_platform as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as device_performance_sk,
    'meta_ads' as source_platform,
    account_id,
    date_day,
    date_trunc('week', date_day)::date as date_week,
    date_trunc('month', date_day)::date as date_month,

    -- Platform dimensions
    publisher_platform,
    device_platform,

    -- Friendly display names
    case
        when publisher_platform = 'facebook' then 'Facebook'
        when publisher_platform = 'instagram' then 'Instagram'
        when publisher_platform = 'audience_network' then 'Audience Network'
        when publisher_platform = 'messenger' then 'Messenger'
        when publisher_platform = 'threads' then 'Threads'
        else coalesce(publisher_platform, 'Unknown')
    end as publisher_platform_display,

    case
        when device_platform = 'mobile_app' then 'Mobile App'
        when device_platform = 'mobile_web' then 'Mobile Web'
        when device_platform = 'desktop' then 'Desktop'
        else coalesce(device_platform, 'Unknown')
    end as device_platform_display,

    -- Device category grouping
    case
        when device_platform in ('mobile_app', 'mobile_web') then 'Mobile'
        when device_platform = 'desktop' then 'Desktop'
        else 'Other'
    end as device_category,

    -- Core metrics
    impressions,
    reach,
    clicks,
    round(spend, 2) as spend,

    -- Rate metrics
    round(cpm, 2) as cpm,
    round(cpc, 2) as cpc,
    round(ctr, 4) as ctr,
    round(cost_per_inline_link_click, 2) as cost_per_click,
    round(frequency, 2) as frequency,

    -- Calculated metrics
    case when impressions > 0 then round(clicks::float / impressions * 100, 4) else 0 end as click_rate,
    case when reach > 0 then round(impressions::float / reach, 2) else 0 end as impressions_per_reach,
    case when clicks > 0 then round(spend / clicks, 2) else 0 end as actual_cpc,

    last_synced
from device_platform_data
where impressions > 0 or spend > 0
    )
;


  