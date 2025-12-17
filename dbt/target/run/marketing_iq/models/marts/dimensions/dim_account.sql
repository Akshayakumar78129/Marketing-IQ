
  
    

create or replace transient table CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.dim_account
    
    
    
    as (

/*
    Unified account dimension table
    Combines Google Ads and Facebook Ads accounts
    Source: GOOGLE_ADS.ACCOUNT_HISTORY, FACEBOOK_ADS.ACCOUNT_HISTORY
*/

with google_ads_accounts as (
    select
        'google_ads' as platform,
        id::varchar as account_id,
        descriptive_name as account_name,
        currency_code,
        time_zone,
        case when test_account = true then 'TEST' else 'ACTIVE' end as account_status,
        manager as is_manager_account,
        _fivetran_active as is_current,
        _fivetran_start as valid_from,
        _fivetran_end as valid_to,
        _fivetran_synced as last_synced
    from CLIENT_RARE_SEEDS_DB.GOOGLE_ADS.account_history
    where _fivetran_active = true
),

facebook_ads_accounts_raw as (
    select
        'meta' as platform,
        id::varchar as account_id,
        name as account_name,
        currency as currency_code,
        timezone_name as time_zone,
        account_status,
        false as is_manager_account,
        true as is_current,
        created_time as valid_from,
        null::timestamp_tz as valid_to,
        _fivetran_synced as last_synced,
        row_number() over (partition by id order by _fivetran_synced desc) as rn
    from CLIENT_RARE_SEEDS_DB.META_ADS.account_history
),

facebook_ads_accounts as (
    select
        platform, account_id, account_name, currency_code, time_zone,
        account_status, is_manager_account, is_current, valid_from, valid_to, last_synced
    from facebook_ads_accounts_raw
    where rn = 1
),

combined as (
    select * from google_ads_accounts
    union all
    select * from facebook_ads_accounts
)

select
    md5(cast(coalesce(cast(platform as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(account_id as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as account_sk,
    platform,
    account_id,
    account_name,
    currency_code,
    time_zone,
    account_status,
    is_manager_account,
    is_current,
    valid_from,
    valid_to,
    last_synced
from combined
    )
;


  