
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select platform
from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_email_health
where platform is null



  
  
      
    ) dbt_internal_test