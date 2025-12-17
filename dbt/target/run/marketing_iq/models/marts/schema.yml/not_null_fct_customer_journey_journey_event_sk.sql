
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select journey_event_sk
from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_customer_journey
where journey_event_sk is null



  
  
      
    ) dbt_internal_test