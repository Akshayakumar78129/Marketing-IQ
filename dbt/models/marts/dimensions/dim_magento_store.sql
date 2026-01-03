{{
    config(
        materialized='table',
        tags=['dimensions', 'magento']
    )
}}

/*
    Magento Store/Website Hierarchy Dimension
    Combines store, store_group, and store_website into a denormalized dimension
    Source: MAGENTO.STORE, MAGENTO.STORE_GROUP, MAGENTO.STORE_WEBSITE
*/

with stores as (
    select
        store_id,
        code as store_code,
        name as store_name,
        website_id,
        group_id as store_group_id,
        sort_order as store_sort_order,
        is_active
    from {{ source('magento', 'store') }}
),

store_groups as (
    select
        group_id,
        code as store_group_code,
        name as store_group_name,
        website_id,
        root_category_id,
        default_store_id
    from {{ source('magento', 'store_group') }}
),

websites as (
    select
        website_id,
        code as website_code,
        name as website_name,
        sort_order as website_sort_order,
        default_group_id,
        is_default as is_default_website
    from {{ source('magento', 'store_website') }}
),

joined as (
    select
        s.store_id,
        s.store_code,
        s.store_name,
        s.store_sort_order,
        s.is_active,

        -- Store Group attributes
        sg.group_id as store_group_id,
        sg.store_group_code,
        sg.store_group_name,
        sg.root_category_id,
        sg.default_store_id,
        case when sg.default_store_id = s.store_id then true else false end as is_default_store,

        -- Website attributes
        w.website_id,
        w.website_code,
        w.website_name,
        w.website_sort_order,
        w.default_group_id,
        w.is_default_website,
        case when w.default_group_id = sg.group_id then true else false end as is_default_store_group

    from stores s
    left join store_groups sg on s.store_group_id = sg.group_id
    left join websites w on sg.website_id = w.website_id
)

select
    {{ dbt_utils.generate_surrogate_key(['store_id']) }} as store_sk,
    store_id,
    store_code,
    store_name,
    store_sort_order,
    case when is_active = 1 then true else false end as is_active,

    -- Store Group
    store_group_id,
    store_group_code,
    store_group_name,
    root_category_id,
    is_default_store,

    -- Website
    website_id,
    website_code,
    website_name,
    website_sort_order,
    case when is_default_website = 1 then true else false end as is_default_website,
    is_default_store_group,

    -- Hierarchy path for easy filtering
    website_code || ' > ' || store_group_code || ' > ' || store_code as store_hierarchy_path

from joined
