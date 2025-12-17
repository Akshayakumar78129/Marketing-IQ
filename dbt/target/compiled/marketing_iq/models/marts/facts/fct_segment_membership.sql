

/*
    Segment Membership Fact Table
    Grain: Segment × Person
    Source: KLAVIYO.SEGMENT_PERSON
*/

with segment_members as (
    select
        segment_id,
        person_id,
        _fivetran_synced as membership_timestamp,
        _fivetran_deleted as is_deleted
    from CLIENT_RARE_SEEDS_DB.KLAVIYO.segment_person
    
    where _fivetran_synced > (select max(membership_timestamp) from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_segment_membership)
    
)

select
    md5(cast(coalesce(cast(segment_id as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(person_id as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as segment_membership_sk,
    'klaviyo' as platform,
    segment_id,
    person_id,
    case when is_deleted then false else true end as is_active_member,
    membership_timestamp,
    date(membership_timestamp) as membership_date
from segment_members