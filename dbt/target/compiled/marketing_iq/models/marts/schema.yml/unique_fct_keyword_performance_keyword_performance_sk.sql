
    
    

select
    keyword_performance_sk as unique_field,
    count(*) as n_records

from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_keyword_performance
where keyword_performance_sk is not null
group by keyword_performance_sk
having count(*) > 1


