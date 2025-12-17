
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select form_submissions
from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_form_funnel
where form_submissions is null



  
  
      
    ) dbt_internal_test