
    
    

select
    meta_conversion_sk as unique_field,
    count(*) as n_records

from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_meta_conversion
where meta_conversion_sk is not null
group by meta_conversion_sk
having count(*) > 1


