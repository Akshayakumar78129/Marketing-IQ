{{
    config(
        materialized='table',
        tags=['facts', 'magento']
    )
}}

/*
    Magento Inventory Fact Table
    Grain: One row per product per stock
    Source: MAGENTO.CATALOGINVENTORY_STOCK_ITEM
*/

with inventory as (
    select
        item_id,
        product_id,
        stock_id,
        website_id,

        -- Quantity
        qty,
        min_qty,
        notify_stock_qty,
        min_sale_qty,
        max_sale_qty,
        qty_increments,

        -- Flags
        is_in_stock,
        manage_stock,
        backorders,
        is_qty_decimal,
        enable_qty_increments,
        is_decimal_divided,
        stock_status_changed_auto,

        -- Use config flags
        use_config_min_qty,
        use_config_backorders,
        use_config_min_sale_qty,
        use_config_max_sale_qty,
        use_config_notify_stock_qty,
        use_config_manage_stock,
        use_config_qty_increments,
        use_config_enable_qty_inc,

        -- Low stock
        low_stock_date

    from {{ source('magento', 'cataloginventory_stock_item') }}
)

select
    {{ dbt_utils.generate_surrogate_key(['item_id']) }} as inventory_sk,
    item_id,
    product_id,
    stock_id,
    website_id,

    -- Quantity
    qty as quantity_on_hand,
    min_qty as minimum_qty,
    notify_stock_qty as notify_at_qty,
    min_sale_qty,
    max_sale_qty,
    qty_increments,

    -- Stock status
    case when is_in_stock = 1 then true else false end as is_in_stock,
    case when manage_stock = 1 then true else false end as is_stock_managed,

    -- Backorders
    case
        when backorders = 0 then 'No Backorders'
        when backorders = 1 then 'Allow Qty Below 0'
        when backorders = 2 then 'Allow Qty Below 0 and Notify Customer'
        else 'Unknown'
    end as backorder_policy,
    case when backorders > 0 then true else false end as allows_backorders,

    -- Quantity type flags
    case when is_qty_decimal = 1 then true else false end as is_qty_decimal,
    case when enable_qty_increments = 1 then true else false end as uses_qty_increments,

    -- Use config flags
    case when use_config_min_qty = 1 then true else false end as uses_config_min_qty,
    case when use_config_backorders = 1 then true else false end as uses_config_backorders,
    case when use_config_manage_stock = 1 then true else false end as uses_config_manage_stock,

    -- Low stock info
    low_stock_date,
    case when low_stock_date is not null then true else false end as has_been_low_stock,

    -- Stock status segment
    case
        when is_in_stock = 0 then 'Out of Stock'
        when qty is null or qty <= 0 then 'Out of Stock'
        when qty <= coalesce(notify_stock_qty, min_qty, 0) then 'Low Stock'
        when qty <= 10 then 'Limited Stock'
        when qty <= 50 then 'Normal Stock'
        else 'High Stock'
    end as stock_status_segment,

    -- Days to sell out (if we had sales velocity, this would be calculated)
    case
        when qty is null or qty <= 0 then 0
        else qty
    end as available_qty

from inventory
