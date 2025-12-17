
  
    

create or replace transient table CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_ad_reactions
    
    
    
    as (

/*
    Ad Reactions Daily Fact Table (Facebook)
    Grain: Ad × Date
    Note: Using basic ad data - reactions data if available in schema
    Source: FACEBOOK_ADS.BASIC_AD
*/

with ad_performance as (
    select
        date as date_day,
        ad_id::varchar as ad_id,
        account_id::varchar as account_id,
        ad_name,
        impressions,
        reach,
        inline_link_clicks as clicks,
        spend,
        frequency,
        _fivetran_synced as last_synced
    from CLIENT_RARE_SEEDS_DB.META_ADS.basic_ad
)

select
    md5(cast(coalesce(cast(date_day as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(ad_id as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as ad_reactions_sk,
    'meta' as platform,
    date_day,
    ad_id,
    account_id,
    ad_name,

    -- Base metrics
    impressions,
    reach,
    clicks,
    spend,
    frequency,

    -- Engagement proxy (using reach as engagement indicator)
    case when impressions > 0 then reach::float / impressions else 0 end as unique_reach_rate,
    case when reach > 0 then clicks::float / reach else 0 end as clicks_per_reach,

    last_synced
from ad_performance
    )
;


  