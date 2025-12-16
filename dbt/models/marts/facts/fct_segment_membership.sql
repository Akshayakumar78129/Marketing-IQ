{{
    config(
        materialized='incremental',
        unique_key='segment_membership_sk',
        tags=['facts', 'klaviyo']
    )
}}

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
    from {{ source('klaviyo', 'segment_person') }}
    {% if is_incremental() %}
    where _fivetran_synced > (select max(membership_timestamp) from {{ this }})
    {% endif %}
)

select
    {{ dbt_utils.generate_surrogate_key(['segment_id', 'person_id']) }} as segment_membership_sk,
    'klaviyo' as platform,
    segment_id,
    person_id,
    case when is_deleted then false else true end as is_active_member,
    membership_timestamp,
    date(membership_timestamp) as membership_date
from segment_members
