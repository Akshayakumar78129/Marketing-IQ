
    
    

select
    ad_sk as unique_field,
    count(*) as n_records

from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.dim_ad
where ad_sk is not null
group by ad_sk
having count(*) > 1


