
    
    

select
    form_funnel_sk as unique_field,
    count(*) as n_records

from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_form_funnel
where form_funnel_sk is not null
group by form_funnel_sk
having count(*) > 1


