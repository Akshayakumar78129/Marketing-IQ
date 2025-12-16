{{
    config(
        materialized='table',
        tags=['dimensions']
    )
}}

/*
    Email Campaign dimension table (Klaviyo)
    Source: KLAVIYO.CAMPAIGN, KLAVIYO.CAMPAIGN_MESSAGE
*/

with campaigns as (
    select
        c.id as campaign_id,
        c.name as campaign_name,
        c.status,
        c.archived,
        c.send_time,
        c.send_strategy_method,
        c.tracking_options_is_tracking_opens as is_tracking_opens,
        c.tracking_options_is_tracking_clicks as is_tracking_clicks,
        c.tracking_options_is_add_utm as is_add_utm,
        c.created,
        c.scheduled,
        c.updated,
        c._fivetran_deleted as is_deleted,
        c._fivetran_synced as last_synced
    from {{ source('klaviyo', 'campaign') }} c
    where c._fivetran_deleted = false
),

campaign_messages as (
    select
        campaign_id,
        count(*) as message_count,
        max(channel) as primary_channel,
        max(content_subject) as subject_line
    from {{ source('klaviyo', 'campaign_message') }}
    where _fivetran_deleted = false
    group by campaign_id
)

select
    {{ dbt_utils.generate_surrogate_key(['c.campaign_id']) }} as email_campaign_sk,
    'klaviyo' as platform,
    c.campaign_id,
    c.campaign_name,
    c.status,
    c.archived as is_archived,
    c.send_time,
    c.send_strategy_method,
    c.is_tracking_opens,
    c.is_tracking_clicks,
    c.is_add_utm,
    cm.message_count,
    cm.primary_channel,
    cm.subject_line,
    c.created as created_at,
    c.scheduled as scheduled_at,
    c.updated as updated_at,
    c.last_synced
from campaigns c
left join campaign_messages cm on c.campaign_id = cm.campaign_id
