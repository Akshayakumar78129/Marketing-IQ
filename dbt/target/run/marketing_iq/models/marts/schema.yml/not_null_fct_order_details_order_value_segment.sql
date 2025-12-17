
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select order_value_segment
from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_order_details
where order_value_segment is null



  
  
      
    ) dbt_internal_test