
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select first_touch_sk
from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_ga4_first_touch
where first_touch_sk is null



  
  
      
    ) dbt_internal_test