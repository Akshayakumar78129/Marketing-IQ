{{
    config(
        materialized='table',
        tags=['facts', 'klaviyo', 'email', 'deliverability']
    )
}}

/*
    Email Health Fact Table
    Tracks email deliverability and list health metrics from Klaviyo
    Source: KLAVIYO.EVENT + KLAVIYO.METRIC
*/

with email_health_metrics as (
    select
        id as metric_id,
        name as metric_name
    from {{ source('klaviyo', 'metric') }}
    where lower(name) in (
        'bounced email',
        'received email',
        'unsubscribed from email marketing',
        'unsubscribed from list',
        'subscribed to list',
        'subscribed to email marketing',
        'marked email as spam',
        'bounce suppression added',
        'dropped email'
    )
),

email_health_events as (
    select
        e.id as event_id,
        date(e.datetime) as event_date,
        m.metric_name,
        e.person_id,
        -- Categorize events
        case
            when lower(m.metric_name) = 'bounced email' then 'bounce'
            when lower(m.metric_name) = 'bounce suppression added' then 'bounce_suppression'
            when lower(m.metric_name) = 'dropped email' then 'dropped'
            when lower(m.metric_name) = 'received email' then 'delivered'
            when lower(m.metric_name) in ('unsubscribed from email marketing', 'unsubscribed from list') then 'unsubscribe'
            when lower(m.metric_name) in ('subscribed to list', 'subscribed to email marketing') then 'subscribe'
            when lower(m.metric_name) = 'marked email as spam' then 'spam'
            else 'other'
        end as event_category
    from {{ source('klaviyo', 'event') }} e
    inner join email_health_metrics m on e.metric_id = m.metric_id
),

-- Daily aggregation
daily_email_health as (
    select
        event_date as date_day,

        -- Delivery metrics
        count(case when event_category = 'delivered' then 1 end) as emails_delivered,
        count(case when event_category = 'bounce' then 1 end) as emails_bounced,
        count(case when event_category = 'bounce_suppression' then 1 end) as bounce_suppressions,
        count(case when event_category = 'dropped' then 1 end) as emails_dropped,

        -- Unique bounced profiles
        count(distinct case when event_category = 'bounce' then person_id end) as unique_bounced_profiles,

        -- List health metrics
        count(case when event_category = 'unsubscribe' then 1 end) as unsubscribes,
        count(case when event_category = 'subscribe' then 1 end) as new_subscribers,

        -- Unique unsubscribed profiles
        count(distinct case when event_category = 'unsubscribe' then person_id end) as unique_unsubscribed_profiles,
        count(distinct case when event_category = 'subscribe' then person_id end) as unique_new_subscribers,

        -- Spam complaints
        count(case when event_category = 'spam' then 1 end) as spam_complaints,
        count(distinct case when event_category = 'spam' then person_id end) as unique_spam_complainers

    from email_health_events
    group by event_date
)

select
    {{ dbt_utils.generate_surrogate_key(['date_day']) }} as email_health_sk,
    'klaviyo' as platform,

    -- Date dimensions
    date_day,
    date_trunc('week', date_day)::date as date_week,
    date_trunc('month', date_day)::date as date_month,
    extract(dow from date_day) as day_of_week,

    -- Delivery metrics
    emails_delivered,
    emails_bounced,
    bounce_suppressions,
    emails_dropped,
    unique_bounced_profiles,

    -- Bounce rate
    case
        when emails_delivered > 0
        then round(emails_bounced::float / (emails_delivered + emails_bounced) * 100, 4)
        else 0
    end as bounce_rate_pct,

    -- List health metrics
    unsubscribes,
    new_subscribers,
    unique_unsubscribed_profiles,
    unique_new_subscribers,

    -- Net subscriber growth
    new_subscribers - unsubscribes as net_subscriber_change,
    unique_new_subscribers - unique_unsubscribed_profiles as net_unique_subscriber_change,

    -- Unsubscribe rate (per delivered)
    case
        when emails_delivered > 0
        then round(unsubscribes::float / emails_delivered * 100, 4)
        else 0
    end as unsubscribe_rate_pct,

    -- Spam complaints
    spam_complaints,
    unique_spam_complainers,

    -- Spam complaint rate
    case
        when emails_delivered > 0
        then round(spam_complaints::float / emails_delivered * 100, 6)
        else 0
    end as spam_rate_pct,

    -- List health score (0-100, higher is better)
    -- Penalizes: bounces, unsubscribes, spam
    -- Rewards: new subscribers, low bounce rate
    case
        when emails_delivered > 0
        then greatest(0, least(100,
            100
            - (case when emails_delivered > 0 then emails_bounced::float / (emails_delivered + emails_bounced) * 100 * 2 else 0 end)  -- Bounce penalty (2x weight)
            - (case when emails_delivered > 0 then unsubscribes::float / emails_delivered * 100 * 1.5 else 0 end)  -- Unsubscribe penalty (1.5x weight)
            - (case when emails_delivered > 0 then spam_complaints::float / emails_delivered * 100 * 10 else 0 end)  -- Spam penalty (10x weight)
            + (case when unsubscribes > 0 then least(new_subscribers::float / unsubscribes * 5, 10) else 10 end)  -- Subscriber growth bonus (max 10 points)
        ))
        else 100
    end as list_health_score,

    -- Health category
    case
        when emails_delivered = 0 then 'No Activity'
        when emails_bounced::float / nullif(emails_delivered + emails_bounced, 0) >= 0.05 then 'Critical (5%+ Bounce)'
        when emails_bounced::float / nullif(emails_delivered + emails_bounced, 0) >= 0.02 then 'Warning (2-5% Bounce)'
        when spam_complaints > 0 and spam_complaints::float / nullif(emails_delivered, 0) >= 0.001 then 'Spam Alert (>0.1%)'
        when unsubscribes > new_subscribers then 'List Shrinking'
        else 'Healthy'
    end as health_category,

    -- Deliverability score (focused on technical delivery)
    case
        when emails_delivered + emails_bounced + emails_dropped > 0
        then round(
            emails_delivered::float / (emails_delivered + emails_bounced + emails_dropped) * 100,
            2
        )
        else 100
    end as deliverability_score

from daily_email_health
where date_day is not null
order by date_day desc
