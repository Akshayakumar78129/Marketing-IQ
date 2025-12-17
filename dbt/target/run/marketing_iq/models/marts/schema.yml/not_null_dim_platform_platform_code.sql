
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select platform_code
from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.dim_platform
where platform_code is null



  
  
      
    ) dbt_internal_test