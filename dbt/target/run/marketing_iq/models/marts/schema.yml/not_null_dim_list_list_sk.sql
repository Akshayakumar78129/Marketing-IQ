
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select list_sk
from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.dim_list
where list_sk is null



  
  
      
    ) dbt_internal_test