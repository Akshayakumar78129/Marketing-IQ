
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select segment_membership_sk
from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_segment_membership
where segment_membership_sk is null



  
  
      
    ) dbt_internal_test