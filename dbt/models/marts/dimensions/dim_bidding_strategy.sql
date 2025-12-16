{{
    config(
        materialized='table',
        tags=['dimensions']
    )
}}

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
    from {{ source('google_ads', 'campaign_history') }}
    where _fivetran_active = true
)

select
    {{ dbt_utils.generate_surrogate_key(['campaign_id', 'bidding_strategy_type']) }} as bidding_strategy_sk,
    'google_ads' as platform,
    campaign_id,
    account_id,
    bidding_type,
    bidding_strategy_type,
    last_synced
from campaign_bidding
