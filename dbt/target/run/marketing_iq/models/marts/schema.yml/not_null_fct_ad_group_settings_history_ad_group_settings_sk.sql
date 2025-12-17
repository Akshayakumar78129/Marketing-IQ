
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select ad_group_settings_sk
from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_ad_group_settings_history
where ad_group_settings_sk is null



  
  
      
    ) dbt_internal_test