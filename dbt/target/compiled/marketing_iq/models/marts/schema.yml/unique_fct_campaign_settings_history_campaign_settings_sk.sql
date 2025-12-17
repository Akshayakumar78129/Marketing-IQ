
    
    

select
    campaign_settings_sk as unique_field,
    count(*) as n_records

from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_campaign_settings_history
where campaign_settings_sk is not null
group by campaign_settings_sk
having count(*) > 1


