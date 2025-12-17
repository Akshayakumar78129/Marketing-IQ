
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select video_performance_sk
from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_video_performance
where video_performance_sk is null



  
  
      
    ) dbt_internal_test