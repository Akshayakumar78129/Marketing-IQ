

/*
    Ecommerce Item Daily Fact Table
    Grain: Item × Date
    Source: GA4.ECOMMERCE_PURCHASES_ITEM_NAME_REPORT
*/

with ecommerce_data as (
    select
        date as date_day,
        property,
        item_name,
        items_viewed,
        items_added_to_cart,
        items_purchased,
        item_revenue as revenue,
        cart_to_view_rate,
        purchase_to_view_rate,
        _fivetran_synced as last_synced
    from CLIENT_RARE_SEEDS_DB.GA4.ecommerce_purchases_item_name_report
    
    where _fivetran_synced > (select max(last_synced) from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_ecommerce_item)
    
)

select
    md5(cast(coalesce(cast(date_day as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(property as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(item_name as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as ecommerce_item_sk,
    'ga4' as platform,
    date_day,
    property,
    item_name,

    -- Metrics
    items_viewed,
    items_added_to_cart,
    items_purchased,
    revenue,

    -- Funnel rates
    cart_to_view_rate,
    purchase_to_view_rate,

    -- Calculated metrics
    case when items_viewed > 0 then items_added_to_cart::float / items_viewed else 0 end as calculated_cart_rate,
    case when items_added_to_cart > 0 then items_purchased::float / items_added_to_cart else 0 end as cart_to_purchase_rate,
    case when items_purchased > 0 then revenue / items_purchased else 0 end as avg_item_revenue,

    last_synced
from ecommerce_data