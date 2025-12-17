
    
    

select
    ad_set_sk as unique_field,
    count(*) as n_records

from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.dim_ad_set
where ad_set_sk is not null
group by ad_set_sk
having count(*) > 1


