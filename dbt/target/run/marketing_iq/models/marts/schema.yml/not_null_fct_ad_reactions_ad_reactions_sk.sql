
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select ad_reactions_sk
from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_ad_reactions
where ad_reactions_sk is null



  
  
      
    ) dbt_internal_test