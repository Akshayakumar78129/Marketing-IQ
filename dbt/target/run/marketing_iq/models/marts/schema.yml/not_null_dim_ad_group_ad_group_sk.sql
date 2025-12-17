
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select ad_group_sk
from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.dim_ad_group
where ad_group_sk is null



  
  
      
    ) dbt_internal_test