
    
    

select
    cohort_month as unique_field,
    count(*) as n_records

from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_customer_metrics
where cohort_month is not null
group by cohort_month
having count(*) > 1


