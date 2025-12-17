

/*
    GA4 Sessions Fact Table
    Exposes total sessions (not just engaged) and session quality metrics
    Source: GA4.TRAFFIC_ACQUISITION_SESSION_SOURCE_MEDIUM_REPORT
*/

with session_source_medium as (
    select
        date as date_day,
        property,
        session_source,
        session_medium,

        -- Session counts (total, not just engaged!)
        sessions as total_sessions,
        engaged_sessions,

        -- User metrics
        total_users,

        -- Engagement metrics
        engagement_rate,
        events_per_session,
        user_engagement_duration,
        event_count,

        -- Conversion metrics
        key_events,
        total_revenue

    from CLIENT_RARE_SEEDS_DB.GA4.traffic_acquisition_session_source_medium_report
),

-- Aggregate by date and source/medium
daily_sessions as (
    select
        date_day,
        session_source,
        session_medium,
        concat(
            coalesce(session_source, '(direct)'),
            ' / ',
            coalesce(session_medium, '(none)')
        ) as source_medium,

        -- Session totals
        sum(total_sessions) as total_sessions,
        sum(engaged_sessions) as engaged_sessions,
        sum(total_users) as total_users,

        -- Engagement metrics (weighted average)
        case
            when sum(total_sessions) > 0
            then sum(engaged_sessions)::float / sum(total_sessions)
            else 0
        end as engagement_rate,

        -- Average events per session (weighted)
        case
            when sum(total_sessions) > 0
            then sum(events_per_session * total_sessions) / sum(total_sessions)
            else 0
        end as avg_events_per_session,

        -- Total engagement duration
        sum(user_engagement_duration) as total_engagement_duration,

        -- Average engagement duration per session
        case
            when sum(total_sessions) > 0
            then sum(user_engagement_duration) / sum(total_sessions)
            else 0
        end as avg_engagement_duration_per_session,

        -- Event totals
        sum(event_count) as total_events,
        sum(key_events) as total_key_events,

        -- Revenue
        sum(total_revenue) as total_revenue

    from session_source_medium
    group by date_day, session_source, session_medium
)

select
    md5(cast(coalesce(cast(date_day as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(source_medium as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as ga4_session_sk,
    'ga4' as platform,

    -- Date dimensions
    date_day,
    date_trunc('week', date_day)::date as date_week,
    date_trunc('month', date_day)::date as date_month,
    extract(dow from date_day) as day_of_week,

    -- Traffic source
    session_source,
    session_medium,
    source_medium,

    -- Session metrics (KEY: Total sessions, not just engaged!)
    total_sessions,
    engaged_sessions,
    total_sessions - engaged_sessions as non_engaged_sessions,

    -- User metrics
    total_users,

    -- Engagement metrics
    round(engagement_rate * 100, 2) as engagement_rate_pct,
    round((1 - engagement_rate) * 100, 2) as bounce_proxy_pct,  -- Proxy for bounce rate
    round(avg_events_per_session, 2) as avg_events_per_session,
    round(avg_engagement_duration_per_session, 2) as avg_engagement_duration_sec,

    -- Engagement duration in minutes for readability
    round(avg_engagement_duration_per_session / 60, 2) as avg_engagement_duration_min,

    -- Event metrics
    total_events,
    total_key_events,

    -- Conversion rate
    case
        when total_sessions > 0
        then round(total_key_events::float / total_sessions * 100, 4)
        else 0
    end as key_event_rate_pct,

    -- Revenue metrics
    total_revenue,
    case
        when total_sessions > 0
        then round(total_revenue / total_sessions, 2)
        else 0
    end as revenue_per_session,

    -- Session quality score (composite metric)
    case
        when total_sessions > 0
        then round(
            (engagement_rate * 40) +  -- 40% weight on engagement
            (least(avg_events_per_session / 10, 1) * 30) +  -- 30% weight on events (capped at 10)
            (least(avg_engagement_duration_per_session / 300, 1) * 30),  -- 30% weight on duration (capped at 5 min)
            2
        )
        else 0
    end as session_quality_score,

    -- Session quality category
    case
        when engagement_rate >= 0.7 and avg_events_per_session >= 5 then 'High Quality'
        when engagement_rate >= 0.5 and avg_events_per_session >= 3 then 'Medium Quality'
        when engagement_rate >= 0.3 then 'Low Quality'
        else 'Very Low Quality'
    end as session_quality_category,

    -- Traffic source category
    case
        when lower(session_medium) in ('organic', 'seo') then 'Organic Search'
        when lower(session_medium) in ('cpc', 'ppc', 'paid', 'paidsearch') then 'Paid Search'
        when lower(session_medium) in ('email', 'newsletter') then 'Email'
        when lower(session_medium) in ('social', 'social-media', 'sm') then 'Social'
        when lower(session_medium) in ('referral', 'ref') then 'Referral'
        when lower(session_medium) = '(none)' or session_medium is null then 'Direct'
        when lower(session_medium) in ('display', 'banner', 'cpm') then 'Display'
        when lower(session_medium) in ('affiliate', 'affiliates') then 'Affiliate'
        else 'Other'
    end as traffic_channel

from daily_sessions
where total_sessions > 0