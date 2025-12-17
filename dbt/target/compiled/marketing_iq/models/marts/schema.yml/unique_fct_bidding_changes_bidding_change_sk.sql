
    
    

select
    bidding_change_sk as unique_field,
    count(*) as n_records

from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_bidding_changes
where bidding_change_sk is not null
group by bidding_change_sk
having count(*) > 1


