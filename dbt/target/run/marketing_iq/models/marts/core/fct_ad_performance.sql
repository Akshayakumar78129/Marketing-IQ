
  
    

create or replace transient table CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_ad_performance
    
    
    
    as (

/*
    Unified ad performance fact table
    Combines Google Ads and Facebook Ads ad-level data
    Source: GOOGLE_ADS.AD_STATS, FACEBOOK_ADS.BASIC_AD
*/

with google_ads_stats as (
    select
        date as date_day,
        customer_id::varchar as account_id,
        campaign_id::varchar as campaign_id,
        ad_group_id::varchar as ad_group_id,
        ad_id::varchar as ad_id,
        device,
        ad_network_type,
        sum(impressions) as impressions,
        sum(clicks) as clicks,
        sum(cost_micros) / 1000000.0 as spend,
        sum(conversions) as conversions,
        sum(conversions_value) as conversion_value,
        sum(view_through_conversions) as view_through_conversions,
        max(_fivetran_synced) as last_synced
    from CLIENT_RARE_SEEDS_DB.GOOGLE_ADS.ad_stats
    group by date, customer_id, campaign_id, ad_group_id, ad_id, device, ad_network_type
),

google_ads_ad_info as (
    select
        id::varchar as ad_id,
        ad_group_id::varchar as ad_group_id,
        name as ad_name,
        status as ad_status,
        type as ad_type,
        display_url
    from CLIENT_RARE_SEEDS_DB.GOOGLE_ADS.ad_history
    where _fivetran_active = true
),

google_ads as (
    select
        s.date_day,
        'google_ads' as platform,
        s.account_id,
        s.campaign_id,
        s.ad_group_id,
        null::varchar as ad_set_id,
        s.ad_id,
        coalesce(a.ad_name, 'Unknown') as ad_name,
        a.ad_type,
        a.ad_status as status,
        a.display_url,
        s.device,
        s.ad_network_type,
        s.impressions,
        s.clicks,
        s.spend,
        s.conversions,
        s.conversion_value,
        s.view_through_conversions,
        s.last_synced
    from google_ads_stats s
    left join google_ads_ad_info a on s.ad_id = a.ad_id
),

facebook_ads as (
    select
        date as date_day,
        'meta' as platform,
        account_id::varchar as account_id,
        null::varchar as campaign_id,
        null::varchar as ad_group_id,
        null::varchar as ad_set_id,
        ad_id::varchar as ad_id,
        ad_name,
        null as ad_type,
        null as status,
        null as display_url,
        null as device,
        null as ad_network_type,
        impressions,
        inline_link_clicks as clicks,
        spend,
        null as conversions,
        null as conversion_value,
        null as view_through_conversions,
        _fivetran_synced as last_synced
    from CLIENT_RARE_SEEDS_DB.META_ADS.basic_ad
),

combined as (
    select * from google_ads
    union all
    select * from facebook_ads
)

select
    md5(cast(coalesce(cast(date_day as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(platform as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(ad_id as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(device as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(ad_network_type as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as ad_performance_sk,
    date_day,
    platform,
    account_id,
    campaign_id,
    ad_group_id,
    ad_set_id,
    ad_id,
    ad_name,
    ad_type,
    status,
    display_url,
    device,
    ad_network_type,

    -- Metrics
    impressions,
    clicks,
    spend,
    conversions,
    conversion_value,
    view_through_conversions,

    -- Calculated metrics
    case when impressions > 0 then clicks::float / impressions else 0 end as ctr,
    case when clicks > 0 then spend / clicks else 0 end as cpc,
    case when impressions > 0 then (spend / impressions) * 1000 else 0 end as cpm,
    case when spend > 0 then conversion_value / spend else 0 end as roas,
    case when conversions > 0 then spend / conversions else 0 end as cpa,

    last_synced
from combined
    )
;


  