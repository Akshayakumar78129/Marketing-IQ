
    
    

select
    campaign_sk as unique_field,
    count(*) as n_records

from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.dim_campaign
where campaign_sk is not null
group by campaign_sk
having count(*) > 1


