
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select form_completions
from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_form_funnel
where form_completions is null



  
  
      
    ) dbt_internal_test