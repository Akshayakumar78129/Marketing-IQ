{{
    config(
        materialized='incremental',
        unique_key='demographics_sk',
        tags=['facts', 'meta', 'demographics']
    )
}}

/*
    Meta Ads Demographics Fact Table
    Performance metrics by age and gender
    Source: META_ADS.DEMOGRAPHICS_AGE, DEMOGRAPHICS_GENDER
*/

with age_data as (
    select
        account_id::varchar as account_id,
        date as date_day,
        age as age_bracket,
        null as gender,
        impressions,
        reach,
        inline_link_clicks as clicks,
        spend,
        cpc,
        cpm,
        ctr,
        frequency,
        _fivetran_synced as last_synced
    from {{ source('meta_ads', 'demographics_age') }}
    {% if is_incremental() %}
    where _fivetran_synced > (select max(last_synced) from {{ this }})
    {% endif %}
),

gender_data as (
    select
        account_id::varchar as account_id,
        date as date_day,
        null as age_bracket,
        gender,
        impressions,
        reach,
        inline_link_clicks as clicks,
        spend,
        cpc,
        cpm,
        ctr,
        frequency,
        _fivetran_synced as last_synced
    from {{ source('meta_ads', 'demographics_gender') }}
    {% if is_incremental() %}
    where _fivetran_synced > (select max(last_synced) from {{ this }})
    {% endif %}
),

combined as (
    select * from age_data
    union all
    select * from gender_data
)

select
    {{ dbt_utils.generate_surrogate_key(['account_id', 'date_day', 'age_bracket', 'gender']) }} as demographics_sk,
    'meta' as platform,
    account_id,
    date_day,
    age_bracket,
    gender,

    -- Demographic type
    case
        when age_bracket is not null then 'age'
        when gender is not null then 'gender'
        else 'unknown'
    end as demographic_type,

    -- Metrics
    impressions,
    reach,
    clicks,
    spend,
    frequency,

    -- Rates
    cpc,
    cpm,
    ctr,

    -- Calculated metrics (backup)
    case when ctr is null and impressions > 0 then clicks::float / impressions else ctr end as calculated_ctr,
    case when cpc is null and clicks > 0 then spend / clicks else cpc end as calculated_cpc,

    last_synced
from combined
