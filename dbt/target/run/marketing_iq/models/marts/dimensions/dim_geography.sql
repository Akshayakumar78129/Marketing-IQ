
  
    

create or replace transient table CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.dim_geography
    
    
    
    as (

/*
    Geography dimension table
    Source: GA4 demographic reports
*/

with countries as (
    select distinct
        country,
        null as region,
        null as city
    from CLIENT_RARE_SEEDS_DB.GA4.demographic_country_report
    where country is not null
),

regions as (
    select distinct
        null as country,
        region,
        null as city
    from CLIENT_RARE_SEEDS_DB.GA4.demographic_region_report
    where region is not null
),

cities as (
    select distinct
        null as country,
        null as region,
        city
    from CLIENT_RARE_SEEDS_DB.GA4.demographic_city_report
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
    md5(cast(coalesce(cast(country as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(region as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(city as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as geography_sk,
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
    )
;


  