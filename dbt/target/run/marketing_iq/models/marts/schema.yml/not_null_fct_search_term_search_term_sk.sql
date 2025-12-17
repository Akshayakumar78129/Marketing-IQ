
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select search_term_sk
from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_search_term
where search_term_sk is null



  
  
      
    ) dbt_internal_test