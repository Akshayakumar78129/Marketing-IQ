
    
    

select
    hour_key as unique_field,
    count(*) as n_records

from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.dim_hour
where hour_key is not null
group by hour_key
having count(*) > 1


