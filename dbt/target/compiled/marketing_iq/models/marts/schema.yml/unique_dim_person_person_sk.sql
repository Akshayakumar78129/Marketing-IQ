
    
    

select
    person_sk as unique_field,
    count(*) as n_records

from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.dim_person
where person_sk is not null
group by person_sk
having count(*) > 1


