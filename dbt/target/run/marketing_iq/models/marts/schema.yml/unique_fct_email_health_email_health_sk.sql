
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

select
    email_health_sk as unique_field,
    count(*) as n_records

from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_email_health
where email_health_sk is not null
group by email_health_sk
having count(*) > 1



  
  
      
    ) dbt_internal_test