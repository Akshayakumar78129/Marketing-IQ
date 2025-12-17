{{
    config(
        materialized='incremental',
        unique_key='regional_revenue_sk',
        tags=['facts', 'klaviyo', 'revenue', 'geography']
    )
}}

/*
    Regional Revenue Fact Table
    Revenue aggregated by customer geography (country, region, city)
    Source: KLAVIYO.EVENT (Placed Order) joined with KLAVIYO.PERSON
*/

with placed_order_metric as (
    select id as metric_id
    from {{ source('klaviyo', 'metric') }}
    where lower(name) = 'placed order'
),

orders as (
    select
        e.id as event_id,
        e.person_id,
        date(e.datetime) as order_date,
        e.property_value as order_value,
        e.property_item_count as item_count,
        e._fivetran_synced as last_synced
    from {{ source('klaviyo', 'event') }} e
    inner join placed_order_metric m on e.metric_id = m.metric_id
    {% if is_incremental() %}
    where e._fivetran_synced > (select max(last_synced) from {{ this }})
    {% endif %}
),

persons as (
    select
        id as person_id,
        -- Normalize country names
        case
            when upper(country) in ('US', 'UNITED STATES', 'USA') then 'United States'
            when upper(country) in ('CA', 'CANADA') then 'Canada'
            when upper(country) in ('GB', 'UK', 'UNITED KINGDOM') then 'United Kingdom'
            when country = 'null' or country is null then 'Unknown'
            else country
        end as country,
        region,
        city,
        zip
    from {{ source('klaviyo', 'person') }}
    where _fivetran_deleted = false or _fivetran_deleted is null
),

orders_with_geo as (
    select
        o.order_date,
        coalesce(p.country, 'Unknown') as country,
        coalesce(p.region, 'Unknown') as region,
        coalesce(p.city, 'Unknown') as city,
        o.order_value,
        o.item_count,
        o.last_synced
    from orders o
    left join persons p on o.person_id = p.person_id
),

aggregated as (
    select
        order_date,
        country,
        region,
        city,
        count(*) as order_count,
        count(distinct order_date) as days_with_orders,
        sum(order_value) as total_revenue,
        avg(order_value) as avg_order_value,
        sum(item_count) as total_items,
        avg(item_count) as avg_items_per_order,
        max(last_synced) as last_synced
    from orders_with_geo
    group by order_date, country, region, city
)

select
    {{ dbt_utils.generate_surrogate_key(['order_date', 'country', 'region', 'city']) }} as regional_revenue_sk,
    'klaviyo' as platform,
    order_date,
    date_trunc('week', order_date)::date as order_week,
    date_trunc('month', order_date)::date as order_month,

    -- Geography
    country,
    region,
    city,

    -- Geography hierarchy
    country || ' > ' || region as country_region,
    country || ' > ' || region || ' > ' || city as full_location,

    -- Region classification
    case
        when country = 'United States' then 'Domestic'
        when country = 'Canada' then 'North America'
        when country in ('United Kingdom', 'Sweden', 'Switzerland', 'Ireland', 'Germany', 'France', 'Netherlands') then 'Europe'
        else 'International'
    end as region_classification,

    -- Metrics
    order_count,
    round(total_revenue, 2) as total_revenue,
    round(avg_order_value, 2) as avg_order_value,
    total_items,
    round(avg_items_per_order, 2) as avg_items_per_order,

    -- Revenue per item
    round(case when total_items > 0 then total_revenue / total_items else 0 end, 2) as revenue_per_item,

    last_synced
from aggregated
