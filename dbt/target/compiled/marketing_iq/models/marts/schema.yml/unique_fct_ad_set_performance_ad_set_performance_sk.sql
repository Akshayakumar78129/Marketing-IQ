
    
    

select
    ad_set_performance_sk as unique_field,
    count(*) as n_records

from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_ad_set_performance
where ad_set_performance_sk is not null
group by ad_set_performance_sk
having count(*) > 1


