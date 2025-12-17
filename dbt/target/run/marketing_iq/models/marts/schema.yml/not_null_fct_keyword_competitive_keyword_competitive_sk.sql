
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select keyword_competitive_sk
from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_keyword_competitive
where keyword_competitive_sk is null



  
  
      
    ) dbt_internal_test