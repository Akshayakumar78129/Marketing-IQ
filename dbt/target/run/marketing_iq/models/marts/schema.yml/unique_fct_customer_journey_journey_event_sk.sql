
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

select
    journey_event_sk as unique_field,
    count(*) as n_records

from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_customer_journey
where journey_event_sk is not null
group by journey_event_sk
having count(*) > 1



  
  
      
    ) dbt_internal_test