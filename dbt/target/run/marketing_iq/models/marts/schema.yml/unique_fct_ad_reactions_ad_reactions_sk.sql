
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

select
    ad_reactions_sk as unique_field,
    count(*) as n_records

from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_ad_reactions
where ad_reactions_sk is not null
group by ad_reactions_sk
having count(*) > 1



  
  
      
    ) dbt_internal_test