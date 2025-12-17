

/*
    Ad Group Settings History Fact Table
    Grain: Ad Group × Change Date
    Source: GOOGLE_ADS.AD_GROUP_HISTORY
    Tracks all changes to ad group settings over time (SCD Type 2)
*/

with ad_group_changes as (
    select
        id::varchar as ad_group_id,
        campaign_id::varchar as campaign_id,
        base_ad_group_id::varchar as base_ad_group_id,
        name as ad_group_name,
        status as ad_group_status,
        type as ad_group_type,
        ad_rotation_mode,
        _fivetran_start as valid_from,
        _fivetran_end as valid_to,
        _fivetran_active as is_current,
        _fivetran_synced as last_synced
    from CLIENT_RARE_SEEDS_DB.GOOGLE_ADS.ad_group_history
    
    where _fivetran_synced > (select max(last_synced) from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_ad_group_settings_history)
    
)

select
    md5(cast(coalesce(cast(ad_group_id as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(valid_from as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as ad_group_settings_sk,
    'google_ads' as platform,
    ad_group_id,
    campaign_id,
    base_ad_group_id,
    ad_group_name,
    ad_group_status,
    ad_group_type,
    ad_rotation_mode,
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
from ad_group_changes