
  
    

create or replace transient table CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.dim_keyword
    
    
    
    as (

/*
    Keyword dimension table (SCD Type 2)
    Source: GOOGLE_ADS.AD_GROUP_CRITERION_HISTORY
*/

with keywords as (
    select
        id::varchar as keyword_id,
        ad_group_id::varchar as ad_group_id,
        keyword_text,
        keyword_match_type as match_type,
        status,
        negative as is_negative,
        quality_info_score as quality_score,
        quality_info_creative_score as creative_quality,
        quality_info_post_click_score as post_click_quality,
        quality_info_search_predicted_ctr as expected_ctr,
        cpc_bid_micros / 1000000.0 as cpc_bid,
        first_page_cpc_micros / 1000000.0 as first_page_cpc,
        first_position_cpc_micros / 1000000.0 as first_position_cpc,
        top_of_page_cpc_micros / 1000000.0 as top_of_page_cpc,
        final_urls,
        _fivetran_active as is_current,
        _fivetran_start as valid_from,
        _fivetran_end as valid_to,
        _fivetran_synced as last_synced
    from CLIENT_RARE_SEEDS_DB.GOOGLE_ADS.ad_group_criterion_history
    where type = 'KEYWORD'
    and _fivetran_active = true
)

select
    md5(cast(coalesce(cast(keyword_id as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(ad_group_id as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as keyword_sk,
    'google_ads' as platform,
    keyword_id,
    ad_group_id,
    keyword_text,
    match_type,
    status,
    is_negative,
    quality_score,
    creative_quality,
    post_click_quality,
    expected_ctr,
    cpc_bid,
    first_page_cpc,
    first_position_cpc,
    top_of_page_cpc,
    final_urls,
    is_current,
    valid_from,
    valid_to,
    last_synced
from keywords
    )
;


  