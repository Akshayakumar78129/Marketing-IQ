

/*
    Unified campaign performance fact table
    Combines Google Ads and Facebook Ads campaign data
    Source: GOOGLE_ADS.CAMPAIGN_STATS, FACEBOOK_ADS.BASIC_AD
*/

with google_ads_stats as (
    select
        date as date_day,
        customer_id::varchar as account_id,
        id::varchar as campaign_id,
        device,
        ad_network_type,
        sum(impressions) as impressions,
        sum(clicks) as clicks,
        sum(cost_micros) / 1000000.0 as spend,
        sum(conversions) as conversions,
        sum(conversions_value) as conversion_value,
        sum(view_through_conversions) as view_through_conversions,
        max(_fivetran_synced) as last_synced
    from CLIENT_RARE_SEEDS_DB.GOOGLE_ADS.campaign_stats
    group by date, customer_id, id, device, ad_network_type
),

google_ads_campaign_info as (
    select
        id::varchar as campaign_id,
        customer_id::varchar as account_id,
        name as campaign_name,
        status,
        advertising_channel_type as campaign_type
    from CLIENT_RARE_SEEDS_DB.GOOGLE_ADS.campaign_history
    where _fivetran_active = true
),

google_ads as (
    select
        s.date_day,
        'google_ads' as platform,
        s.account_id,
        s.campaign_id,
        coalesce(c.campaign_name, 'Unknown') as campaign_name,
        c.status,
        c.campaign_type,
        s.device,
        s.ad_network_type,
        s.impressions,
        s.clicks,
        s.spend,
        s.conversions,
        s.conversion_value,
        s.view_through_conversions,
        s.last_synced
    from google_ads_stats s
    left join google_ads_campaign_info c on s.campaign_id = c.campaign_id
),

facebook_ads_campaign_info as (
    select
        id::varchar as campaign_id,
        account_id::varchar as account_id,
        name as campaign_name,
        status
    from CLIENT_RARE_SEEDS_DB.META_ADS.campaign_history
),

-- Meta campaign-level conversions (purchase counts)
meta_campaign_conversions as (
    select
        campaign_id::varchar as campaign_id,
        date as date_day,
        sum(case when action_type = 'purchase' then value else 0 end) as conversions
    from CLIENT_RARE_SEEDS_DB.META_ADS.basic_campaign_actions
    where action_type = 'purchase'
    group by campaign_id, date
),

-- Meta conversion values (revenue) - aggregated from ad level to campaign level
meta_ad_conversion_values as (
    select
        a.campaign_id::varchar as campaign_id,
        v.date as date_day,
        sum(v.value) as conversion_value
    from CLIENT_RARE_SEEDS_DB.META_ADS.basic_ad_action_values v
    left join CLIENT_RARE_SEEDS_DB.META_ADS.ad_history a on v.ad_id = a.id
    where v.action_type = 'purchase'
    group by a.campaign_id, v.date
),

facebook_ads_stats as (
    select
        b.date as date_day,
        a.campaign_id::varchar as campaign_id,
        b.account_id::varchar as account_id,
        sum(b.impressions) as impressions,
        sum(b.inline_link_clicks) as clicks,
        sum(b.spend) as spend,
        max(b._fivetran_synced) as last_synced
    from CLIENT_RARE_SEEDS_DB.META_ADS.basic_ad b
    left join CLIENT_RARE_SEEDS_DB.META_ADS.ad_history a on b.ad_id = a.id
    group by b.date, a.campaign_id, b.account_id
),

facebook_ads as (
    select
        s.date_day,
        'meta' as platform,
        s.account_id,
        s.campaign_id,
        coalesce(c.campaign_name, 'Unknown') as campaign_name,
        c.status,
        'SOCIAL' as campaign_type,
        null as device,
        null as ad_network_type,
        s.impressions,
        s.clicks,
        s.spend,
        conv.conversions,
        cval.conversion_value,
        null as view_through_conversions,
        s.last_synced
    from facebook_ads_stats s
    left join facebook_ads_campaign_info c on s.campaign_id = c.campaign_id
    left join meta_campaign_conversions conv
        on s.campaign_id = conv.campaign_id and s.date_day = conv.date_day
    left join meta_ad_conversion_values cval
        on s.campaign_id = cval.campaign_id and s.date_day = cval.date_day
),

combined as (
    select * from google_ads
    union all
    select * from facebook_ads
)

select
    md5(cast(coalesce(cast(date_day as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(platform as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(campaign_id as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(device as TEXT), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(ad_network_type as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as performance_sk,
    date_day,
    platform,
    account_id,
    campaign_id,
    campaign_name,
    status,
    campaign_type,
    device,
    ad_network_type,

    -- Metrics
    impressions,
    clicks,
    spend,
    conversions,
    conversion_value,
    view_through_conversions,

    -- Calculated metrics
    case when impressions > 0 then clicks::float / impressions else 0 end as ctr,
    case when clicks > 0 then spend / clicks else 0 end as cpc,
    case when impressions > 0 then (spend / impressions) * 1000 else 0 end as cpm,
    case when spend > 0 then conversion_value / spend else 0 end as roas,
    case when conversions > 0 then spend / conversions else 0 end as cpa,

    last_synced
from combined