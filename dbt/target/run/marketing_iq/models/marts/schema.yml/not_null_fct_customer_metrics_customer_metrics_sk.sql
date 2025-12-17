
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select customer_metrics_sk
from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_customer_metrics
where customer_metrics_sk is null



  
  
      
    ) dbt_internal_test