{{
    config(
        materialized='table',
        tags=['facts', 'daily', 'meta']
    )
}}

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
    from {{ source('meta_ads', 'basic_ad') }}
)

select
    {{ dbt_utils.generate_surrogate_key(['date_day', 'ad_id']) }} as ad_reactions_sk,
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
