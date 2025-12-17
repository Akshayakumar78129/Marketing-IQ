
    
    

select
    ga4_geo_sk as unique_field,
    count(*) as n_records

from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_ga4_geo
where ga4_geo_sk is not null
group by ga4_geo_sk
having count(*) > 1


