
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select klaviyo_revenue_sk
from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_klaviyo_revenue
where klaviyo_revenue_sk is null



  
  
      
    ) dbt_internal_test