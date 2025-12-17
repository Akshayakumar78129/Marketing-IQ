

/*
    Bidding Strategy dimension table
    Source: GOOGLE_ADS.BIDDING_STRATEGY_HISTORY
    Note: Uses campaign-level bidding info if dedicated table not available
*/

-- Using campaign history for bidding strategy info
with campaign_bidding as (
    select distinct
        id::varchar as campaign_id,
        customer_id::varchar as account_id,
        payment_mode as bidding_type,
        -- Derive bidding strategy from campaign settings
        case
            when payment_mode = 'CONVERSIONS' then 'TARGET_CPA'
            when payment_mode = 'CONVERSION_VALUE' then 'TARGET_ROAS'
            when payment_mode = 'CLICKS' then 'MAXIMIZE_CLICKS'
            else 'MANUAL'
        end as bidding_strategy_type,
        _fivetran_synced as last_synced
    from CLIENT_RARE_SEEDS_DB.GOOGLE_ADS.campaign_history
    where _fivetran_active = true
)

select
    md5(cast(coalesce(cast(campaign_id as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(bidding_strategy_type as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as bidding_strategy_sk,
    'google_ads' as platform,
    campaign_id,
    account_id,
    bidding_type,
    bidding_strategy_type,
    last_synced
from campaign_bidding