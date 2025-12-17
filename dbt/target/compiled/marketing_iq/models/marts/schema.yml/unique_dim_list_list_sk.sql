
    
    

select
    list_sk as unique_field,
    count(*) as n_records

from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.dim_list
where list_sk is not null
group by list_sk
having count(*) > 1


