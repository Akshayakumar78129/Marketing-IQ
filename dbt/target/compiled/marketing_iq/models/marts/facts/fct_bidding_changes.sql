

/*
    Bidding Changes History Fact Table
    Grain: Campaign Bidding Strategy × Change Date
    Source: GOOGLE_ADS.CAMPAIGN_BIDDING_STRATEGY_HISTORY
    Tracks all changes to bidding strategies over time (SCD Type 2)
*/

with bidding_changes as (
    select
        campaign_id::varchar as campaign_id,
        name as bidding_strategy_name,
        type as bidding_strategy_type,
        status as bidding_strategy_status,
        target_cpa_micros / 1000000.0 as target_cpa,
        target_roas,
        cpc_bid_ceiling_micros / 1000000.0 as cpc_bid_ceiling,
        cpc_bid_floor_micros / 1000000.0 as cpc_bid_floor,
        enhanced_cpc_enabled,
        _fivetran_start as valid_from,
        _fivetran_end as valid_to,
        _fivetran_active as is_current,
        _fivetran_synced as last_synced
    from CLIENT_RARE_SEEDS_DB.GOOGLE_ADS.campaign_bidding_strategy_history
    
    where _fivetran_synced > (select max(last_synced) from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_bidding_changes)
    
)

select
    md5(cast(coalesce(cast(campaign_id as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(valid_from as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as bidding_change_sk,
    'google_ads' as platform,
    campaign_id,
    bidding_strategy_name,
    bidding_strategy_type,
    bidding_strategy_status,
    target_cpa,
    target_roas,
    cpc_bid_ceiling,
    cpc_bid_floor,
    enhanced_cpc_enabled,
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
from bidding_changes