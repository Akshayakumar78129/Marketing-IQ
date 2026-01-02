{{
    config(
        materialized='incremental',
        unique_key='meta_campaign_conversion_sk',
        tags=['facts', 'meta', 'conversions']
    )
}}

/*
    Meta Ads Campaign-Level Conversion Fact Table
    Contains conversion actions (purchases, add_to_cart, etc.) by campaign
    Source: META_ADS.BASIC_CAMPAIGN_ACTIONS

    NOTE: This table has FULL HISTORICAL DATA (2.8+ years) unlike ad-level
    conversions which are limited to ~30 days by Meta's API.
*/

with campaign_actions as (
    select
        campaign_id::varchar as campaign_id,
        date as date_day,
        action_type,
        value as action_value,
        _7_d_click as value_7d_click,
        _1_d_view as value_1d_view,
        _fivetran_synced as last_synced
    from {{ source('meta_ads', 'basic_campaign_actions') }}
    {% if is_incremental() %}
    where _fivetran_synced > (select max(last_synced) from {{ this }})
    {% endif %}
),

pivoted as (
    select
        campaign_id,
        date_day,

        -- Purchase metrics
        sum(case when action_type = 'purchase' then action_value else 0 end) as purchases,
        sum(case when action_type = 'purchase' then value_7d_click else 0 end) as purchases_7d_click,
        sum(case when action_type = 'purchase' then value_1d_view else 0 end) as purchases_1d_view,

        -- Add to cart metrics
        sum(case when action_type = 'add_to_cart' then action_value else 0 end) as add_to_cart,

        -- Initiate checkout metrics
        sum(case when action_type = 'initiate_checkout' then action_value else 0 end) as initiate_checkout,

        -- Engagement metrics
        sum(case when action_type = 'link_click' then action_value else 0 end) as link_clicks,
        sum(case when action_type = 'post_engagement' then action_value else 0 end) as post_engagements,
        sum(case when action_type = 'page_engagement' then action_value else 0 end) as page_engagements,
        sum(case when action_type = 'post_reaction' then action_value else 0 end) as post_reactions,
        sum(case when action_type = 'comment' then action_value else 0 end) as comments,
        sum(case when action_type = 'like' then action_value else 0 end) as likes,
        sum(case when action_type = 'share' then action_value else 0 end) as shares,

        -- View content
        sum(case when action_type = 'view_content' then action_value else 0 end) as view_content,

        -- Lead generation
        sum(case when action_type = 'lead' then action_value else 0 end) as leads,
        sum(case when action_type = 'complete_registration' then action_value else 0 end) as registrations,

        -- Video metrics
        sum(case when action_type = 'video_view' then action_value else 0 end) as video_views,
        sum(case when action_type = 'video_p25_watched' then action_value else 0 end) as video_25_watched,
        sum(case when action_type = 'video_p50_watched' then action_value else 0 end) as video_50_watched,
        sum(case when action_type = 'video_p75_watched' then action_value else 0 end) as video_75_watched,
        sum(case when action_type = 'video_p100_watched' then action_value else 0 end) as video_100_watched,

        -- Total conversions (all types)
        sum(action_value) as total_actions,

        max(last_synced) as last_synced
    from campaign_actions
    group by campaign_id, date_day
)

select
    {{ dbt_utils.generate_surrogate_key(['campaign_id', 'date_day']) }} as meta_campaign_conversion_sk,
    'meta' as platform,
    campaign_id,
    date_day,

    -- Purchase funnel
    view_content,
    add_to_cart,
    initiate_checkout,
    purchases,
    purchases_7d_click,
    purchases_1d_view,

    -- Lead generation
    leads,
    registrations,

    -- Engagement
    link_clicks,
    post_engagements,
    page_engagements,
    post_reactions,
    comments,
    likes,
    shares,

    -- Video engagement
    video_views,
    video_25_watched,
    video_50_watched,
    video_75_watched,
    video_100_watched,

    -- Totals
    total_actions,

    -- Funnel conversion rates
    case when view_content > 0 then add_to_cart::float / view_content else 0 end as view_to_cart_rate,
    case when add_to_cart > 0 then initiate_checkout::float / add_to_cart else 0 end as cart_to_checkout_rate,
    case when initiate_checkout > 0 then purchases::float / initiate_checkout else 0 end as checkout_to_purchase_rate,

    -- Video completion rates
    case when video_views > 0 then video_25_watched::float / video_views else 0 end as video_25_completion_rate,
    case when video_views > 0 then video_50_watched::float / video_views else 0 end as video_50_completion_rate,
    case when video_views > 0 then video_75_watched::float / video_views else 0 end as video_75_completion_rate,
    case when video_views > 0 then video_100_watched::float / video_views else 0 end as video_100_completion_rate,

    last_synced
from pivoted
