

/*
    Keyword Daily Performance Fact Table
    Grain: Keyword × Date × Device
    Source: GOOGLE_ADS.KEYWORD_STATS
*/

with keyword_stats as (
    select
        date as date_day,
        ad_group_criterion_criterion_id::varchar as keyword_id,
        ad_group_id::varchar as ad_group_id,
        campaign_id::varchar as campaign_id,
        customer_id::varchar as account_id,
        device,
        ad_network_type,
        impressions,
        clicks,
        cost_micros / 1000000.0 as spend,
        conversions,
        conversions_value as conversion_value,
        interactions,
        view_through_conversions,
        _fivetran_synced as last_synced
    from CLIENT_RARE_SEEDS_DB.GOOGLE_ADS.keyword_stats
    
    where _fivetran_synced > (select max(last_synced) from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_keyword_performance)
    
)

select
    md5(cast(coalesce(cast(date_day as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(keyword_id as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(ad_group_id as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(device as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(ad_network_type as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as keyword_performance_sk,
    'google_ads' as platform,
    date_day,
    keyword_id,
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

    -- Calculated metrics
    case when impressions > 0 then clicks::float / impressions else 0 end as ctr,
    case when clicks > 0 then spend / clicks else 0 end as cpc,
    case when impressions > 0 then (spend / impressions) * 1000 else 0 end as cpm,
    case when spend > 0 then conversion_value / spend else 0 end as roas,
    case when conversions > 0 then spend / conversions else 0 end as cpa,

    last_synced
from keyword_stats