{{
    config(
        materialized='incremental',
        unique_key='list_membership_sk',
        tags=['facts', 'klaviyo']
    )
}}

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
    from {{ source('klaviyo', 'list_person') }}
    {% if is_incremental() %}
    where _fivetran_synced > (select max(last_synced) from {{ this }})
    {% endif %}
)

select
    {{ dbt_utils.generate_surrogate_key(['list_id', 'person_id']) }} as list_membership_sk,
    'klaviyo' as platform,
    list_id,
    person_id,
    joined_group_at as joined_at,
    date(joined_group_at) as joined_date,
    case when is_deleted then false else true end as is_active_member,
    last_synced
from list_members
