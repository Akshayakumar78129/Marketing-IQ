
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select hour_key
from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.dim_hour
where hour_key is null



  
  
      
    ) dbt_internal_test