
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select ad_set_sk
from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.dim_ad_set
where ad_set_sk is null



  
  
      
    ) dbt_internal_test