

/*
    List dimension table (Klaviyo)
    Source: KLAVIYO.LIST
*/

with lists as (
    select
        id as list_id,
        list_name,
        created as created_at,
        updated as updated_at,
        _fivetran_deleted as is_deleted,
        _fivetran_synced as last_synced
    from CLIENT_RARE_SEEDS_DB.KLAVIYO.list
    where _fivetran_deleted = false
),

list_counts as (
    select
        list_id,
        count(distinct person_id) as member_count
    from CLIENT_RARE_SEEDS_DB.KLAVIYO.list_person
    where _fivetran_deleted = false
    group by list_id
)

select
    md5(cast(coalesce(cast(l.list_id as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as list_sk,
    'klaviyo' as platform,
    l.list_id,
    l.list_name,
    coalesce(lc.member_count, 0) as member_count,
    l.created_at,
    l.updated_at,
    l.last_synced
from lists l
left join list_counts lc on l.list_id = lc.list_id