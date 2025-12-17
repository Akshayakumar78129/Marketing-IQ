
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

select
    ecommerce_item_sk as unique_field,
    count(*) as n_records

from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_ecommerce_item
where ecommerce_item_sk is not null
group by ecommerce_item_sk
having count(*) > 1



  
  
      
    ) dbt_internal_test