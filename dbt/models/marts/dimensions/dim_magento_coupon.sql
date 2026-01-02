{{
    config(
        materialized='table',
        tags=['dimensions', 'magento']
    )
}}

/*
    Magento Coupon Dimension
    Coupon codes linked to sales rules/promotions
    Source: MAGENTO.SALESRULE_COUPON, MAGENTO.SALESRULE
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
        discount_amount,
        simple_action as discount_type,
        is_active as rule_is_active
    from {{ source('magento', 'salesrule') }}
),

joined as (
    select
        c.*,
        r.promotion_name,
        r.discount_amount,
        r.discount_type,
        r.rule_is_active
    from coupons c
    left join rules r on c.rule_id = r.rule_id
)

select
    {{ dbt_utils.generate_surrogate_key(['coupon_id']) }} as coupon_sk,
    coupon_id,
    rule_id,
    coupon_code,
    promotion_name,

    -- Usage
    usage_limit,
    usage_per_customer,
    times_used,
    case
        when usage_limit is not null and usage_limit > 0
        then usage_limit - times_used
        else null
    end as remaining_uses,

    -- Expiration
    expiration_date,
    case
        when expiration_date is not null and expiration_date < current_timestamp()
        then true
        else false
    end as is_expired,

    -- Type flags
    case when is_primary = 1 then true else false end as is_primary,
    case
        when coupon_type = 0 then 'Manual'
        when coupon_type = 1 then 'Auto-Generated'
        else 'Unknown'
    end as coupon_type_label,

    -- Associated discount info
    discount_amount,
    case
        when discount_type = 'by_percent' then 'Percentage'
        when discount_type = 'by_fixed' then 'Fixed Amount'
        when discount_type = 'cart_fixed' then 'Cart Fixed'
        when discount_type = 'buy_x_get_y' then 'Buy X Get Y'
        else discount_type
    end as discount_type_label,

    -- Status
    case
        when rule_is_active = 0 then 'Inactive Rule'
        when expiration_date is not null and expiration_date < current_timestamp() then 'Expired'
        when usage_limit is not null and times_used >= usage_limit then 'Exhausted'
        else 'Active'
    end as coupon_status,

    -- Timestamps
    created_at,
    datediff('day', created_at, current_timestamp()) as days_since_created

from joined
