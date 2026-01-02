{{
    config(
        materialized='table',
        tags=['facts', 'magento']
    )
}}

/*
    Magento Coupon Usage Fact Table
    Grain: One row per coupon (aggregated usage)
    Source: MAGENTO.SALESRULE_COUPON, MAGENTO.SALESRULE, MAGENTO.SALES_ORDER
*/

with coupons as (
    select
        coupon_id,
        rule_id,
        code as coupon_code,
        usage_limit,
        usage_per_customer,
        times_used,
        expiration_date,
        is_primary,
        type as coupon_type,
        created_at
    from {{ source('magento', 'salesrule_coupon') }}
),

rules as (
    select
        rule_id,
        name as promotion_name,
        simple_action as discount_type,
        discount_amount,
        from_date,
        to_date,
        is_active,
        times_used as rule_times_used
    from {{ source('magento', 'salesrule') }}
),

-- Get order statistics for each coupon
order_stats as (
    select
        coupon_code,
        count(*) as order_count,
        sum(base_grand_total) as total_order_value,
        sum(coalesce(base_discount_amount, 0)) as total_discount_given,
        min(created_at) as first_order_date,
        max(created_at) as last_order_date,
        count(distinct customer_id) as unique_customers
    from {{ source('magento', 'sales_order') }}
    where coupon_code is not null
    group by coupon_code
),

joined as (
    select
        c.coupon_id,
        c.rule_id,
        c.coupon_code,
        c.usage_limit,
        c.usage_per_customer,
        c.times_used,
        c.expiration_date,
        c.is_primary,
        c.coupon_type,
        c.created_at,

        r.promotion_name,
        r.discount_type,
        r.discount_amount,
        r.from_date,
        r.to_date,
        r.is_active as rule_is_active,

        os.order_count,
        os.total_order_value,
        os.total_discount_given,
        os.first_order_date,
        os.last_order_date,
        os.unique_customers

    from coupons c
    left join rules r on c.rule_id = r.rule_id
    left join order_stats os on c.coupon_code = os.coupon_code
)

select
    {{ dbt_utils.generate_surrogate_key(['coupon_id']) }} as coupon_usage_sk,
    coupon_id,
    rule_id,
    coupon_code,
    promotion_name,

    -- Usage statistics
    times_used,
    coalesce(order_count, 0) as order_count,
    coalesce(unique_customers, 0) as unique_customers,

    -- Limits
    usage_limit,
    usage_per_customer,
    case
        when usage_limit is not null then usage_limit - times_used
        else null
    end as remaining_uses,
    case
        when usage_limit is not null and usage_limit > 0
        then round(times_used / usage_limit * 100, 2)
        else null
    end as usage_rate_percent,

    -- Financial metrics
    coalesce(total_order_value, 0) as total_order_value,
    coalesce(total_discount_given, 0) as total_discount_given,
    case
        when coalesce(order_count, 0) > 0
        then round(total_order_value / order_count, 2)
        else 0
    end as avg_order_value,
    case
        when coalesce(order_count, 0) > 0
        then round(total_discount_given / order_count, 2)
        else 0
    end as avg_discount_per_order,
    case
        when coalesce(total_order_value, 0) > 0
        then round(total_discount_given / total_order_value * 100, 2)
        else 0
    end as discount_rate_percent,

    -- Discount info
    discount_type,
    case
        when discount_type = 'by_percent' then 'Percentage'
        when discount_type = 'by_fixed' then 'Fixed Amount'
        when discount_type = 'cart_fixed' then 'Cart Fixed'
        else discount_type
    end as discount_type_label,
    discount_amount,

    -- Dates
    created_at as coupon_created_at,
    first_order_date,
    last_order_date,
    expiration_date,
    from_date as promotion_start_date,
    to_date as promotion_end_date,

    -- Status
    case when is_primary = 1 then true else false end as is_primary,
    case when rule_is_active = 1 then true else false end as is_active,
    case
        when rule_is_active = 0 then 'Inactive'
        when expiration_date is not null and expiration_date < current_timestamp() then 'Expired'
        when usage_limit is not null and times_used >= usage_limit then 'Exhausted'
        else 'Active'
    end as coupon_status,

    -- Days analysis
    datediff('day', created_at, current_timestamp()) as days_since_created,
    case
        when first_order_date is not null
        then datediff('day', first_order_date, coalesce(last_order_date, current_timestamp()))
        else null
    end as active_usage_days

from joined
