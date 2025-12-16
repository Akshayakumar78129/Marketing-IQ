{{
    config(
        materialized='table',
        tags=['dimensions']
    )
}}

/*
    Conversion Action dimension table
    Source: GA4.CONVERSION_EVENTS, GA4.CONVERSIONS_REPORT
*/

with ga4_conversion_events_raw as (
    select
        event_name,
        name as conversion_name,
        custom,
        deletable,
        create_time as created_at,
        row_number() over (partition by event_name order by create_time desc nulls last) as rn
    from {{ source('ga4', 'conversion_events') }}
),

ga4_conversion_events as (
    select
        event_name,
        conversion_name,
        custom,
        deletable,
        created_at
    from ga4_conversion_events_raw
    where rn = 1
),

ga4_conversions as (
    select distinct
        event_name
    from {{ source('ga4', 'conversions_report') }}
    where event_name is not null
),

all_conversions as (
    select
        ce.event_name,
        ce.conversion_name,
        ce.custom as is_custom,
        ce.created_at
    from ga4_conversion_events ce
    union
    select
        c.event_name,
        c.event_name as conversion_name,
        null as is_custom,
        null as created_at
    from ga4_conversions c
    where not exists (
        select 1 from ga4_conversion_events ce
        where ce.event_name = c.event_name
    )
)

select
    {{ dbt_utils.generate_surrogate_key(['event_name']) }} as conversion_action_sk,
    'ga4' as platform,
    event_name as conversion_action_id,
    coalesce(conversion_name, event_name) as conversion_action_name,
    is_custom,
    case
        when lower(event_name) like '%purchase%' then 'Purchase'
        when lower(event_name) like '%lead%' then 'Lead'
        when lower(event_name) like '%signup%' or lower(event_name) like '%sign_up%' then 'Sign Up'
        when lower(event_name) like '%add_to_cart%' then 'Add to Cart'
        when lower(event_name) like '%checkout%' then 'Checkout'
        when lower(event_name) like '%page_view%' then 'Page View'
        else 'Other'
    end as conversion_category,
    created_at
from all_conversions
