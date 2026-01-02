{{
    config(
        materialized='table',
        tags=['dimensions', 'magento']
    )
}}

/*
    Magento Promotion/Sales Rule Dimension
    Cart price rules and promotions
    Source: MAGENTO.SALESRULE
*/

with promotions as (
    select
        rule_id,
        name as promotion_name,
        description,
        from_date,
        to_date,
        is_active,
        uses_per_customer,
        uses_per_coupon,
        times_used,
        simple_action as discount_type,
        discount_amount,
        discount_qty,
        discount_step,
        apply_to_shipping,
        coupon_type,
        use_auto_generation,
        simple_free_shipping,
        stop_rules_processing,
        sort_order
    from {{ source('magento', 'salesrule') }}
)

select
    {{ dbt_utils.generate_surrogate_key(['rule_id']) }} as promotion_sk,
    rule_id,
    promotion_name,
    description,
    from_date,
    to_date,

    -- Discount details
    case
        when discount_type = 'by_percent' then 'Percent of product price discount'
        when discount_type = 'by_fixed' then 'Fixed amount discount'
        when discount_type = 'cart_fixed' then 'Fixed amount discount for whole cart'
        when discount_type = 'buy_x_get_y' then 'Buy X get Y free'
        else discount_type
    end as discount_type_label,
    discount_type as discount_type_code,
    discount_amount,
    discount_qty as max_qty_discount_applied_to,
    discount_step as discount_qty_step,

    -- Usage limits
    uses_per_customer,
    uses_per_coupon,
    times_used as total_times_used,

    -- Flags
    case when is_active = 1 then true else false end as is_active,
    case when apply_to_shipping = 1 then true else false end as applies_to_shipping,
    case when simple_free_shipping = 1 then true else false end as provides_free_shipping,
    case when stop_rules_processing = 1 then true else false end as stops_further_rules,

    -- Coupon type
    case
        when coupon_type = 1 then 'No Coupon'
        when coupon_type = 2 then 'Specific Coupon'
        when coupon_type = 3 then 'Auto'
        else 'Unknown'
    end as coupon_type_label,
    case when use_auto_generation = 1 then true else false end as uses_auto_generated_coupons,

    -- Derived status
    case
        when is_active = 0 then 'Inactive'
        when from_date > current_date() then 'Scheduled'
        when to_date is not null and to_date < current_date() then 'Expired'
        else 'Active'
    end as promotion_status,

    -- Validity period
    datediff('day', from_date, coalesce(to_date, current_date())) as validity_days,
    case when to_date is null then true else false end as is_indefinite,

    sort_order as priority

from promotions
