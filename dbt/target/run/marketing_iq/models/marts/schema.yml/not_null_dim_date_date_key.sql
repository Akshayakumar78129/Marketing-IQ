
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select date_key
from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.dim_date
where date_key is null



  
  
      
    ) dbt_internal_test