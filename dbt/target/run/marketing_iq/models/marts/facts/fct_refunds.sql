
  
    

create or replace transient table CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_refunds
    
    
    
    as (

/*
    Refunds Fact Table
    Tracks refunded and cancelled orders
    Source: KLAVIYO.EVENT (Refunded Order, Cancelled Order metrics)
*/

with refund_metrics as (
    select
        id as metric_id,
        name as metric_name,
        case
            when lower(name) = 'refunded order' then 'refund'
            when lower(name) = 'cancelled order' then 'cancellation'
        end as event_type
    from CLIENT_RARE_SEEDS_DB.KLAVIYO.metric
    where lower(name) in ('refunded order', 'cancelled order')
),

refund_events as (
    select
        e.id as event_id,
        e.uuid as event_uuid,
        e.person_id,
        e.datetime as event_datetime,
        date(e.datetime) as event_date,
        m.event_type,
        m.metric_name,

        -- Value metrics
        e.property_value as refund_value,
        e.property_item_count as item_count,

        -- Product info
        e.property_product_names as product_names,

        e._fivetran_synced as last_synced
    from CLIENT_RARE_SEEDS_DB.KLAVIYO.event e
    inner join refund_metrics m on e.metric_id = m.metric_id
    
)

select
    md5(cast(coalesce(cast(event_id as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as refund_sk,
    'klaviyo' as platform,
    event_id,
    event_uuid,
    person_id,
    event_datetime,
    event_date,
    date_trunc('week', event_date)::date as event_week,
    date_trunc('month', event_date)::date as event_month,

    -- Event classification
    event_type,
    metric_name as event_name,

    -- Value metrics
    coalesce(refund_value, 0) as refund_value,
    coalesce(item_count, 0) as item_count,

    -- Refund value segments
    case
        when refund_value >= 200 then 'High Value ($200+)'
        when refund_value >= 100 then 'Medium-High ($100-199)'
        when refund_value >= 50 then 'Medium ($50-99)'
        when refund_value >= 25 then 'Low-Medium ($25-49)'
        else 'Low (<$25)'
    end as refund_value_segment,

    -- Product info
    product_names,

    last_synced
from refund_events
    )
;


  