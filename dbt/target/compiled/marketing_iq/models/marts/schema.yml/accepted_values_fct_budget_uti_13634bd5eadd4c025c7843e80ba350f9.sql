
    
    

with all_values as (

    select
        utilization_category as value_field,
        count(*) as n_records

    from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_budget_utilization
    group by utilization_category

)

select *
from all_values
where value_field not in (
    'No Budget Set','Significantly Overspent (>120%)','Overspent (100-120%)','On Track (80-100%)','Underspent (50-80%)','Significantly Underspent (<50%)'
)


