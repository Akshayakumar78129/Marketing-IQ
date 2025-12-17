
    
    

select
    refund_sk as unique_field,
    count(*) as n_records

from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_refunds
where refund_sk is not null
group by refund_sk
having count(*) > 1


