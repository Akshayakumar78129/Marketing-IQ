{{
    config(
        materialized='incremental',
        unique_key='email_campaign_performance_sk',
        tags=['facts', 'daily', 'klaviyo', 'email']
    )
}}

/*
    Email Campaign Daily Performance Fact Table
    Grain: Campaign × Date (aggregated from events)
    Source: KLAVIYO.EVENT
*/

with campaign_events as (
    select
        date(datetime) as date_day,
        campaign_id,
        type as event_type,
        count(*) as event_count
    from {{ source('klaviyo', 'event') }}
    where campaign_id is not null
    and _fivetran_deleted = false
    {% if is_incremental() %}
    and _fivetran_synced > (select max(last_synced) from {{ this }})
    {% endif %}
    group by date(datetime), campaign_id, type
),

pivoted as (
    select
        date_day,
        campaign_id,
        sum(case when lower(event_type) like '%receive%' or lower(event_type) like '%sent%' then event_count else 0 end) as sent,
        sum(case when lower(event_type) like '%open%' then event_count else 0 end) as opens,
        sum(case when lower(event_type) like '%click%' then event_count else 0 end) as clicks,
        sum(case when lower(event_type) like '%bounce%' then event_count else 0 end) as bounces,
        sum(case when lower(event_type) like '%unsubscribe%' then event_count else 0 end) as unsubscribes,
        sum(case when lower(event_type) like '%spam%' or lower(event_type) like '%complaint%' then event_count else 0 end) as spam_complaints,
        sum(event_count) as total_events,
        max(date_day) as last_synced
    from campaign_events
    group by date_day, campaign_id
)

select
    {{ dbt_utils.generate_surrogate_key(['date_day', 'campaign_id']) }} as email_campaign_performance_sk,
    'klaviyo' as platform,
    date_day,
    campaign_id,

    -- Metrics
    sent,
    opens,
    clicks,
    bounces,
    unsubscribes,
    spam_complaints,
    total_events,

    -- Calculated rates
    case when sent > 0 then opens::float / sent else 0 end as open_rate,
    case when sent > 0 then clicks::float / sent else 0 end as click_rate,
    case when opens > 0 then clicks::float / opens else 0 end as click_to_open_rate,
    case when sent > 0 then bounces::float / sent else 0 end as bounce_rate,
    case when sent > 0 then unsubscribes::float / sent else 0 end as unsubscribe_rate,

    last_synced
from pivoted
