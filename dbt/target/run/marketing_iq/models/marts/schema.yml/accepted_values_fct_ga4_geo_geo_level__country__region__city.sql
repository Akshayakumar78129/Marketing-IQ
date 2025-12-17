
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

with all_values as (

    select
        geo_level as value_field,
        count(*) as n_records

    from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_ga4_geo
    group by geo_level

)

select *
from all_values
where value_field not in (
    'country','region','city'
)



  
  
      
    ) dbt_internal_test