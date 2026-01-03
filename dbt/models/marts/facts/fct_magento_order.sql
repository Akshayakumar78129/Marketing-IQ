{{
    config(
        materialized='incremental',
        unique_key='order_id',
        tags=['facts', 'magento']
    )
}}

/*
    Magento Order Fact Table
    Grain: One row per order
    Source: MAGENTO.SALES_ORDER, MAGENTO.SALES_ORDER_PAYMENT
*/

with orders as (
    select
        entity_id as order_id,
        increment_id,
        store_id,
        customer_id,
        customer_group_id,
        customer_email,
        customer_firstname,
        customer_lastname,
        customer_is_guest,

        -- Status
        state,
        status,

        -- Dates
        created_at as order_date,
        updated_at,

        -- Address IDs
        billing_address_id,
        shipping_address_id,

        -- Quote reference
        quote_id,

        -- Financials (store currency)
        subtotal,
        tax_amount,
        shipping_amount,
        discount_amount,
        grand_total,

        -- Financials (base currency)
        base_subtotal,
        base_tax_amount,
        base_shipping_amount,
        base_discount_amount,
        base_grand_total,

        -- Quantity
        total_qty_ordered,
        total_item_count,

        -- Shipping
        shipping_method,
        shipping_description,
        weight,
        is_virtual,

        -- Coupon/Promotions
        coupon_code,
        applied_rule_ids,
        coupon_rule_name,

        -- Currency
        order_currency_code,
        base_currency_code,
        store_currency_code,

        -- Invoiced/Paid/Refunded
        base_total_invoiced,
        base_total_paid,
        base_total_refunded,
        total_invoiced,
        total_paid,
        total_refunded

    from {{ source('magento', 'sales_order') }}
    {% if is_incremental() %}
    where updated_at > (select max(updated_at) from {{ this }})
    {% endif %}
),

-- Get payment method from sales_order_payment
payments as (
    select
        parent_id as order_id,
        method as payment_method,
        cc_type as credit_card_type,
        amount_paid,
        amount_ordered
    from {{ source('magento', 'sales_order_payment') }}
)

select
    {{ dbt_utils.generate_surrogate_key(['o.order_id']) }} as order_sk,
    o.order_id,
    o.increment_id,
    o.store_id,
    o.customer_id,
    o.customer_group_id,
    o.customer_email,
    o.customer_firstname || ' ' || o.customer_lastname as customer_full_name,
    case when o.customer_is_guest = 1 then true else false end as is_guest_order,
    o.quote_id,

    -- Status
    o.state,
    o.status,

    -- Dates
    o.order_date,
    o.order_date::date as order_date_day,
    date_trunc('week', o.order_date)::date as order_date_week,
    date_trunc('month', o.order_date)::date as order_date_month,
    o.updated_at,

    -- Financials (store currency)
    o.subtotal,
    o.tax_amount,
    o.shipping_amount,
    coalesce(o.discount_amount, 0) as discount_amount,
    o.grand_total,

    -- Financials (base currency)
    o.base_subtotal,
    o.base_tax_amount,
    o.base_shipping_amount,
    coalesce(o.base_discount_amount, 0) as base_discount_amount,
    o.base_grand_total,

    -- Invoiced/Paid/Refunded
    coalesce(o.base_total_invoiced, 0) as base_total_invoiced,
    coalesce(o.base_total_paid, 0) as base_total_paid,
    coalesce(o.base_total_refunded, 0) as base_total_refunded,
    o.base_grand_total - coalesce(o.base_total_refunded, 0) as net_revenue,

    -- Quantity
    o.total_qty_ordered,
    o.total_item_count,

    -- Shipping
    o.shipping_method,
    o.shipping_description,
    o.weight as total_weight,
    case when o.is_virtual = 1 then true else false end as is_virtual_order,

    -- Payment
    p.payment_method,
    p.credit_card_type,

    -- Coupon/Promotions
    o.coupon_code,
    o.applied_rule_ids,
    o.coupon_rule_name,
    case when o.coupon_code is not null then true else false end as has_coupon,
    case when o.discount_amount is not null and o.discount_amount != 0 then true else false end as has_discount,

    -- Currency
    o.order_currency_code,
    o.base_currency_code,

    -- Address IDs for joining
    o.billing_address_id,
    o.shipping_address_id,

    -- Derived metrics
    case
        when o.base_grand_total < 50 then 'Under $50'
        when o.base_grand_total < 100 then '$50-$100'
        when o.base_grand_total < 250 then '$100-$250'
        when o.base_grand_total < 500 then '$250-$500'
        else '$500+'
    end as order_value_segment,

    -- Average item value
    case when o.total_item_count > 0
        then o.base_grand_total / o.total_item_count
        else 0
    end as avg_item_value

from orders o
left join payments p on o.order_id = p.order_id
