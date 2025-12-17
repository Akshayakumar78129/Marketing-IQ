
    
    

select
    ga4_event_sk as unique_field,
    count(*) as n_records

from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_ga4_events
where ga4_event_sk is not null
group by ga4_event_sk
having count(*) > 1


