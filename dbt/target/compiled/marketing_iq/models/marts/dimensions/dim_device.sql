

/*
    Device dimension table
    Combines device data from GA4 and ad platforms
    Source: GA4.TECH_DEVICE_CATEGORY_REPORT, GOOGLE_ADS.CAMPAIGN_STATS
*/

with ga4_devices as (
    select distinct
        device_category as device_type
    from CLIENT_RARE_SEEDS_DB.GA4.tech_device_category_report
    where device_category is not null
),

google_ads_devices as (
    select distinct
        device as device_type
    from CLIENT_RARE_SEEDS_DB.GOOGLE_ADS.campaign_stats
    where device is not null
),

all_devices as (
    select device_type from ga4_devices
    union
    select device_type from google_ads_devices
)

select
    md5(cast(coalesce(cast(device_type as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as device_sk,
    device_type,
    case
        when lower(device_type) in ('mobile', 'connected_tv', 'tablet') then 'Mobile/Tablet'
        when lower(device_type) in ('desktop', 'computer') then 'Desktop'
        else 'Other'
    end as device_category,
    case
        when lower(device_type) in ('mobile', 'connected_tv', 'tablet') then true
        else false
    end as is_mobile
from all_devices