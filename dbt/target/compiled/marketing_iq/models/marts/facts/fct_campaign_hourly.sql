

/*
    Campaign Hourly Performance Fact Table
    Grain: Campaign × Date × Hour × Device × Ad Network Type
    Source: GOOGLE_ADS.CAMPAIGN_HOURLY_STATS
*/

with hourly_stats as (
    select
        date as date_day,
        hour,
        id::varchar as campaign_id,
        customer_id::varchar as account_id,
        device,
        ad_network_type,
        sum(impressions) as impressions,
        sum(clicks) as clicks,
        sum(cost_micros) / 1000000.0 as spend,
        sum(conversions) as conversions,
        sum(conversions_value) as conversion_value,
        sum(interactions) as interactions,
        max(_fivetran_synced) as last_synced
    from CLIENT_RARE_SEEDS_DB.GOOGLE_ADS.campaign_hourly_stats
    
    where _fivetran_synced > (select max(last_synced) from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_campaign_hourly)
    
    group by date, hour, id, customer_id, device, ad_network_type
)

select
    md5(cast(coalesce(cast(date_day as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(hour as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(campaign_id as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(device as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(ad_network_type as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as hourly_performance_sk,
    'google_ads' as platform,
    date_day,
    hour,
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

    -- Calculated metrics
    case when impressions > 0 then clicks::float / impressions else 0 end as ctr,
    case when clicks > 0 then spend / clicks else 0 end as cpc,
    case when impressions > 0 then (spend / impressions) * 1000 else 0 end as cpm,
    case when spend > 0 then conversion_value / spend else 0 end as roas,
    case when conversions > 0 then spend / conversions else 0 end as cpa,

    last_synced
from hourly_stats