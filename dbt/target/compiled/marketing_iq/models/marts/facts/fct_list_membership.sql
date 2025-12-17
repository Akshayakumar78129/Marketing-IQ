

/*
    List Membership Fact Table
    Grain: List × Person
    Source: KLAVIYO.LIST_PERSON
*/

with list_members as (
    select
        list_id,
        person_id,
        joined_group_at,
        _fivetran_synced as last_synced,
        _fivetran_deleted as is_deleted
    from CLIENT_RARE_SEEDS_DB.KLAVIYO.list_person
    
    where _fivetran_synced > (select max(last_synced) from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_list_membership)
    
)

select
    md5(cast(coalesce(cast(list_id as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(person_id as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as list_membership_sk,
    'klaviyo' as platform,
    list_id,
    person_id,
    joined_group_at as joined_at,
    date(joined_group_at) as joined_date,
    case when is_deleted then false else true end as is_active_member,
    last_synced
from list_members