
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

select
    email_template_sk as unique_field,
    count(*) as n_records

from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.dim_email_template
where email_template_sk is not null
group by email_template_sk
having count(*) > 1



  
  
      
    ) dbt_internal_test