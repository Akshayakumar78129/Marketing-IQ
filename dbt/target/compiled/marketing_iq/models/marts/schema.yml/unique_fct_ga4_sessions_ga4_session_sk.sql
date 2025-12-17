
    
    

select
    ga4_session_sk as unique_field,
    count(*) as n_records

from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_ga4_sessions
where ga4_session_sk is not null
group by ga4_session_sk
having count(*) > 1


