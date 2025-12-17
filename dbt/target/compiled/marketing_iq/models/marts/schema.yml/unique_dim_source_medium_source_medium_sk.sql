
    
    

select
    source_medium_sk as unique_field,
    count(*) as n_records

from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.dim_source_medium
where source_medium_sk is not null
group by source_medium_sk
having count(*) > 1


