
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select keyword_performance_sk
from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_keyword_performance
where keyword_performance_sk is null



  
  
      
    ) dbt_internal_test