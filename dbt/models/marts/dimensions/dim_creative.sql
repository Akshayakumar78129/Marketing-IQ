{{
    config(
        materialized='table',
        tags=['dimensions', 'meta']
    )
}}

/*
    Creative Dimension Table (Meta Ads)
    Contains creative assets: headlines, body copy, CTA, images, videos
    Source: META_ADS.CREATIVE_HISTORY
*/

with creatives as (
    select
        id::varchar as creative_id,
        account_id::varchar as account_id,
        name as creative_name,
        title as headline,
        body as body_copy,
        call_to_action_type,
        object_type as creative_type,
        status,
        image_hash,
        image_url,
        video_id::varchar as video_id,
        thumbnail_url,
        link_url,
        link_destination_display_url,
        instagram_permalink_url,
        instagram_user_id,
        object_story_id,
        enable_direct_install,
        _fivetran_synced as last_synced,
        row_number() over (partition by id order by _fivetran_synced desc) as rn
    from {{ source('meta_ads', 'creative_history') }}
)

select
    {{ dbt_utils.generate_surrogate_key(['creative_id']) }} as creative_sk,
    'meta' as platform,
    creative_id,
    account_id,
    creative_name,
    headline,
    body_copy,
    call_to_action_type,
    creative_type,
    status,

    -- Media assets
    image_hash,
    image_url,
    video_id,
    thumbnail_url,

    -- Destination
    link_url,
    link_destination_display_url,

    -- Instagram
    instagram_permalink_url,
    instagram_user_id,

    -- Other
    object_story_id,
    enable_direct_install,

    -- Flags
    case when image_url is not null or image_hash is not null then true else false end as has_image,
    case when video_id is not null then true else false end as has_video,

    last_synced
from creatives
where rn = 1
