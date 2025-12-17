
    
    

select
    creative_sk as unique_field,
    count(*) as n_records

from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.dim_creative
where creative_sk is not null
group by creative_sk
having count(*) > 1


