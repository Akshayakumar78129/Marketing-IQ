
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

with all_values as (

    select
        position_category as value_field,
        count(*) as n_records

    from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_keyword_competitive
    group by position_category

)

select *
from all_values
where value_field not in (
    'Dominant (50%+ Absolute Top)','Strong (25-50% Absolute Top)','Competitive (50%+ Top)','Moderate (25-50% Top)','Weak (<25% Top)','No Position Data'
)



  
  
      
    ) dbt_internal_test