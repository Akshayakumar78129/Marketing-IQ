

/*
    Meta Ads Conversion Fact Table
    Contains conversion actions (purchases, add_to_cart, etc.) by ad
    Source: META_ADS.BASIC_AD_ACTIONS
*/

with ad_actions as (
    select
        ad_id::varchar as ad_id,
        date as date_day,
        action_type,
        value as action_value,
        _7_d_click as value_7d_click,
        _1_d_view as value_1d_view,
        _fivetran_synced as last_synced
    from CLIENT_RARE_SEEDS_DB.META_ADS.basic_ad_actions
    
),

pivoted as (
    select
        ad_id,
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

        -- View content
        sum(case when action_type = 'view_content' then action_value else 0 end) as view_content,

        -- Total conversions (all types)
        sum(action_value) as total_actions,

        max(last_synced) as last_synced
    from ad_actions
    group by ad_id, date_day
)

select
    md5(cast(coalesce(cast(ad_id as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(date_day as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as meta_conversion_sk,
    'meta' as platform,
    ad_id,
    date_day,

    -- Purchase funnel
    view_content,
    add_to_cart,
    initiate_checkout,
    purchases,
    purchases_7d_click,
    purchases_1d_view,

    -- Engagement
    link_clicks,
    post_engagements,
    page_engagements,
    post_reactions,

    -- Totals
    total_actions,

    -- Funnel conversion rates
    case when view_content > 0 then add_to_cart::float / view_content else 0 end as view_to_cart_rate,
    case when add_to_cart > 0 then initiate_checkout::float / add_to_cart else 0 end as cart_to_checkout_rate,
    case when initiate_checkout > 0 then purchases::float / initiate_checkout else 0 end as checkout_to_purchase_rate,

    last_synced
from pivoted