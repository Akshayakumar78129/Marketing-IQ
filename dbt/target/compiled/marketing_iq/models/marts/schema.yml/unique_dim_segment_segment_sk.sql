
    
    

select
    segment_sk as unique_field,
    count(*) as n_records

from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.dim_segment
where segment_sk is not null
group by segment_sk
having count(*) > 1


