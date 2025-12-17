
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select geography_sk
from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.dim_geography
where geography_sk is null



  
  
      
    ) dbt_internal_test