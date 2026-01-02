{{
    config(
        materialized='incremental',
        unique_key='item_id',
        tags=['facts', 'magento']
    )
}}

/*
    Magento Order Item Fact Table
    Grain: One row per order line item
    Source: MAGENTO.SALES_ORDER_ITEM
*/

with order_items as (
    select
        item_id,
        order_id,
        parent_item_id,
        quote_item_id,
        store_id,
        product_id,
        product_type,
        sku,
        name as product_name,

        -- Quantities
        qty_ordered,
        qty_invoiced,
        qty_shipped,
        qty_refunded,
        qty_canceled,
        qty_backordered,

        -- Pricing (store currency)
        price,
        original_price,
        row_total,
        tax_amount,
        tax_percent,
        discount_amount,
        discount_percent,

        -- Pricing (base currency)
        base_price,
        base_original_price,
        base_row_total,
        base_tax_amount,
        base_discount_amount,

        -- Cost
        base_cost,

        -- Weight
        weight,
        row_weight,

        -- Flags
        is_virtual,
        is_qty_decimal,
        no_discount,
        free_shipping,

        -- Promotions
        applied_rule_ids,

        -- Timestamps
        created_at,
        updated_at

    from {{ source('magento', 'sales_order_item') }}
    {% if is_incremental() %}
    where updated_at > (select max(updated_at) from {{ this }})
    {% endif %}
)

select
    {{ dbt_utils.generate_surrogate_key(['item_id']) }} as order_item_sk,
    item_id,
    order_id,
    parent_item_id,
    quote_item_id,
    store_id,
    product_id,
    product_type,
    sku,
    product_name,

    -- Quantities
    qty_ordered,
    qty_invoiced,
    qty_shipped,
    qty_refunded,
    qty_canceled,
    qty_backordered,
    qty_ordered - coalesce(qty_canceled, 0) - coalesce(qty_refunded, 0) as net_qty,
    qty_ordered - coalesce(qty_shipped, 0) as qty_pending_shipment,

    -- Pricing (store currency)
    price as unit_price,
    original_price,
    row_total,
    tax_amount,
    tax_percent,
    coalesce(discount_amount, 0) as discount_amount,
    coalesce(discount_percent, 0) as discount_percent,
    row_total - coalesce(discount_amount, 0) + coalesce(tax_amount, 0) as row_total_incl_tax,

    -- Pricing (base currency)
    base_price as base_unit_price,
    base_original_price,
    base_row_total,
    base_tax_amount,
    coalesce(base_discount_amount, 0) as base_discount_amount,
    base_row_total - coalesce(base_discount_amount, 0) + coalesce(base_tax_amount, 0) as base_row_total_incl_tax,

    -- Margin calculation
    base_cost,
    case
        when base_cost is not null and base_cost > 0
        then base_row_total - (base_cost * qty_ordered)
        else null
    end as gross_margin,
    case
        when base_cost is not null and base_cost > 0 and base_row_total > 0
        then round((base_row_total - (base_cost * qty_ordered)) / base_row_total * 100, 2)
        else null
    end as gross_margin_percent,

    -- Weight
    weight as unit_weight,
    row_weight,

    -- Flags
    case when is_virtual = 1 then true else false end as is_virtual,
    case when is_qty_decimal = 1 then true else false end as is_qty_decimal,
    case when no_discount = 1 then true else false end as no_discount_applied,
    case when free_shipping = 1 then true else false end as has_free_shipping,

    -- Parent item flag (for configurable products)
    case when parent_item_id is null then true else false end as is_parent_item,

    -- Promotions
    applied_rule_ids,
    case when applied_rule_ids is not null then true else false end as has_promotion,

    -- Fulfillment status
    case
        when qty_canceled = qty_ordered then 'Canceled'
        when qty_refunded = qty_ordered then 'Refunded'
        when qty_shipped = qty_ordered then 'Shipped'
        when qty_shipped > 0 then 'Partially Shipped'
        when qty_invoiced = qty_ordered then 'Invoiced'
        when qty_invoiced > 0 then 'Partially Invoiced'
        else 'Pending'
    end as fulfillment_status,

    -- Timestamps
    created_at,
    updated_at

from order_items
