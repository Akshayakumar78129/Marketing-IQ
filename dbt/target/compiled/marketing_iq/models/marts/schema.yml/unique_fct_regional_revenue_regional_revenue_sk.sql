
    
    

select
    regional_revenue_sk as unique_field,
    count(*) as n_records

from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_regional_revenue
where regional_revenue_sk is not null
group by regional_revenue_sk
having count(*) > 1


