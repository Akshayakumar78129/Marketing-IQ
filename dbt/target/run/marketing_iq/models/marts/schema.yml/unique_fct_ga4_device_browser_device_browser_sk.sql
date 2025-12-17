
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

select
    device_browser_sk as unique_field,
    count(*) as n_records

from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_ga4_device_browser
where device_browser_sk is not null
group by device_browser_sk
having count(*) > 1



  
  
      
    ) dbt_internal_test