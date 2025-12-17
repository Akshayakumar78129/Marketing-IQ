
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select refund_sk
from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_refunds
where refund_sk is null



  
  
      
    ) dbt_internal_test