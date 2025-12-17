
    
    

select
    performance_sk as unique_field,
    count(*) as n_records

from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_campaign_performance
where performance_sk is not null
group by performance_sk
having count(*) > 1


