{{
    config(
        materialized='incremental',
        unique_key='search_term_sk',
        tags=['facts', 'daily']
    )
}}

/*
    Search Term Daily Performance Fact Table
    Grain: Keyword × Search Term × Date
    Source: GOOGLE_ADS.SEARCH_TERM_STATS
*/

with search_term_stats as (
    select
        date as date_day,
        search_term,
        search_term_match_type as match_type,
        ad_group_id::varchar as ad_group_id,
        campaign_id::varchar as campaign_id,
        customer_id::varchar as account_id,
        status,
        impressions,
        clicks,
        cost_micros / 1000000.0 as spend,
        conversions,
        view_through_conversions,
        ctr,
        average_cpc,
        absolute_top_impression_percentage,
        top_impression_percentage,
        _fivetran_synced as last_synced
    from {{ source('google_ads', 'search_term_stats') }}
    {% if is_incremental() %}
    where _fivetran_synced > (select max(last_synced) from {{ this }})
    {% endif %}
)

select
    {{ dbt_utils.generate_surrogate_key(['date_day', 'search_term', 'ad_group_id', 'match_type']) }} as search_term_sk,
    'google_ads' as platform,
    date_day,
    search_term,
    match_type,
    ad_group_id,
    campaign_id,
    account_id,
    status,

    -- Metrics
    impressions,
    clicks,
    spend,
    conversions,
    view_through_conversions,

    -- Provided metrics
    ctr,
    average_cpc,
    absolute_top_impression_percentage,
    top_impression_percentage,

    -- Calculated metrics (backup)
    case
        when ctr is null and impressions > 0 then clicks::float / impressions
        else ctr
    end as calculated_ctr,
    case
        when average_cpc is null and clicks > 0 then spend / clicks
        else average_cpc
    end as calculated_cpc,

    last_synced
from search_term_stats
