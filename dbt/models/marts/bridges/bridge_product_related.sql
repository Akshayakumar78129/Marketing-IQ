{{
    config(
        materialized='table',
        tags=['bridges', 'magento']
    )
}}

/*
    Magento Product Relationships Bridge Table
    Product relationships: related, upsell, cross-sell
    Source: MAGENTO.CATALOG_PRODUCT_LINK, MAGENTO.CATALOG_PRODUCT_LINK_TYPE
*/

with product_links as (
    select
        link_id,
        product_id,
        linked_product_id,
        link_type_id
    from {{ source('magento', 'catalog_product_link') }}
),

link_types as (
    select
        link_type_id,
        code as link_type_code
    from {{ source('magento', 'catalog_product_link_type') }}
),

joined as (
    select
        pl.link_id,
        pl.product_id,
        pl.linked_product_id,
        pl.link_type_id,
        lt.link_type_code
    from product_links pl
    left join link_types lt on pl.link_type_id = lt.link_type_id
)

select
    {{ dbt_utils.generate_surrogate_key(['link_id']) }} as product_link_sk,
    link_id,
    product_id,
    linked_product_id,
    link_type_id,

    -- Link type details
    link_type_code,
    case
        when link_type_code = 'relation' then 'Related Products'
        when link_type_code = 'up_sell' then 'Up-Sell Products'
        when link_type_code = 'cross_sell' then 'Cross-Sell Products'
        when link_type_code = 'super' then 'Grouped/Bundle Products'
        else initcap(replace(link_type_code, '_', ' '))
    end as link_type_label,

    -- Type flags
    case when link_type_code = 'relation' then true else false end as is_related,
    case when link_type_code = 'up_sell' then true else false end as is_upsell,
    case when link_type_code = 'cross_sell' then true else false end as is_crosssell

from joined
