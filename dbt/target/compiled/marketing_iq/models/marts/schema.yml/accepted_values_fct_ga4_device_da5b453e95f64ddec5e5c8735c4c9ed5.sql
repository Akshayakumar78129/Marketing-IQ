
    
    

with all_values as (

    select
        dimension_type as value_field,
        count(*) as n_records

    from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_ga4_device_browser
    group by dimension_type

)

select *
from all_values
where value_field not in (
    'device','browser','platform'
)


