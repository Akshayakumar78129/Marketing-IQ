
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select conversion_action_sk
from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.dim_conversion_action
where conversion_action_sk is null



  
  
      
    ) dbt_internal_test