

/*
    Audience dimension table
    Combines Google Ads User Lists and Klaviyo Segments
    Source: GOOGLE_ADS.USER_LIST, KLAVIYO.SEGMENT
*/

with google_ads_audiences as (
    select
        'google_ads' as platform,
        id::varchar as audience_id,
        name as audience_name,
        description,
        type as audience_type,
        membership_status,
        size_for_search as audience_size_search,
        size_for_display as audience_size_display,
        size_range_for_search,
        size_range_for_display,
        eligible_for_search,
        eligible_for_display,
        null::timestamp_tz as created_at,
        _fivetran_synced as last_synced
    from CLIENT_RARE_SEEDS_DB.GOOGLE_ADS.user_list
),

klaviyo_audiences as (
    select
        'klaviyo' as platform,
        id::varchar as audience_id,
        name as audience_name,
        null as description,
        'SEGMENT' as audience_type,
        null as membership_status,
        null as audience_size_search,
        null as audience_size_display,
        null as size_range_for_search,
        null as size_range_for_display,
        null as eligible_for_search,
        null as eligible_for_display,
        created as created_at,
        _fivetran_synced as last_synced
    from CLIENT_RARE_SEEDS_DB.KLAVIYO.segment
    where _fivetran_deleted = false
),

combined as (
    select * from google_ads_audiences
    union all
    select * from klaviyo_audiences
)

select
    md5(cast(coalesce(cast(platform as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(audience_id as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as audience_sk,
    platform,
    audience_id,
    audience_name,
    description,
    audience_type,
    membership_status,
    audience_size_search,
    audience_size_display,
    size_range_for_search,
    size_range_for_display,
    eligible_for_search,
    eligible_for_display,
    created_at,
    last_synced
from combined