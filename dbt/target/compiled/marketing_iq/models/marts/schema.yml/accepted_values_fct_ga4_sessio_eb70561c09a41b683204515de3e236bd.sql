
    
    

with all_values as (

    select
        session_quality_category as value_field,
        count(*) as n_records

    from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_ga4_sessions
    group by session_quality_category

)

select *
from all_values
where value_field not in (
    'High Quality','Medium Quality','Low Quality','Very Low Quality'
)


