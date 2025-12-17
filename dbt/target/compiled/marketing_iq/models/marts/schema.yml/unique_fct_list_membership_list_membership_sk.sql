
    
    

select
    list_membership_sk as unique_field,
    count(*) as n_records

from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.fct_list_membership
where list_membership_sk is not null
group by list_membership_sk
having count(*) > 1


