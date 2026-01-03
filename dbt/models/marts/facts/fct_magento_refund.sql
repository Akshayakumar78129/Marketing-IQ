{{
    config(
        materialized='incremental',
        unique_key='creditmemo_id',
        tags=['facts', 'magento']
    )
}}

/*
    Magento Refund (Credit Memo) Fact Table
    Grain: One row per credit memo
    Source: MAGENTO.SALES_CREDITMEMO
*/

with creditmemos as (
    select
        entity_id as creditmemo_id,
        increment_id,
        order_id,
        invoice_id,
        store_id,
        state,
        creditmemo_status,

        -- Dates
        created_at as refund_date,
        updated_at,

        -- Financials (store currency)
        subtotal,
        tax_amount,
        shipping_amount,
        shipping_tax_amount,
        discount_amount,
        grand_total,
        adjustment_positive,
        adjustment_negative,
        adjustment,

        -- Financials (base currency)
        base_subtotal,
        base_tax_amount,
        base_shipping_amount,
        base_shipping_tax_amount,
        base_discount_amount,
        base_grand_total,
        base_adjustment_positive,
        base_adjustment_negative,
        base_adjustment,

        -- Currency
        order_currency_code,
        base_currency_code,
        store_currency_code,

        -- Address IDs
        billing_address_id,
        shipping_address_id,

        -- Flags
        email_sent

    from {{ source('magento', 'sales_creditmemo') }}
    {% if is_incremental() %}
    where updated_at > (select max(updated_at) from {{ this }})
    {% endif %}
)

select
    {{ dbt_utils.generate_surrogate_key(['creditmemo_id']) }} as refund_sk,
    creditmemo_id,
    increment_id,
    order_id,
    invoice_id,
    store_id,

    -- State
    state,
    case
        when state = 1 then 'Open'
        when state = 2 then 'Refunded'
        when state = 3 then 'Canceled'
        else 'Unknown'
    end as state_label,
    creditmemo_status,

    -- Dates
    refund_date,
    refund_date::date as refund_date_day,
    date_trunc('month', refund_date)::date as refund_date_month,
    updated_at,

    -- Financials (store currency)
    subtotal,
    tax_amount,
    shipping_amount,
    shipping_tax_amount,
    coalesce(discount_amount, 0) as discount_amount,
    grand_total,

    -- Adjustments
    coalesce(adjustment_positive, 0) as adjustment_positive,
    coalesce(adjustment_negative, 0) as adjustment_negative,
    coalesce(adjustment, 0) as net_adjustment,

    -- Financials (base currency)
    base_subtotal,
    base_tax_amount,
    base_shipping_amount,
    coalesce(base_discount_amount, 0) as base_discount_amount,
    base_grand_total,
    coalesce(base_adjustment_positive, 0) as base_adjustment_positive,
    coalesce(base_adjustment_negative, 0) as base_adjustment_negative,

    -- Currency
    order_currency_code,
    base_currency_code,

    -- Flags
    case when email_sent = 1 then true else false end as email_sent,
    case when invoice_id is not null then true else false end as has_invoice_reference

from creditmemos
