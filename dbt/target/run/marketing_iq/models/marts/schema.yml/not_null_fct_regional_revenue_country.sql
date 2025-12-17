
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select country
from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_regional_revenue
where country is null



  
  
      
    ) dbt_internal_test