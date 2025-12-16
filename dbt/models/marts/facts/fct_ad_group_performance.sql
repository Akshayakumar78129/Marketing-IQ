{{
    config(
        materialized='incremental',
        unique_key='ad_group_performance_sk',
        tags=['facts', 'daily']
    )
}}

/*
    Ad Group Daily Performance Fact Table
    Grain: Ad Group × Date × Device × Ad Network Type
    Source: GOOGLE_ADS.AD_GROUP_STATS
*/

with ad_group_stats as (
    select
        date as date_day,
        id::varchar as ad_group_id,
        campaign_id::varchar as campaign_id,
        customer_id::varchar as account_id,
        device,
        ad_network_type,
        sum(impressions) as impressions,
        sum(clicks) as clicks,
        sum(cost_micros) / 1000000.0 as spend,
        sum(conversions) as conversions,
        sum(conversions_value) as conversion_value,
        sum(interactions) as interactions,
        sum(view_through_conversions) as view_through_conversions,
        sum(active_view_impressions) as active_view_impressions,
        avg(active_view_viewability) as active_view_viewability,
        max(_fivetran_synced) as last_synced
    from {{ source('google_ads', 'ad_group_stats') }}
    {% if is_incremental() %}
    where _fivetran_synced > (select max(last_synced) from {{ this }})
    {% endif %}
    group by date, id, campaign_id, customer_id, device, ad_network_type
)

select
    {{ dbt_utils.generate_surrogate_key(['date_day', 'ad_group_id', 'device', 'ad_network_type']) }} as ad_group_performance_sk,
    'google_ads' as platform,
    date_day,
    ad_group_id,
    campaign_id,
    account_id,
    device,
    ad_network_type,

    -- Metrics
    impressions,
    clicks,
    spend,
    conversions,
    conversion_value,
    interactions,
    view_through_conversions,
    active_view_impressions,
    active_view_viewability,

    -- Calculated metrics
    case when impressions > 0 then clicks::float / impressions else 0 end as ctr,
    case when clicks > 0 then spend / clicks else 0 end as cpc,
    case when impressions > 0 then (spend / impressions) * 1000 else 0 end as cpm,
    case when spend > 0 then conversion_value / spend else 0 end as roas,
    case when conversions > 0 then spend / conversions else 0 end as cpa,

    last_synced
from ad_group_stats
