
    
    

select
    demographics_sk as unique_field,
    count(*) as n_records

from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_demographics
where demographics_sk is not null
group by demographics_sk
having count(*) > 1


