{{
    config(
        materialized='table',
        tags=['dimensions', 'magento']
    )
}}

/*
    Magento Product Dimension
    Flattened product with key EAV attributes using dynamic attribute lookup
    Source: MAGENTO.CATALOG_PRODUCT_ENTITY, MAGENTO.CATALOG_PRODUCT_ENTITY_*, MAGENTO.EAV_ATTRIBUTE
*/

-- Step 1: Get attribute IDs dynamically for product entity type (entity_type_id = 4)
with attribute_mapping as (
    select attribute_id, attribute_code, backend_type
    from {{ source('magento', 'eav_attribute') }}
    where entity_type_id = 4  -- catalog_product
    and attribute_code in (
        -- Varchar attributes
        'name', 'url_key', 'url_path', 'meta_title', 'meta_description', 'meta_keyword', 'image', 'small_image', 'thumbnail',
        -- Decimal attributes
        'price', 'special_price', 'cost', 'weight', 'minimal_price',
        -- Int attributes
        'status', 'visibility', 'tax_class_id', 'quantity_and_stock_status'
    )
),

-- Step 2: Product base entity
products as (
    select
        entity_id as product_id,
        attribute_set_id,
        type_id as product_type,
        sku,
        has_options,
        required_options,
        created_at,
        updated_at
    from {{ source('magento', 'catalog_product_entity') }}
),

-- Step 3: Varchar attributes with store override (store-specific first, then global)
product_varchar_ranked as (
    select
        pv.entity_id,
        am.attribute_code,
        pv.value,
        row_number() over (
            partition by pv.entity_id, pv.attribute_id
            order by case when pv.store_id = 1 then 1 when pv.store_id = 0 then 2 else 3 end
        ) as rn
    from {{ source('magento', 'catalog_product_entity_varchar') }} pv
    inner join attribute_mapping am on pv.attribute_id = am.attribute_id
    where pv.store_id in (0, 1)
),

product_varchar as (
    select
        entity_id,
        max(case when attribute_code = 'name' then value end) as product_name,
        max(case when attribute_code = 'url_key' then value end) as url_key,
        max(case when attribute_code = 'url_path' then value end) as url_path,
        max(case when attribute_code = 'meta_title' then value end) as meta_title,
        max(case when attribute_code = 'meta_description' then value end) as meta_description,
        max(case when attribute_code = 'meta_keyword' then value end) as meta_keyword,
        max(case when attribute_code = 'image' then value end) as image,
        max(case when attribute_code = 'small_image' then value end) as small_image,
        max(case when attribute_code = 'thumbnail' then value end) as thumbnail
    from product_varchar_ranked
    where rn = 1
    group by entity_id
),

-- Step 4: Decimal attributes with store override
product_decimal_ranked as (
    select
        pd.entity_id,
        am.attribute_code,
        pd.value,
        row_number() over (
            partition by pd.entity_id, pd.attribute_id
            order by case when pd.store_id = 1 then 1 when pd.store_id = 0 then 2 else 3 end
        ) as rn
    from {{ source('magento', 'catalog_product_entity_decimal') }} pd
    inner join attribute_mapping am on pd.attribute_id = am.attribute_id
    where pd.store_id in (0, 1)
),

product_decimal as (
    select
        entity_id,
        max(case when attribute_code = 'price' then value end) as price,
        max(case when attribute_code = 'special_price' then value end) as special_price,
        max(case when attribute_code = 'cost' then value end) as cost,
        max(case when attribute_code = 'weight' then value end) as weight,
        max(case when attribute_code = 'minimal_price' then value end) as minimal_price
    from product_decimal_ranked
    where rn = 1
    group by entity_id
),

-- Step 5: Int attributes with store override
product_int_ranked as (
    select
        pi.entity_id,
        am.attribute_code,
        pi.value,
        row_number() over (
            partition by pi.entity_id, pi.attribute_id
            order by case when pi.store_id = 1 then 1 when pi.store_id = 0 then 2 else 3 end
        ) as rn
    from {{ source('magento', 'catalog_product_entity_int') }} pi
    inner join attribute_mapping am on pi.attribute_id = am.attribute_id
    where pi.store_id in (0, 1)
),

product_int as (
    select
        entity_id,
        max(case when attribute_code = 'status' then value end) as status,
        max(case when attribute_code = 'visibility' then value end) as visibility,
        max(case when attribute_code = 'tax_class_id' then value end) as tax_class_id,
        max(case when attribute_code = 'quantity_and_stock_status' then value end) as quantity_and_stock_status
    from product_int_ranked
    where rn = 1
    group by entity_id
),

-- Step 6: Join everything together
joined as (
    select
        p.product_id,
        p.attribute_set_id,
        p.product_type,
        p.sku,
        p.has_options,
        p.required_options,
        p.created_at,
        p.updated_at,

        -- Varchar attributes
        pv.product_name,
        pv.url_key,
        pv.url_path,
        pv.meta_title,
        pv.meta_description,
        pv.meta_keyword,
        pv.image,
        pv.small_image,
        pv.thumbnail,

        -- Decimal attributes
        pd.price,
        pd.special_price,
        pd.cost,
        pd.weight,
        pd.minimal_price,

        -- Int attributes
        pi.status,
        pi.visibility,
        pi.tax_class_id,
        pi.quantity_and_stock_status

    from products p
    left join product_varchar pv on p.product_id = pv.entity_id
    left join product_decimal pd on p.product_id = pd.entity_id
    left join product_int pi on p.product_id = pi.entity_id
)

select
    {{ dbt_utils.generate_surrogate_key(['product_id']) }} as product_sk,
    product_id,
    sku,
    product_name,
    product_type,
    attribute_set_id,

    -- Pricing
    price,
    special_price,
    cost,
    coalesce(special_price, price) as effective_price,
    case
        when special_price is not null and price is not null and price > 0
        then round((price - special_price) / price * 100, 2)
        else 0
    end as discount_percent,
    minimal_price,

    -- Physical attributes
    weight,

    -- Status fields
    case
        when status = 1 then 'Enabled'
        when status = 2 then 'Disabled'
        else 'Unknown'
    end as status,
    case when status = 1 then true else false end as is_enabled,

    case
        when visibility = 1 then 'Not Visible Individually'
        when visibility = 2 then 'Catalog'
        when visibility = 3 then 'Search'
        when visibility = 4 then 'Catalog, Search'
        else 'Unknown'
    end as visibility,
    case when visibility = 4 then true else false end as is_visible_in_catalog_and_search,

    tax_class_id,
    case when quantity_and_stock_status = 1 then true else false end as is_in_stock,

    -- Product type flags
    case when product_type = 'simple' then true else false end as is_simple,
    case when product_type = 'configurable' then true else false end as is_configurable,
    case when product_type = 'bundle' then true else false end as is_bundle,
    case when product_type = 'grouped' then true else false end as is_grouped,
    case when product_type = 'virtual' then true else false end as is_virtual,
    case when product_type = 'downloadable' then true else false end as is_downloadable,

    -- Options flags
    case when has_options = 1 then true else false end as has_options,
    case when required_options = 1 then true else false end as has_required_options,

    -- SEO/URL
    url_key,
    url_path,
    meta_title,
    meta_description,
    meta_keyword,

    -- Images
    image,
    small_image,
    thumbnail,

    -- Timestamps
    created_at,
    updated_at,

    -- Price tier segmentation
    case
        when price is null then 'No Price'
        when price < 10 then 'Under $10'
        when price < 25 then '$10-$25'
        when price < 50 then '$25-$50'
        when price < 100 then '$50-$100'
        when price < 250 then '$100-$250'
        else '$250+'
    end as price_tier_segment

from joined
