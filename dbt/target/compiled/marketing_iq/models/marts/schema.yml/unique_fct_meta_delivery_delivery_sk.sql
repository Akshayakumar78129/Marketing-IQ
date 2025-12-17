
    
    

select
    delivery_sk as unique_field,
    count(*) as n_records

from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_meta_delivery
where delivery_sk is not null
group by delivery_sk
having count(*) > 1


