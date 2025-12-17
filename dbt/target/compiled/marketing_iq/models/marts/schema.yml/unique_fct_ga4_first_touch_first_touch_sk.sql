
    
    

select
    first_touch_sk as unique_field,
    count(*) as n_records

from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_ga4_first_touch
where first_touch_sk is not null
group by first_touch_sk
having count(*) > 1


