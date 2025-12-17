
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select new_customers
from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_customer_metrics
where new_customers is null



  
  
      
    ) dbt_internal_test