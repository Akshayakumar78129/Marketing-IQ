
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select platform
from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_ga4_sessions
where platform is null



  
  
      
    ) dbt_internal_test