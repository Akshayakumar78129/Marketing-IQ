
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

select
    segment_membership_sk as unique_field,
    count(*) as n_records

from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_segment_membership
where segment_membership_sk is not null
group by segment_membership_sk
having count(*) > 1



  
  
      
    ) dbt_internal_test