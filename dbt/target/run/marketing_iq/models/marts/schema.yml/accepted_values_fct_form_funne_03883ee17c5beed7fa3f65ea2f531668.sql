
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

with all_values as (

    select
        performance_category as value_field,
        count(*) as n_records

    from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_form_funnel
    group by performance_category

)

select *
from all_values
where value_field not in (
    'No Activity','Excellent (10%+)','Good (5-10%)','Average (2-5%)','Needs Improvement (<2%)'
)



  
  
      
    ) dbt_internal_test