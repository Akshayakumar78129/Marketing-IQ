
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select publisher_platform
from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_meta_device_performance
where publisher_platform is null



  
  
      
    ) dbt_internal_test