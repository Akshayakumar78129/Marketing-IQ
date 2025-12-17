
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select bidding_strategy_sk
from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.dim_bidding_strategy
where bidding_strategy_sk is null



  
  
      
    ) dbt_internal_test