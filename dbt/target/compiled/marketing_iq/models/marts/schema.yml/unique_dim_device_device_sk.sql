
    
    

select
    device_sk as unique_field,
    count(*) as n_records

from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.dim_device
where device_sk is not null
group by device_sk
having count(*) > 1


