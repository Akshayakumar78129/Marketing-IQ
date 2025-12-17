

/*
    Campaign Settings History Fact Table
    Grain: Campaign × Change Date
    Source: GOOGLE_ADS.CAMPAIGN_HISTORY
    Tracks all changes to campaign settings over time (SCD Type 2)
*/

with campaign_changes as (
    select
        id::varchar as campaign_id,
        customer_id::varchar as account_id,
        name as campaign_name,
        status as campaign_status,
        advertising_channel_type,
        advertising_channel_subtype,
        start_date,
        end_date,
        _fivetran_start as valid_from,
        _fivetran_end as valid_to,
        _fivetran_active as is_current,
        _fivetran_synced as last_synced
    from CLIENT_RARE_SEEDS_DB.GOOGLE_ADS.campaign_history
    
    where _fivetran_synced > (select max(last_synced) from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_campaign_settings_history)
    
)

select
    md5(cast(coalesce(cast(campaign_id as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(valid_from as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as campaign_settings_sk,
    'google_ads' as platform,
    campaign_id,
    account_id,
    campaign_name,
    campaign_status,
    advertising_channel_type,
    advertising_channel_subtype,
    start_date,
    end_date,
    valid_from,
    valid_to,
    is_current,

    -- Change tracking
    date(valid_from) as change_date,
    case
        when valid_to is null then datediff('day', date(valid_from), current_date())
        else datediff('day', date(valid_from), date(valid_to))
    end as days_active,

    last_synced
from campaign_changes