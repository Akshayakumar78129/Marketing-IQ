
    
    

select
    klaviyo_revenue_sk as unique_field,
    count(*) as n_records

from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_klaviyo_revenue
where klaviyo_revenue_sk is not null
group by klaviyo_revenue_sk
having count(*) > 1


