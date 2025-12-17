
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

select
    customer_metrics_sk as unique_field,
    count(*) as n_records

from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_customer_metrics
where customer_metrics_sk is not null
group by customer_metrics_sk
having count(*) > 1



  
  
      
    ) dbt_internal_test