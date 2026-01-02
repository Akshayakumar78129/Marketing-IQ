{{
    config(
        materialized='table',
        tags=['bridges', 'magento']
    )
}}

/*
    Magento Product-Category Bridge Table
    Many-to-many relationship between products and categories
    Source: MAGENTO.CATALOG_CATEGORY_PRODUCT
*/

with product_categories as (
    select
        entity_id,
        product_id,
        category_id,
        position
    from {{ source('magento', 'catalog_category_product') }}
),

-- Determine primary category (lowest position = primary)
ranked_categories as (
    select
        product_id,
        category_id,
        position,
        row_number() over (
            partition by product_id
            order by position asc
        ) as category_rank
    from product_categories
)

select
    {{ dbt_utils.generate_surrogate_key(['product_id', 'category_id']) }} as product_category_sk,
    product_id,
    category_id,
    position,
    case when category_rank = 1 then true else false end as is_primary_category,
    category_rank

from ranked_categories
