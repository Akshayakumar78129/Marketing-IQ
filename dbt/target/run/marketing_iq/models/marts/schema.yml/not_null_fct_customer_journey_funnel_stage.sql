
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select funnel_stage
from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_customer_journey
where funnel_stage is null



  
  
      
    ) dbt_internal_test