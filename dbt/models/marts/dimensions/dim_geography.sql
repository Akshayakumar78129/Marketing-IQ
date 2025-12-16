{{
    config(
        materialized='table',
        tags=['dimensions']
    )
}}

/*
    Geography dimension table
    Source: GA4 demographic reports
*/

with countries as (
    select distinct
        country,
        null as region,
        null as city
    from {{ source('ga4', 'demographic_country_report') }}
    where country is not null
),

regions as (
    select distinct
        null as country,
        region,
        null as city
    from {{ source('ga4', 'demographic_region_report') }}
    where region is not null
),

cities as (
    select distinct
        null as country,
        null as region,
        city
    from {{ source('ga4', 'demographic_city_report') }}
    where city is not null
),

combined as (
    select country, region, city from countries
    union all
    select country, region, city from regions
    union all
    select country, region, city from cities
)

select
    {{ dbt_utils.generate_surrogate_key(['country', 'region', 'city']) }} as geography_sk,
    country,
    region,
    city,
    coalesce(country, region, city) as location_name,
    case
        when city is not null then 'city'
        when region is not null then 'region'
        when country is not null then 'country'
        else 'unknown'
    end as geo_level
from combined
where coalesce(country, region, city) is not null
