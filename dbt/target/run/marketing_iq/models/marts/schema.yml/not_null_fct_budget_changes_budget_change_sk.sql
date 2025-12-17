
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select budget_change_sk
from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_budget_changes
where budget_change_sk is null



  
  
      
    ) dbt_internal_test