
  
    

create or replace transient table CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.dim_email_flow
    
    
    
    as (

/*
    Email Flow dimension table (Klaviyo)
    Source: KLAVIYO.FLOW, KLAVIYO.FLOW_ACTION
*/

with flows as (
    select
        id as flow_id,
        name as flow_name,
        status,
        archived as is_archived,
        trigger_type,
        created as created_at,
        updated as updated_at,
        _fivetran_deleted as is_deleted,
        _fivetran_synced as last_synced
    from CLIENT_RARE_SEEDS_DB.KLAVIYO.flow
    where _fivetran_deleted = false
),

flow_actions as (
    select
        flow_id,
        count(*) as action_count,
        count(case when action_type = 'EMAIL' then 1 end) as email_action_count,
        count(case when action_type = 'SMS' then 1 end) as sms_action_count
    from CLIENT_RARE_SEEDS_DB.KLAVIYO.flow_action
    where _fivetran_deleted = false
    group by flow_id
)

select
    md5(cast(coalesce(cast(f.flow_id as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as email_flow_sk,
    'klaviyo' as platform,
    f.flow_id,
    f.flow_name,
    f.status,
    f.is_archived,
    f.trigger_type,
    fa.action_count,
    fa.email_action_count,
    fa.sms_action_count,
    f.created_at,
    f.updated_at,
    f.last_synced
from flows f
left join flow_actions fa on f.flow_id = fa.flow_id
    )
;


  