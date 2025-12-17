
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select ecommerce_item_sk
from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_ecommerce_item
where ecommerce_item_sk is null



  
  
      
    ) dbt_internal_test