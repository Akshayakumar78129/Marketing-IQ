{{
    config(
        materialized='table',
        tags=['dimensions']
    )
}}

/*
    Segment dimension table (Klaviyo)
    Source: KLAVIYO.SEGMENT
*/

with segments as (
    select
        id as segment_id,
        name as segment_name,
        definition,
        created as created_at,
        updated as updated_at,
        _fivetran_deleted as is_deleted,
        _fivetran_synced as last_synced
    from {{ source('klaviyo', 'segment') }}
    where _fivetran_deleted = false
),

segment_counts as (
    select
        segment_id,
        count(distinct person_id) as member_count
    from {{ source('klaviyo', 'segment_person') }}
    where _fivetran_deleted = false
    group by segment_id
)

select
    {{ dbt_utils.generate_surrogate_key(['s.segment_id']) }} as segment_sk,
    'klaviyo' as platform,
    s.segment_id,
    s.segment_name,
    s.definition,
    coalesce(sc.member_count, 0) as member_count,
    s.created_at,
    s.updated_at,
    s.last_synced
from segments s
left join segment_counts sc on s.segment_id = sc.segment_id
