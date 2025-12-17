

/*
    Source/Medium dimension table
    Source: GA4 traffic acquisition reports
*/

with source_medium as (
    select distinct
        session_source as source,
        session_medium as medium
    from CLIENT_RARE_SEEDS_DB.GA4.traffic_acquisition_session_source_medium_report
    where session_source is not null or session_medium is not null
)

select
    md5(cast(coalesce(cast(source as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(medium as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as source_medium_sk,
    source,
    medium,
    coalesce(source, '(direct)') || ' / ' || coalesce(medium, '(none)') as source_medium,
    case
        when lower(medium) in ('cpc', 'ppc', 'paid', 'paidsearch') then 'Paid Search'
        when lower(medium) in ('organic', 'seo') then 'Organic Search'
        when lower(medium) in ('social', 'social-media', 'sm') then 'Social'
        when lower(medium) = 'email' then 'Email'
        when lower(medium) = 'referral' then 'Referral'
        when lower(medium) = 'display' then 'Display'
        when lower(medium) = 'affiliate' then 'Affiliate'
        when medium is null or lower(medium) = '(none)' then 'Direct'
        else 'Other'
    end as channel_grouping,
    case
        when lower(medium) in ('cpc', 'ppc', 'paid', 'paidsearch', 'display') then true
        else false
    end as is_paid
from source_medium