
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

with all_values as (

    select
        platform as value_field,
        count(*) as n_records

    from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_email_health
    group by platform

)

select *
from all_values
where value_field not in (
    'klaviyo'
)



  
  
      
    ) dbt_internal_test