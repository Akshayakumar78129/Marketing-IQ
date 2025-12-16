{{
    config(
        materialized='table',
        tags=['dimensions']
    )
}}

/*
    Device dimension table
    Combines device data from GA4 and ad platforms
    Source: GA4.TECH_DEVICE_CATEGORY_REPORT, GOOGLE_ADS.CAMPAIGN_STATS
*/

with ga4_devices as (
    select distinct
        device_category as device_type
    from {{ source('ga4', 'tech_device_category_report') }}
    where device_category is not null
),

google_ads_devices as (
    select distinct
        device as device_type
    from {{ source('google_ads', 'campaign_stats') }}
    where device is not null
),

all_devices as (
    select device_type from ga4_devices
    union
    select device_type from google_ads_devices
)

select
    {{ dbt_utils.generate_surrogate_key(['device_type']) }} as device_sk,
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
