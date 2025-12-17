
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select source_medium_sk
from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.dim_source_medium
where source_medium_sk is null



  
  
      
    ) dbt_internal_test