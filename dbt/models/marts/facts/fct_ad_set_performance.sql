{{
    config(
        materialized='incremental',
        unique_key='ad_set_performance_sk',
        tags=['facts', 'daily']
    )
}}

/*
    Ad Set Daily Performance Fact Table (Facebook)
    Grain: Ad Set × Date
    Source: FACEBOOK_ADS.BASIC_AD_SET
*/

with ad_set_stats as (
    select
        date as date_day,
        adset_id::varchar as ad_set_id,
        account_id::varchar as account_id,
        adset_name as ad_set_name,
        campaign_name,
        impressions,
        reach,
        inline_link_clicks as clicks,
        spend,
        cpc,
        cpm,
        ctr,
        frequency,
        _fivetran_synced as last_synced
    from {{ source('meta_ads', 'basic_ad_set') }}
    {% if is_incremental() %}
    where _fivetran_synced > (select max(last_synced) from {{ this }})
    {% endif %}
)

select
    {{ dbt_utils.generate_surrogate_key(['date_day', 'ad_set_id']) }} as ad_set_performance_sk,
    'meta' as platform,
    date_day,
    ad_set_id,
    account_id,
    ad_set_name,
    campaign_name,

    -- Metrics
    impressions,
    reach,
    clicks,
    spend,
    frequency,

    -- Provided metrics
    cpc,
    cpm,
    ctr,

    -- Calculated metrics (backup if provided are null)
    case
        when ctr is null and impressions > 0 then clicks::float / impressions
        else ctr
    end as calculated_ctr,
    case
        when cpc is null and clicks > 0 then spend / clicks
        else cpc
    end as calculated_cpc,

    last_synced
from ad_set_stats
