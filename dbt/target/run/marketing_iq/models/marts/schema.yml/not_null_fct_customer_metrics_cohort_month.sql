
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select cohort_month
from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_customer_metrics
where cohort_month is null



  
  
      
    ) dbt_internal_test