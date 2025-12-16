{{
    config(
        materialized='table',
        tags=['dimensions']
    )
}}

/*
    Google Ads Ad Group dimension table (SCD Type 2)
    Source: GOOGLE_ADS.AD_GROUP_HISTORY
*/

with ad_groups as (
    select
        id::varchar as ad_group_id,
        campaign_id::varchar as campaign_id,
        name as ad_group_name,
        status,
        type as ad_group_type,
        ad_rotation_mode,
        _fivetran_active as is_current,
        _fivetran_start as valid_from,
        _fivetran_end as valid_to,
        _fivetran_synced as last_synced
    from {{ source('google_ads', 'ad_group_history') }}
    where _fivetran_active = true
)

select
    {{ dbt_utils.generate_surrogate_key(['ad_group_id']) }} as ad_group_sk,
    'google_ads' as platform,
    ad_group_id,
    campaign_id,
    ad_group_name,
    status,
    ad_group_type,
    ad_rotation_mode,
    is_current,
    valid_from,
    valid_to,
    last_synced
from ad_groups
