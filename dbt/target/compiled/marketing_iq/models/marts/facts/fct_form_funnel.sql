

/*
    Form Funnel Fact Table
    Tracks form view -> submission -> completion funnel from Klaviyo events
    Source: KLAVIYO.EVENT, KLAVIYO.METRIC
*/

with form_metrics as (
    select
        id as metric_id,
        name as metric_name
    from CLIENT_RARE_SEEDS_DB.KLAVIYO.metric
    where lower(name) like '%form%'
),

form_events as (
    select
        e.id as event_id,
        e.person_id,
        date(e.datetime) as event_date,
        e.datetime as event_timestamp,
        m.metric_name,
        e.property_value,
        e.campaign_id,
        e.flow_id,
        -- Categorize form events into funnel stages
        case
            when lower(m.metric_name) in ('viewed form', 'viewed_form_step') then 'view'
            when lower(m.metric_name) in ('submitted form', 'submitted_form_step', 'form submitted by profile') then 'submit'
            when lower(m.metric_name) in ('form completed by profile') then 'complete'
            when lower(m.metric_name) = 'closed form' then 'abandon'
            else 'other'
        end as funnel_stage
    from CLIENT_RARE_SEEDS_DB.KLAVIYO.event e
    inner join form_metrics m on e.metric_id = m.metric_id
),

-- Aggregate by date
daily_form_metrics as (
    select
        event_date as date_day,

        -- View stage
        count(case when funnel_stage = 'view' then 1 end) as form_views,
        count(distinct case when funnel_stage = 'view' then person_id end) as unique_form_viewers,

        -- Submit stage
        count(case when funnel_stage = 'submit' then 1 end) as form_submissions,
        count(distinct case when funnel_stage = 'submit' then person_id end) as unique_form_submitters,

        -- Complete stage
        count(case when funnel_stage = 'complete' then 1 end) as form_completions,
        count(distinct case when funnel_stage = 'complete' then person_id end) as unique_form_completers,

        -- Abandon stage
        count(case when funnel_stage = 'abandon' then 1 end) as form_abandons,
        count(distinct case when funnel_stage = 'abandon' then person_id end) as unique_form_abandoners,

        -- Total unique persons interacting with forms
        count(distinct person_id) as unique_form_users

    from form_events
    group by event_date
),

-- Get form-attributed campaign/flow data
form_attribution as (
    select
        event_date as date_day,
        campaign_id,
        flow_id,
        count(case when funnel_stage = 'view' then 1 end) as views,
        count(case when funnel_stage = 'submit' then 1 end) as submissions,
        count(case when funnel_stage = 'complete' then 1 end) as completions
    from form_events
    where campaign_id is not null or flow_id is not null
    group by event_date, campaign_id, flow_id
)

select
    md5(cast(coalesce(cast(date_day as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as form_funnel_sk,
    'klaviyo' as platform,
    date_day,
    date_trunc('week', date_day)::date as date_week,
    date_trunc('month', date_day)::date as date_month,
    extract(dow from date_day) as day_of_week,

    -- Funnel counts
    form_views,
    unique_form_viewers,
    form_submissions,
    unique_form_submitters,
    form_completions,
    unique_form_completers,
    form_abandons,
    unique_form_abandoners,
    unique_form_users,

    -- Conversion rates (View -> Submit)
    case
        when form_views > 0
        then round(form_submissions::float / form_views * 100, 2)
        else 0
    end as view_to_submit_rate,

    -- Conversion rates (Submit -> Complete)
    case
        when form_submissions > 0
        then round(form_completions::float / form_submissions * 100, 2)
        else 0
    end as submit_to_complete_rate,

    -- Overall conversion rate (View -> Complete)
    case
        when form_views > 0
        then round(form_completions::float / form_views * 100, 2)
        else 0
    end as overall_conversion_rate,

    -- Abandonment rate
    case
        when form_views > 0
        then round(form_abandons::float / form_views * 100, 2)
        else 0
    end as abandonment_rate,

    -- Unique user conversion rates
    case
        when unique_form_viewers > 0
        then round(unique_form_submitters::float / unique_form_viewers * 100, 2)
        else 0
    end as unique_view_to_submit_rate,

    case
        when unique_form_viewers > 0
        then round(unique_form_completers::float / unique_form_viewers * 100, 2)
        else 0
    end as unique_overall_conversion_rate,

    -- Funnel efficiency score (weighted completion)
    case
        when form_views > 0
        then round(
            (form_completions * 1.0 + form_submissions * 0.5) / form_views * 100,
            2
        )
        else 0
    end as funnel_efficiency_score,

    -- Drop-off at each stage
    form_views - form_submissions as view_to_submit_dropoff,
    form_submissions - form_completions as submit_to_complete_dropoff,

    -- Performance category
    case
        when form_views = 0 then 'No Activity'
        when (form_completions::float / nullif(form_views, 0)) >= 0.10 then 'Excellent (10%+)'
        when (form_completions::float / nullif(form_views, 0)) >= 0.05 then 'Good (5-10%)'
        when (form_completions::float / nullif(form_views, 0)) >= 0.02 then 'Average (2-5%)'
        else 'Needs Improvement (<2%)'
    end as performance_category

from daily_form_metrics
where date_day is not null
order by date_day desc