

/*
    Unified Ad dimension table
    Combines Google Ads and Facebook Ads ads (SCD Type 2)
    Source: GOOGLE_ADS.AD_HISTORY, FACEBOOK_ADS.AD_HISTORY
*/

with google_ads_raw as (
    select
        'google_ads' as platform,
        id::varchar as ad_id,
        ad_group_id::varchar as ad_group_id,
        null::varchar as ad_set_id,
        null::varchar as campaign_id,
        name as ad_name,
        status,
        type as ad_type,
        display_url,
        final_urls,
        null::varchar as creative_id,
        _fivetran_active as is_current,
        _fivetran_start as valid_from,
        _fivetran_end as valid_to,
        _fivetran_synced as last_synced,
        row_number() over (partition by id order by _fivetran_synced desc) as rn
    from CLIENT_RARE_SEEDS_DB.GOOGLE_ADS.ad_history
    where _fivetran_active = true
),

google_ads as (
    select
        platform, ad_id, ad_group_id, ad_set_id, campaign_id, ad_name, status,
        ad_type, display_url, final_urls, creative_id, is_current, valid_from, valid_to, last_synced
    from google_ads_raw
    where rn = 1
),

facebook_ads_raw as (
    select
        'meta' as platform,
        id::varchar as ad_id,
        null::varchar as ad_group_id,
        ad_set_id::varchar as ad_set_id,
        campaign_id::varchar as campaign_id,
        name as ad_name,
        status,
        null as ad_type,
        null as display_url,
        null as final_urls,
        creative_id::varchar as creative_id,
        true as is_current,
        created_time as valid_from,
        null::timestamp_tz as valid_to,
        _fivetran_synced as last_synced,
        row_number() over (partition by id order by _fivetran_synced desc) as rn
    from CLIENT_RARE_SEEDS_DB.META_ADS.ad_history
),

facebook_ads as (
    select
        platform, ad_id, ad_group_id, ad_set_id, campaign_id, ad_name, status,
        ad_type, display_url, final_urls, creative_id, is_current, valid_from, valid_to, last_synced
    from facebook_ads_raw
    where rn = 1
),

combined as (
    select * from google_ads
    union all
    select * from facebook_ads
)

select
    md5(cast(coalesce(cast(platform as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(ad_id as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as ad_sk,
    platform,
    ad_id,
    ad_group_id,
    ad_set_id,
    campaign_id,
    ad_name,
    status,
    ad_type,
    display_url,
    final_urls,
    creative_id,
    is_current,
    valid_from,
    valid_to,
    last_synced
from combined