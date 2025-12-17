
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select email_health_sk
from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_email_health
where email_health_sk is null



  
  
      
    ) dbt_internal_test