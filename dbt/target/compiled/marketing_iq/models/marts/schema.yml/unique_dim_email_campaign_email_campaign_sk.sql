
    
    

select
    email_campaign_sk as unique_field,
    count(*) as n_records

from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.dim_email_campaign
where email_campaign_sk is not null
group by email_campaign_sk
having count(*) > 1


