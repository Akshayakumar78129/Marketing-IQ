
    
    

select
    search_term_sk as unique_field,
    count(*) as n_records

from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_search_term
where search_term_sk is not null
group by search_term_sk
having count(*) > 1


