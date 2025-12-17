
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select audience_performance_sk
from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_audience_performance
where audience_performance_sk is null



  
  
      
    ) dbt_internal_test