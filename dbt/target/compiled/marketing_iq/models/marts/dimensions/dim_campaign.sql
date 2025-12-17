

/*
    Unified campaign dimension table
    Combines Google Ads and Facebook Ads campaigns (SCD Type 2)
    Source: GOOGLE_ADS.CAMPAIGN_HISTORY, FACEBOOK_ADS.CAMPAIGN_HISTORY
*/

with google_ads_campaigns as (
    select
        'google_ads' as platform,
        id::varchar as campaign_id,
        customer_id::varchar as account_id,
        name as campaign_name,
        status,
        advertising_channel_type as campaign_type,
        advertising_channel_subtype as campaign_subtype,
        start_date,
        end_date,
        null::number as daily_budget,
        null::number as lifetime_budget,
        null::text as objective,
        _fivetran_active as is_current,
        _fivetran_start as valid_from,
        _fivetran_end as valid_to,
        _fivetran_synced as last_synced
    from CLIENT_RARE_SEEDS_DB.GOOGLE_ADS.campaign_history
    where _fivetran_active = true
),

facebook_ads_campaigns as (
    select
        'meta' as platform,
        id::varchar as campaign_id,
        account_id::varchar as account_id,
        name as campaign_name,
        status,
        'SOCIAL' as campaign_type,
        null as campaign_subtype,
        start_time::date::text as start_date,
        stop_time::date::text as end_date,
        daily_budget,
        lifetime_budget,
        objective,
        true as is_current,
        created_time as valid_from,
        null::timestamp_tz as valid_to,
        _fivetran_synced as last_synced
    from CLIENT_RARE_SEEDS_DB.META_ADS.campaign_history
),

combined as (
    select * from google_ads_campaigns
    union all
    select * from facebook_ads_campaigns
)

select
    md5(cast(coalesce(cast(platform as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(campaign_id as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as campaign_sk,
    platform,
    campaign_id,
    account_id,
    campaign_name,
    status,
    campaign_type,
    campaign_subtype,
    start_date,
    end_date,
    daily_budget,
    lifetime_budget,
    objective,
    is_current,
    valid_from,
    valid_to,
    last_synced
from combined