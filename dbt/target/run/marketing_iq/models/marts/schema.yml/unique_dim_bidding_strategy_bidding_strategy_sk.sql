
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

select
    bidding_strategy_sk as unique_field,
    count(*) as n_records

from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.dim_bidding_strategy
where bidding_strategy_sk is not null
group by bidding_strategy_sk
having count(*) > 1



  
  
      
    ) dbt_internal_test