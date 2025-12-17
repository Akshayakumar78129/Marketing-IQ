
    
    

select
    image_sk as unique_field,
    count(*) as n_records

from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.dim_image
where image_sk is not null
group by image_sk
having count(*) > 1


