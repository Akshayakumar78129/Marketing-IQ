
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select ga4_conversion_sk
from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_ga4_conversions
where ga4_conversion_sk is null



  
  
      
    ) dbt_internal_test