{{
    config(
        materialized='incremental',
        unique_key='shipment_id',
        tags=['facts', 'magento']
    )
}}

/*
    Magento Shipment Fact Table
    Grain: One row per shipment
    Source: MAGENTO.SALES_SHIPMENT
*/

with shipments as (
    select
        entity_id as shipment_id,
        increment_id,
        order_id,
        customer_id,
        store_id,
        shipment_status,

        -- Dates
        created_at as shipment_date,
        updated_at,

        -- Totals
        total_qty,
        total_weight,

        -- Address IDs
        shipping_address_id,
        billing_address_id,

        -- Flags
        email_sent

    from {{ source('magento', 'sales_shipment') }}
    {% if is_incremental() %}
    where updated_at > (select max(updated_at) from {{ this }})
    {% endif %}
)

select
    {{ dbt_utils.generate_surrogate_key(['shipment_id']) }} as shipment_sk,
    shipment_id,
    increment_id,
    order_id,
    customer_id,
    store_id,

    -- Status
    shipment_status,

    -- Dates
    shipment_date,
    shipment_date::date as shipment_date_day,
    date_trunc('week', shipment_date)::date as shipment_date_week,
    date_trunc('month', shipment_date)::date as shipment_date_month,
    updated_at,

    -- Totals
    total_qty,
    total_weight,

    -- Address IDs
    shipping_address_id,
    billing_address_id,

    -- Flags
    case when email_sent = 1 then true else false end as email_sent

from shipments
