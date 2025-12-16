{{
    config(
        materialized='incremental',
        unique_key='klaviyo_revenue_sk',
        tags=['facts', 'klaviyo', 'revenue']
    )
}}

/*
    Klaviyo Revenue Fact Table
    Revenue from 'Placed Order' events attributed to campaigns/flows
    Source: KLAVIYO.EVENT filtered for Placed Order metric
*/

with placed_order_metrics as (
    -- Get the metric IDs for 'Placed Order' events
    select id as metric_id
    from {{ source('klaviyo', 'metric') }}
    where lower(name) = 'placed order'
),

order_events as (
    select
        e.id as event_id,
        e.person_id,
        e.campaign_id,
        e.flow_id,
        e.flow_message_id,
        e.datetime as event_datetime,
        date(e.datetime) as date_day,
        e.property_value as revenue,
        e.property_item_count as item_count,
        e.property_attribution as attribution,
        e._fivetran_synced as last_synced
    from {{ source('klaviyo', 'event') }} e
    inner join placed_order_metrics m on e.metric_id = m.metric_id
    {% if is_incremental() %}
    where e._fivetran_synced > (select max(last_synced) from {{ this }})
    {% endif %}
),

aggregated as (
    select
        date_day,
        person_id,
        campaign_id,
        flow_id,
        count(*) as order_count,
        sum(revenue) as total_revenue,
        sum(item_count) as total_items,
        avg(revenue) as avg_order_value,
        max(last_synced) as last_synced
    from order_events
    group by date_day, person_id, campaign_id, flow_id
)

select
    {{ dbt_utils.generate_surrogate_key(['date_day', 'person_id', 'campaign_id', 'flow_id']) }} as klaviyo_revenue_sk,
    'klaviyo' as platform,
    date_day,
    person_id,
    campaign_id,
    flow_id,

    -- Attribution type
    case
        when campaign_id is not null then 'campaign'
        when flow_id is not null then 'flow'
        else 'unattributed'
    end as attribution_type,

    -- Metrics
    order_count,
    total_revenue,
    total_items,
    avg_order_value,

    last_synced
from aggregated
