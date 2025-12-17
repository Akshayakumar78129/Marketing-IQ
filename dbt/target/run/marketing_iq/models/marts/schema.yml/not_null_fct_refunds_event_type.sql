
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select event_type
from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_refunds
where event_type is null



  
  
      
    ) dbt_internal_test