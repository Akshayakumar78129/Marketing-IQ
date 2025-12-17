
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select ga4_traffic_sk
from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_ga4_traffic
where ga4_traffic_sk is null



  
  
      
    ) dbt_internal_test