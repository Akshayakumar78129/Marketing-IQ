
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

with all_values as (

    select
        traffic_channel as value_field,
        count(*) as n_records

    from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_ga4_sessions
    group by traffic_channel

)

select *
from all_values
where value_field not in (
    'Organic Search','Paid Search','Email','Social','Referral','Direct','Display','Affiliate','Other'
)



  
  
      
    ) dbt_internal_test