
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

with all_values as (

    select
        health_category as value_field,
        count(*) as n_records

    from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_email_health
    group by health_category

)

select *
from all_values
where value_field not in (
    'No Activity','Critical (5%+ Bounce)','Warning (2-5% Bounce)','Spam Alert (>0.1%)','List Shrinking','Healthy'
)



  
  
      
    ) dbt_internal_test