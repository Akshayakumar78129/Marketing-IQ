{{
    config(
        materialized='incremental',
        unique_key='quote_id',
        tags=['facts', 'magento']
    )
}}

/*
    Magento Quote (Abandoned Cart) Fact Table
    Grain: One row per quote/cart
    Source: MAGENTO.QUOTE
*/

with quotes as (
    select
        entity_id as quote_id,
        store_id,
        customer_id,
        customer_email,
        customer_group_id,
        customer_firstname,
        customer_lastname,
        customer_is_guest,

        -- Dates
        created_at,
        updated_at,
        converted_at,

        -- Status
        is_active,
        is_virtual,
        is_multi_shipping,
        is_persistent,

        -- Items
        items_count,
        items_qty,

        -- Financials
        subtotal,
        base_subtotal,
        subtotal_with_discount,
        base_subtotal_with_discount,
        grand_total,
        base_grand_total,

        -- Coupon/Promotions
        coupon_code,
        applied_rule_ids,

        -- Currency
        quote_currency_code,
        base_currency_code,
        store_currency_code,

        -- Checkout method
        checkout_method,

        -- Reserved order ID (if converted)
        reserved_order_id

    from {{ source('magento', 'quote') }}
    {% if is_incremental() %}
    where updated_at > (select max(updated_at) from {{ this }})
    {% endif %}
)

select
    {{ dbt_utils.generate_surrogate_key(['quote_id']) }} as quote_sk,
    quote_id,
    store_id,
    customer_id,
    customer_email,
    customer_group_id,
    customer_firstname || ' ' || customer_lastname as customer_full_name,
    case when customer_is_guest = 1 then true else false end as is_guest,

    -- Dates
    created_at,
    updated_at,
    converted_at,
    created_at::date as quote_date,

    -- Status flags
    case when is_active = 1 then true else false end as is_active,
    case when is_virtual = 1 then true else false end as is_virtual,
    case when is_multi_shipping = 1 then true else false end as is_multi_shipping,
    case when is_persistent = 1 then true else false end as is_persistent,

    -- Conversion status
    case when converted_at is not null then true else false end as is_converted,
    reserved_order_id,

    -- Items
    items_count,
    items_qty,

    -- Financials (store currency)
    subtotal,
    subtotal_with_discount,
    grand_total,
    coalesce(subtotal, 0) - coalesce(subtotal_with_discount, 0) as discount_amount,

    -- Financials (base currency)
    base_subtotal,
    base_subtotal_with_discount,
    base_grand_total,

    -- Coupon/Promotions
    coupon_code,
    applied_rule_ids,
    case when coupon_code is not null then true else false end as has_coupon,

    -- Currency
    quote_currency_code,
    base_currency_code,

    -- Checkout method
    checkout_method,

    -- Abandonment analysis
    case
        when converted_at is not null then 'Converted'
        when is_active = 1 and datediff('hour', updated_at, current_timestamp()) < 1 then 'Active'
        when is_active = 1 and datediff('hour', updated_at, current_timestamp()) < 24 then 'Recent'
        when is_active = 0 then 'Inactive'
        else 'Abandoned'
    end as cart_status,

    datediff('hour', updated_at, current_timestamp()) as hours_since_update,
    datediff('day', created_at, coalesce(converted_at, current_timestamp())) as days_to_convert,

    -- Cart value segment
    case
        when base_grand_total is null or base_grand_total = 0 then 'Empty'
        when base_grand_total < 50 then 'Under $50'
        when base_grand_total < 100 then '$50-$100'
        when base_grand_total < 250 then '$100-$250'
        else '$250+'
    end as cart_value_segment

from quotes
