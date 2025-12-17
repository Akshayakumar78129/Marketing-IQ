
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select geo_level
from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_ga4_geo
where geo_level is null



  
  
      
    ) dbt_internal_test