
    
    

select
    keyword_competitive_sk as unique_field,
    count(*) as n_records

from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_keyword_competitive
where keyword_competitive_sk is not null
group by keyword_competitive_sk
having count(*) > 1


