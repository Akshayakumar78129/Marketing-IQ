{{
    config(
        materialized='incremental',
        unique_key='delivery_sk',
        tags=['facts', 'meta', 'delivery']
    )
}}

/*
    Meta Ads Delivery Fact Table
    Performance metrics by device and platform (Facebook, Instagram, etc.)
    Source: META_ADS.DELIVERY_DEVICE, DELIVERY_PLATFORM
*/

with device_data as (
    select
        account_id::varchar as account_id,
        date as date_day,
        device_platform as dimension_value,
        'device' as dimension_type,
        impressions,
        reach,
        inline_link_clicks as clicks,
        spend,
        cpc,
        cpm,
        ctr,
        frequency,
        _fivetran_synced as last_synced
    from {{ source('meta_ads', 'delivery_device') }}
    {% if is_incremental() %}
    where _fivetran_synced > (select max(last_synced) from {{ this }})
    {% endif %}
),

platform_data as (
    select
        account_id::varchar as account_id,
        date as date_day,
        publisher_platform as dimension_value,
        'platform' as dimension_type,
        impressions,
        reach,
        inline_link_clicks as clicks,
        spend,
        cpc,
        cpm,
        ctr,
        frequency,
        _fivetran_synced as last_synced
    from {{ source('meta_ads', 'delivery_platform') }}
    {% if is_incremental() %}
    where _fivetran_synced > (select max(last_synced) from {{ this }})
    {% endif %}
),

combined as (
    select * from device_data
    union all
    select * from platform_data
)

select
    {{ dbt_utils.generate_surrogate_key(['account_id', 'date_day', 'dimension_type', 'dimension_value']) }} as delivery_sk,
    'meta' as platform,
    account_id,
    date_day,
    dimension_type,
    dimension_value,

    -- Friendly names
    case dimension_type
        when 'device' then
            case dimension_value
                when 'mobile_app' then 'Mobile App'
                when 'mobile_web' then 'Mobile Web'
                when 'desktop' then 'Desktop'
                else dimension_value
            end
        when 'platform' then
            case dimension_value
                when 'facebook' then 'Facebook'
                when 'instagram' then 'Instagram'
                when 'audience_network' then 'Audience Network'
                when 'messenger' then 'Messenger'
                else dimension_value
            end
        else dimension_value
    end as dimension_display_name,

    -- Metrics
    impressions,
    reach,
    clicks,
    spend,
    frequency,

    -- Rates
    cpc,
    cpm,
    ctr,

    -- Calculated metrics (backup)
    case when ctr is null and impressions > 0 then clicks::float / impressions else ctr end as calculated_ctr,
    case when cpc is null and clicks > 0 then spend / clicks else cpc end as calculated_cpc,

    last_synced
from combined
