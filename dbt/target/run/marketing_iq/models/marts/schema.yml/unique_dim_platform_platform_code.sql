
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

select
    platform_code as unique_field,
    count(*) as n_records

from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.dim_platform
where platform_code is not null
group by platform_code
having count(*) > 1



  
  
      
    ) dbt_internal_test