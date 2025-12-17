
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select meta_conversion_sk
from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_meta_conversion
where meta_conversion_sk is null



  
  
      
    ) dbt_internal_test