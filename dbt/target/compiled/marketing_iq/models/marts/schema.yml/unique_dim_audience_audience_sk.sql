
    
    

select
    audience_sk as unique_field,
    count(*) as n_records

from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.dim_audience
where audience_sk is not null
group by audience_sk
having count(*) > 1


