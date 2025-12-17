
    
    

with all_values as (

    select
        funnel_stage as value_field,
        count(*) as n_records

    from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_customer_journey
    group by funnel_stage

)

select *
from all_values
where value_field not in (
    'awareness','consideration','intent','purchase','fulfillment','refund'
)


