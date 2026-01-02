{{
    config(
        materialized='incremental',
        unique_key='invoice_id',
        tags=['facts', 'magento']
    )
}}

/*
    Magento Invoice Fact Table
    Grain: One row per invoice
    Source: MAGENTO.SALES_INVOICE
*/

with invoices as (
    select
        entity_id as invoice_id,
        increment_id,
        order_id,
        store_id,
        state,

        -- Dates
        created_at as invoice_date,
        updated_at,

        -- Financials (store currency)
        subtotal,
        tax_amount,
        shipping_amount,
        shipping_tax_amount,
        discount_amount,
        grand_total,

        -- Financials (base currency)
        base_subtotal,
        base_tax_amount,
        base_shipping_amount,
        base_shipping_tax_amount,
        base_discount_amount,
        base_grand_total,

        -- Refunded from this invoice
        base_total_refunded,

        -- Quantity
        total_qty,

        -- Currency
        order_currency_code,
        base_currency_code,
        store_currency_code,

        -- Address IDs
        billing_address_id,
        shipping_address_id,

        -- Flags
        email_sent,
        can_void_flag,
        is_used_for_refund

    from {{ source('magento', 'sales_invoice') }}
    {% if is_incremental() %}
    where updated_at > (select max(updated_at) from {{ this }})
    {% endif %}
)

select
    {{ dbt_utils.generate_surrogate_key(['invoice_id']) }} as invoice_sk,
    invoice_id,
    increment_id,
    order_id,
    store_id,

    -- State
    state,
    case
        when state = 1 then 'Open'
        when state = 2 then 'Paid'
        when state = 3 then 'Canceled'
        else 'Unknown'
    end as state_label,

    -- Dates
    invoice_date,
    invoice_date::date as invoice_date_day,
    date_trunc('month', invoice_date)::date as invoice_date_month,
    updated_at,

    -- Financials (store currency)
    subtotal,
    tax_amount,
    shipping_amount,
    shipping_tax_amount,
    coalesce(discount_amount, 0) as discount_amount,
    grand_total,

    -- Financials (base currency)
    base_subtotal,
    base_tax_amount,
    base_shipping_amount,
    base_shipping_tax_amount,
    coalesce(base_discount_amount, 0) as base_discount_amount,
    base_grand_total,

    -- Net after refunds
    coalesce(base_total_refunded, 0) as base_total_refunded,
    base_grand_total - coalesce(base_total_refunded, 0) as net_invoiced,

    -- Quantity
    total_qty,

    -- Currency
    order_currency_code,
    base_currency_code,

    -- Flags
    case when email_sent = 1 then true else false end as email_sent,
    case when can_void_flag = 1 then true else false end as can_void,
    case when is_used_for_refund = 1 then true else false end as has_refund

from invoices
