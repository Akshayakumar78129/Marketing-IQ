
    
    

select
    ad_group_settings_sk as unique_field,
    count(*) as n_records

from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_ad_group_settings_history
where ad_group_settings_sk is not null
group by ad_group_settings_sk
having count(*) > 1


