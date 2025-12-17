
    
    

select
    budget_utilization_sk as unique_field,
    count(*) as n_records

from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_budget_utilization
where budget_utilization_sk is not null
group by budget_utilization_sk
having count(*) > 1


