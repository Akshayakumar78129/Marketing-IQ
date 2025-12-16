{{
    config(
        materialized='table',
        tags=['dimensions']
    )
}}

/*
    Platform dimension table
    Based on seed data
*/

select
    platform_code,
    platform_name,
    platform_display_name,
    is_advertising,
    is_analytics,
    is_email
from {{ ref('seed_platforms') }}
