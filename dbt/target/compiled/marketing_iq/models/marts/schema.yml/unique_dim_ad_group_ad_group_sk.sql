
    
    

select
    ad_group_sk as unique_field,
    count(*) as n_records

from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.dim_ad_group
where ad_group_sk is not null
group by ad_group_sk
having count(*) > 1


