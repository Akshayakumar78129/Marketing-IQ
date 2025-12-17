

/*
    Image Dimension Table (Meta Ads)
    Contains image asset metadata
    Source: META_ADS.AD_IMAGE_HISTORY
*/

with images as (
    select
        id::varchar as image_id,
        hash as image_hash,
        account_id::varchar as account_id,
        name as image_name,
        status,
        url as image_url,
        url_128 as image_url_128,
        permalink_url,
        width,
        height,
        original_width,
        original_height,
        is_associated_creatives_in_adgroups,
        created_time as created_at,
        updated_time as updated_at,
        _fivetran_synced as last_synced
    from CLIENT_RARE_SEEDS_DB.META_ADS.ad_image_history
)

select
    md5(cast(coalesce(cast(image_id as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as image_sk,
    'meta' as platform,
    image_id,
    image_hash,
    account_id,
    image_name,
    status,
    image_url,
    image_url_128,
    permalink_url,

    -- Dimensions
    width,
    height,
    original_width,
    original_height,

    -- Aspect ratio category
    case
        when width = height then 'Square (1:1)'
        when width > height and (width::float / height) >= 1.7 then 'Landscape (16:9)'
        when width > height then 'Landscape (Other)'
        when height > width and (height::float / width) >= 1.7 then 'Portrait (9:16)'
        else 'Portrait (Other)'
    end as aspect_ratio_category,

    is_associated_creatives_in_adgroups,
    created_at,
    updated_at,
    last_synced
from images