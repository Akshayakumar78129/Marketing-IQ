
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select delivery_sk
from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_meta_delivery
where delivery_sk is null



  
  
      
    ) dbt_internal_test