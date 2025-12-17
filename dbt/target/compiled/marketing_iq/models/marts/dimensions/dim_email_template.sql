

/*
    Email Template dimension table (Klaviyo)
    Source: KLAVIYO.EMAIL_TEMPLATE
*/

with templates as (
    select
        id as template_id,
        name as template_name,
        editor_type,
        -- Store HTML length instead of full content for performance
        length(html) as html_length,
        length(text) as text_length,
        created as created_at,
        updated as updated_at,
        _fivetran_deleted as is_deleted,
        _fivetran_synced as last_synced
    from CLIENT_RARE_SEEDS_DB.KLAVIYO.email_template
    where _fivetran_deleted = false
)

select
    md5(cast(coalesce(cast(template_id as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as email_template_sk,
    'klaviyo' as platform,
    template_id,
    template_name,
    editor_type,
    html_length,
    text_length,
    case when html_length > 0 then true else false end as has_html,
    case when text_length > 0 then true else false end as has_text,
    created_at,
    updated_at,
    last_synced
from templates