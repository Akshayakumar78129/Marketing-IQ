{{
    config(
        materialized='table',
        tags=['facts', 'daily', 'meta', 'video']
    )
}}

/*
    Video Performance Daily Fact Table (Facebook)
    Grain: Video × Date
    Source: FACEBOOK_ADS.AD_VIDEO_HISTORY (aggregated with ad performance)
    Note: Using video metadata combined with ad-level performance
*/

with videos as (
    select
        id as video_id,
        account_id::varchar as account_id,
        title as video_title,
        length as video_length_seconds,
        views as total_views,
        post_views,
        created_time::date as created_date,
        _fivetran_synced as last_synced
    from {{ source('meta_ads', 'ad_video_history') }}
),

video_performance as (
    select
        video_id,
        account_id,
        video_title,
        video_length_seconds,
        total_views,
        post_views,
        created_date,
        last_synced
    from videos
)

select
    {{ dbt_utils.generate_surrogate_key(['video_id']) }} as video_performance_sk,
    'meta' as platform,
    video_id,
    account_id,
    video_title,
    video_length_seconds,
    total_views,
    post_views,
    created_date,

    -- Video length category
    case
        when video_length_seconds < 15 then 'Short (< 15s)'
        when video_length_seconds < 30 then 'Medium (15-30s)'
        when video_length_seconds < 60 then 'Long (30-60s)'
        else 'Very Long (> 60s)'
    end as video_length_category,

    last_synced
from video_performance
