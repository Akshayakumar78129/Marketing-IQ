
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select device_platform
from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_meta_device_performance
where device_platform is null



  
  
      
    ) dbt_internal_test