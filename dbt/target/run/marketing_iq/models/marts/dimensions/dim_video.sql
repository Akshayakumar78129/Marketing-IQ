
  
    

create or replace transient table CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.dim_video
    
    
    
    as (

/*
    Video dimension table (Facebook Ads)
    Source: FACEBOOK_ADS.AD_VIDEO_HISTORY
*/

with videos as (
    select
        id as video_id,
        account_id::varchar as account_id,
        title as video_title,
        description,
        length as video_length_seconds,
        views as total_views,
        post_views,
        source as video_source,
        permalink_url,
        picture,
        embeddable as is_embeddable,
        published as is_published,
        is_crosspost_video,
        is_crossposting_eligible,
        is_instagram_eligible,
        live_status,
        content_category,
        status_value as processing_status,
        created_time as created_at,
        updated_time as updated_at,
        _fivetran_synced as last_synced
    from CLIENT_RARE_SEEDS_DB.META_ADS.ad_video_history
)

select
    md5(cast(coalesce(cast(video_id as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as video_sk,
    'meta' as platform,
    video_id,
    account_id,
    video_title,
    description,
    video_length_seconds,
    case
        when video_length_seconds < 15 then 'Short (< 15s)'
        when video_length_seconds < 30 then 'Medium (15-30s)'
        when video_length_seconds < 60 then 'Long (30-60s)'
        else 'Very Long (> 60s)'
    end as video_length_category,
    total_views,
    post_views,
    video_source,
    permalink_url,
    is_embeddable,
    is_published,
    is_crosspost_video,
    is_crossposting_eligible,
    is_instagram_eligible,
    live_status,
    content_category,
    processing_status,
    created_at,
    updated_at,
    last_synced
from videos
    )
;


  