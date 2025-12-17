

/*
    Budget Changes History Fact Table
    Grain: Campaign Budget × Change Date
    Source: GOOGLE_ADS.CAMPAIGN_BUDGET_HISTORY
    Tracks all changes to campaign budgets over time (SCD Type 2)
*/

with budget_changes as (
    select
        id::varchar as budget_id,
        campaign_id::varchar as campaign_id,
        name as budget_name,
        amount_micros / 1000000.0 as budget_amount,
        delivery_method,
        explicitly_shared as is_shared_budget,
        period as budget_period,
        reference_count,
        status as budget_status,
        type as budget_type,
        _fivetran_start as valid_from,
        _fivetran_end as valid_to,
        _fivetran_active as is_current,
        _fivetran_synced as last_synced
    from CLIENT_RARE_SEEDS_DB.GOOGLE_ADS.campaign_budget_history
    
    where _fivetran_synced > (select max(last_synced) from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_budget_changes)
    
)

select
    md5(cast(coalesce(cast(budget_id as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(campaign_id as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(valid_from as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as budget_change_sk,
    'google_ads' as platform,
    budget_id,
    campaign_id,
    budget_name,
    budget_amount,
    delivery_method,
    is_shared_budget,
    budget_period,
    reference_count,
    budget_status,
    budget_type,
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
from budget_changes