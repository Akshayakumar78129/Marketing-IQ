{{
    config(
        materialized='incremental',
        unique_key='item_id',
        tags=['facts', 'magento']
    )
}}

/*
    Magento Quote Item Fact Table
    Grain: One row per quote/cart line item
    Source: MAGENTO.QUOTE_ITEM
*/

with quote_items as (
    select
        item_id,
        quote_id,
        parent_item_id,
        product_id,
        store_id,
        product_type,
        sku,
        name as product_name,

        -- Quantity
        qty,

        -- Pricing (store currency)
        price,
        custom_price,
        row_total,
        row_total_with_discount,
        tax_amount,
        tax_percent,
        discount_amount,
        discount_percent,

        -- Pricing (base currency)
        base_price,
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

    from {{ source('magento', 'quote_item') }}
    {% if is_incremental() %}
    where updated_at > (select max(updated_at) from {{ this }})
    {% endif %}
)

select
    {{ dbt_utils.generate_surrogate_key(['item_id']) }} as quote_item_sk,
    item_id,
    quote_id,
    parent_item_id,
    product_id,
    store_id,
    product_type,
    sku,
    product_name,

    -- Quantity
    qty,

    -- Pricing (store currency)
    price as unit_price,
    custom_price,
    row_total,
    row_total_with_discount,
    tax_amount,
    tax_percent,
    coalesce(discount_amount, 0) as discount_amount,
    coalesce(discount_percent, 0) as discount_percent,

    -- Pricing (base currency)
    base_price as base_unit_price,
    base_row_total,
    base_tax_amount,
    coalesce(base_discount_amount, 0) as base_discount_amount,

    -- Cost and margin
    base_cost,
    case
        when base_cost is not null and base_cost > 0
        then base_row_total - (base_cost * qty)
        else null
    end as potential_margin,

    -- Weight
    weight as unit_weight,
    row_weight,

    -- Flags
    case when is_virtual = 1 then true else false end as is_virtual,
    case when is_qty_decimal = 1 then true else false end as is_qty_decimal,
    case when no_discount = 1 then true else false end as no_discount_applied,
    case when free_shipping = 1 then true else false end as has_free_shipping,

    -- Parent item flag
    case when parent_item_id is null then true else false end as is_parent_item,

    -- Promotions
    applied_rule_ids,
    case when applied_rule_ids is not null then true else false end as has_promotion,

    -- Timestamps
    created_at,
    updated_at

from quote_items
