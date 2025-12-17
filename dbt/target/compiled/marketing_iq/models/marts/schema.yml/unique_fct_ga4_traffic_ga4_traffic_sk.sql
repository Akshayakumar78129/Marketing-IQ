
    
    

select
    ga4_traffic_sk as unique_field,
    count(*) as n_records

from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_ga4_traffic
where ga4_traffic_sk is not null
group by ga4_traffic_sk
having count(*) > 1


