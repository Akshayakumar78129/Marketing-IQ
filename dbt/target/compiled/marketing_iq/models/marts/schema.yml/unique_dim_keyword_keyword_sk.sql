
    
    

select
    keyword_sk as unique_field,
    count(*) as n_records

from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.dim_keyword
where keyword_sk is not null
group by keyword_sk
having count(*) > 1


