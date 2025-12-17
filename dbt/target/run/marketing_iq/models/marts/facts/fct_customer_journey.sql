
  
    

create or replace transient table CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_customer_journey
    
    
    
    as (

/*
    Customer Journey Fact Table
    Key funnel events: Viewed Product -> Added to Cart -> Started Checkout -> Placed Order -> Fulfilled
    Source: KLAVIYO.EVENT
*/

with journey_metrics as (
    select
        id as metric_id,
        name as metric_name,
        case
            when lower(name) = 'viewed product' then 1
            when lower(name) = 'added to cart' then 2
            when lower(name) = 'started checkout' then 3
            when lower(name) = 'placed order' then 4
            when lower(name) = 'fulfilled order' then 5
            when lower(name) = 'refunded order' then 6
        end as funnel_stage_order,
        case
            when lower(name) = 'viewed product' then 'awareness'
            when lower(name) = 'added to cart' then 'consideration'
            when lower(name) = 'started checkout' then 'intent'
            when lower(name) = 'placed order' then 'purchase'
            when lower(name) = 'fulfilled order' then 'fulfillment'
            when lower(name) = 'refunded order' then 'refund'
        end as funnel_stage
    from CLIENT_RARE_SEEDS_DB.KLAVIYO.metric
    where lower(name) in (
        'viewed product',
        'added to cart',
        'started checkout',
        'placed order',
        'fulfilled order',
        'refunded order'
    )
),

journey_events as (
    select
        e.id as event_id,
        e.person_id,
        e.campaign_id,
        e.flow_id,
        e.datetime as event_datetime,
        date(e.datetime) as event_date,
        m.metric_name as event_name,
        m.funnel_stage,
        m.funnel_stage_order,

        -- Value metrics (for orders)
        e.property_value as event_value,
        e.property_item_count as item_count,

        -- Product info
        e.property_product_id as product_id,
        e.property_name as product_name,
        e.property_sku as product_sku,
        e.property_price as product_price,
        e.property_quantity as quantity,

        -- Attribution
        e.property_utm_source as utm_source,
        e.property_utm_medium as utm_medium,
        e.property_utm_campaign as utm_campaign,

        e._fivetran_synced as last_synced
    from CLIENT_RARE_SEEDS_DB.KLAVIYO.event e
    inner join journey_metrics m on e.metric_id = m.metric_id
    
)

select
    md5(cast(coalesce(cast(event_id as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as journey_event_sk,
    'klaviyo' as platform,
    event_id,
    person_id,
    campaign_id,
    flow_id,
    event_datetime,
    event_date,
    date_trunc('week', event_date)::date as event_week,
    date_trunc('month', event_date)::date as event_month,
    extract(hour from event_datetime) as event_hour,

    -- Funnel info
    event_name,
    funnel_stage,
    funnel_stage_order,

    -- Is this a conversion event?
    case when funnel_stage in ('purchase', 'fulfillment') then true else false end as is_conversion,

    -- Value metrics
    coalesce(event_value, 0) as event_value,
    coalesce(item_count, 0) as item_count,

    -- Product info
    product_id,
    product_name,
    product_sku,
    product_price,
    quantity,

    -- Attribution
    case
        when campaign_id is not null then 'Campaign'
        when flow_id is not null then 'Flow'
        when utm_source is not null then 'UTM Tracked'
        else 'Direct/Organic'
    end as attribution_type,

    utm_source,
    utm_medium,
    utm_campaign,

    last_synced
from journey_events
    )
;


  