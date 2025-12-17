

/*
    Keyword Competitive Metrics Fact Table
    Exposes impression share and competitive position metrics for Google Ads keywords
    Source: GOOGLE_ADS.SEARCH_KEYWORD_STATS
*/

with search_keyword_stats as (
    select
        date as date_day,
        customer_id as account_id,
        campaign_id,
        ad_group_id,
        ad_group_criterion_criterion_id as keyword_id,

        -- Performance metrics
        impressions,
        clicks,
        cost_micros / 1000000.0 as cost,
        ctr,
        average_cpc / 1000000.0 as avg_cpc,
        average_cpm / 1000000.0 as avg_cpm,

        -- Conversion metrics
        conversions_value as conversion_value,
        conversions_from_interactions_rate as conversion_rate,
        view_through_conversions,

        -- Competitive position metrics (the key new data!)
        top_impression_percentage,
        absolute_top_impression_percentage

    from CLIENT_RARE_SEEDS_DB.GOOGLE_ADS.search_keyword_stats
    where impressions > 0
),

-- Get keyword info from dim_keyword (using keyword_id + ad_group_id as unique key)
keyword_info as (
    select
        keyword_id,
        ad_group_id,
        keyword_text,
        match_type,
        status as keyword_status
    from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.dim_keyword
    where is_current = true
),

-- Get campaign info
campaign_info as (
    select
        campaign_id,
        campaign_name,
        status as campaign_status,
        campaign_type
    from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.dim_campaign
    where platform = 'google_ads'
    and is_current = true
),

-- Get ad group info
ad_group_info as (
    select
        ad_group_id,
        ad_group_name,
        status as ad_group_status
    from CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.dim_ad_group
    where is_current = true
)

select
    md5(cast(coalesce(cast(s.date_day as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(s.keyword_id as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(s.ad_group_id as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(s.campaign_id as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as keyword_competitive_sk,
    'google_ads' as platform,

    -- Date dimensions
    s.date_day,
    date_trunc('week', s.date_day)::date as date_week,
    date_trunc('month', s.date_day)::date as date_month,
    extract(dow from s.date_day) as day_of_week,

    -- Identifiers
    s.account_id,
    s.campaign_id,
    c.campaign_name,
    c.campaign_type,
    s.ad_group_id,
    ag.ad_group_name,
    s.keyword_id,
    k.keyword_text,
    k.match_type,

    -- Performance metrics
    s.impressions,
    s.clicks,
    s.cost,
    s.ctr,
    s.avg_cpc,
    s.avg_cpm,

    -- Conversion metrics
    s.conversion_value,
    s.conversion_rate,
    s.view_through_conversions,

    -- Competitive position metrics
    s.top_impression_percentage,
    s.absolute_top_impression_percentage,

    -- Calculated: Non-top impression percentage (appeared lower on page)
    case
        when s.top_impression_percentage is not null
        then round((1 - s.top_impression_percentage) * 100, 2)
        else null
    end as below_top_impression_pct,

    -- Calculated: Gap between top and absolute top
    case
        when s.top_impression_percentage is not null
        and s.absolute_top_impression_percentage is not null
        then round((s.top_impression_percentage - s.absolute_top_impression_percentage) * 100, 2)
        else null
    end as top_vs_absolute_gap_pct,

    -- Position category
    case
        when s.absolute_top_impression_percentage >= 0.5 then 'Dominant (50%+ Absolute Top)'
        when s.absolute_top_impression_percentage >= 0.25 then 'Strong (25-50% Absolute Top)'
        when s.top_impression_percentage >= 0.5 then 'Competitive (50%+ Top)'
        when s.top_impression_percentage >= 0.25 then 'Moderate (25-50% Top)'
        when s.top_impression_percentage > 0 then 'Weak (<25% Top)'
        else 'No Position Data'
    end as position_category,

    -- ROAS calculation
    case
        when s.cost > 0
        then round(s.conversion_value / s.cost, 2)
        else 0
    end as roas,

    -- Cost efficiency at position
    case
        when s.absolute_top_impression_percentage > 0 and s.cost > 0
        then round(s.cost / (s.absolute_top_impression_percentage * 100), 4)
        else null
    end as cost_per_abs_top_imp_pct

from search_keyword_stats s
left join keyword_info k on s.keyword_id = k.keyword_id and s.ad_group_id = k.ad_group_id
left join campaign_info c on s.campaign_id = c.campaign_id
left join ad_group_info ag on s.ad_group_id = ag.ad_group_id