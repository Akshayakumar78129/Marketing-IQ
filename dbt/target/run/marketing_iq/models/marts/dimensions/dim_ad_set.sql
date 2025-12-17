
  
    

create or replace transient table CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.dim_ad_set
    
    
    
    as (

/*
    Facebook Ads Ad Set dimension table
    Source: FACEBOOK_ADS.AD_SET_HISTORY
*/

with ad_sets as (
    select
        id::varchar as ad_set_id,
        campaign_id::varchar as campaign_id,
        account_id::varchar as account_id,
        name as ad_set_name,
        status,
        effective_status,
        optimization_goal,
        billing_event,
        bid_strategy,
        bid_amount,
        daily_budget,
        lifetime_budget,
        start_time,
        end_time,
        targeting_age_min,
        targeting_age_max,
        is_dynamic_creative,
        created_time,
        updated_time,
        _fivetran_synced as last_synced
    from CLIENT_RARE_SEEDS_DB.META_ADS.ad_set_history
)

select
    md5(cast(coalesce(cast(ad_set_id as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as ad_set_sk,
    'meta' as platform,
    ad_set_id,
    campaign_id,
    account_id,
    ad_set_name,
    status,
    effective_status,
    optimization_goal,
    billing_event,
    bid_strategy,
    bid_amount,
    daily_budget,
    lifetime_budget,
    start_time,
    end_time,
    targeting_age_min,
    targeting_age_max,
    is_dynamic_creative,
    created_time,
    updated_time,
    last_synced
from ad_sets
    )
;


  