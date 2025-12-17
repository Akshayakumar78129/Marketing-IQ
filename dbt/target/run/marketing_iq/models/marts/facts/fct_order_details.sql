
  
    

create or replace transient table CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_order_details
    
    
    
    as (

/*
    Order Details Fact Table
    Transaction-level order data with value distribution metrics
    Source: KLAVIYO.EVENT (Placed Order metric)
*/

with placed_order_metric as (
    select id as metric_id
    from CLIENT_RARE_SEEDS_DB.KLAVIYO.metric
    where lower(name) = 'placed order'
),

orders as (
    select
        e.id as event_id,
        e.uuid as order_uuid,
        e.person_id,
        e.campaign_id,
        e.flow_id,
        e.flow_message_id,
        e.datetime as order_datetime,
        date(e.datetime) as order_date,

        -- Order value metrics
        e.property_value as order_value,
        e.property_item_count as item_count,
        e.property_discounted as is_discounted,
        e.property_order_currency_code as currency_code,

        -- Product info
        e.property_product_names as product_names,
        e.property_product_categories as product_categories,

        -- Attribution
        e.property_utm_source as utm_source,
        e.property_utm_medium as utm_medium,
        e.property_utm_campaign as utm_campaign,

        e._fivetran_synced as last_synced
    from CLIENT_RARE_SEEDS_DB.KLAVIYO.event e
    inner join placed_order_metric m on e.metric_id = m.metric_id
    
)

select
    md5(cast(coalesce(cast(event_id as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as order_sk,
    'klaviyo' as platform,
    event_id,
    order_uuid,
    person_id,
    campaign_id,
    flow_id,
    flow_message_id,
    order_datetime,
    order_date,

    -- Time dimensions
    date_trunc('week', order_date)::date as order_week,
    date_trunc('month', order_date)::date as order_month,
    extract(hour from order_datetime) as order_hour,
    extract(dayofweek from order_datetime) as order_day_of_week,

    -- Order value
    order_value,
    item_count,
    coalesce(is_discounted, false) as is_discounted,
    coalesce(currency_code, 'USD') as currency_code,

    -- Order value segments
    case
        when order_value >= 200 then 'High Value ($200+)'
        when order_value >= 100 then 'Medium-High ($100-199)'
        when order_value >= 50 then 'Medium ($50-99)'
        when order_value >= 25 then 'Low-Medium ($25-49)'
        else 'Low (<$25)'
    end as order_value_segment,

    -- Item count segments
    case
        when item_count >= 10 then '10+ items'
        when item_count >= 5 then '5-9 items'
        when item_count >= 3 then '3-4 items'
        when item_count = 2 then '2 items'
        else '1 item'
    end as item_count_segment,

    -- Average item value
    case when item_count > 0 then order_value / item_count else order_value end as avg_item_value,

    -- Attribution
    case
        when campaign_id is not null then 'Campaign'
        when flow_id is not null then 'Flow'
        when utm_source is not null then 'UTM Tracked'
        else 'Direct/Unattributed'
    end as attribution_type,

    utm_source,
    utm_medium,
    utm_campaign,

    -- Product info (as arrays)
    product_names,
    product_categories,

    last_synced
from orders
    )
;


  