
    
    

select
    conversion_action_sk as unique_field,
    count(*) as n_records

from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.dim_conversion_action
where conversion_action_sk is not null
group by conversion_action_sk
having count(*) > 1


