
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select budget_utilization_sk
from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_budget_utilization
where budget_utilization_sk is null



  
  
      
    ) dbt_internal_test