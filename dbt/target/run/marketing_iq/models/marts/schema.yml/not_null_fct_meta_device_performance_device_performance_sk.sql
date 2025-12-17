
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select device_performance_sk
from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_meta_device_performance
where device_performance_sk is null



  
  
      
    ) dbt_internal_test