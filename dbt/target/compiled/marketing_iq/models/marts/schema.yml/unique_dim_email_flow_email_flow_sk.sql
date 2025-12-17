
    
    

select
    email_flow_sk as unique_field,
    count(*) as n_records

from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.dim_email_flow
where email_flow_sk is not null
group by email_flow_sk
having count(*) > 1


