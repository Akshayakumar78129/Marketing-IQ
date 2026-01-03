{{
    config(
        materialized='table',
        tags=['dimensions', 'magento']
    )
}}

/*
    Magento Category Dimension (Hierarchical)
    Flattens EAV attributes and provides hierarchy levels
    Source: MAGENTO.CATALOG_CATEGORY_ENTITY, MAGENTO.CATALOG_CATEGORY_ENTITY_VARCHAR, MAGENTO.CATALOG_CATEGORY_ENTITY_INT
*/

-- Step 1: Get attribute IDs dynamically for category entity type (entity_type_id = 3)
with attribute_mapping as (
    select attribute_id, attribute_code
    from {{ source('magento', 'eav_attribute') }}
    where entity_type_id = 3  -- catalog_category
    and attribute_code in ('name', 'url_key', 'url_path', 'meta_title', 'meta_description', 'is_active', 'include_in_menu', 'is_anchor', 'description')
),

-- Step 2: Category base entity
categories as (
    select
        entity_id as category_id,
        attribute_set_id,
        parent_id,
        path,
        position,
        level,
        children_count,
        created_at,
        updated_at
    from {{ source('magento', 'catalog_category_entity') }}
),

-- Step 3: Varchar attributes with store override (store-specific first, then global)
category_varchar_ranked as (
    select
        cv.entity_id,
        am.attribute_code,
        cv.value,
        row_number() over (
            partition by cv.entity_id, cv.attribute_id
            order by case when cv.store_id = 1 then 1 when cv.store_id = 0 then 2 else 3 end
        ) as rn
    from {{ source('magento', 'catalog_category_entity_varchar') }} cv
    inner join attribute_mapping am on cv.attribute_id = am.attribute_id
    where cv.store_id in (0, 1)
),

category_varchar as (
    select
        entity_id,
        max(case when attribute_code = 'name' then value end) as category_name,
        max(case when attribute_code = 'url_key' then value end) as url_key,
        max(case when attribute_code = 'url_path' then value end) as url_path,
        max(case when attribute_code = 'meta_title' then value end) as meta_title,
        max(case when attribute_code = 'meta_description' then value end) as meta_description
    from category_varchar_ranked
    where rn = 1
    group by entity_id
),

-- Step 4: Int attributes with store override
category_int_ranked as (
    select
        ci.entity_id,
        am.attribute_code,
        ci.value,
        row_number() over (
            partition by ci.entity_id, ci.attribute_id
            order by case when ci.store_id = 1 then 1 when ci.store_id = 0 then 2 else 3 end
        ) as rn
    from {{ source('magento', 'catalog_category_entity_int') }} ci
    inner join attribute_mapping am on ci.attribute_id = am.attribute_id
    where ci.store_id in (0, 1)
),

category_int as (
    select
        entity_id,
        max(case when attribute_code = 'is_active' then value end) as is_active,
        max(case when attribute_code = 'include_in_menu' then value end) as include_in_menu,
        max(case when attribute_code = 'is_anchor' then value end) as is_anchor
    from category_int_ranked
    where rn = 1
    group by entity_id
),

-- Step 5: Build hierarchy lookups for path levels
-- Path format: "1/2/4/10" where each number is a category_id
category_names as (
    select category_id, category_name
    from categories c
    left join category_varchar cv on c.category_id = cv.entity_id
),

-- Step 6: Join everything together
joined as (
    select
        c.category_id,
        c.attribute_set_id,
        c.parent_id,
        c.path,
        c.position,
        c.level,
        c.children_count,
        c.created_at,
        c.updated_at,

        -- Varchar attributes
        cv.category_name,
        cv.url_key,
        cv.url_path,
        cv.meta_title,
        cv.meta_description,

        -- Int attributes
        ci.is_active,
        ci.include_in_menu,
        ci.is_anchor,

        -- Extract level IDs from path
        split_part(c.path, '/', 1)::number as level_0_id,
        split_part(c.path, '/', 2)::number as level_1_id,
        split_part(c.path, '/', 3)::number as level_2_id,
        split_part(c.path, '/', 4)::number as level_3_id,
        split_part(c.path, '/', 5)::number as level_4_id

    from categories c
    left join category_varchar cv on c.category_id = cv.entity_id
    left join category_int ci on c.category_id = ci.entity_id
),

-- Step 7: Get names for each level
final as (
    select
        j.*,
        l1.category_name as level_1_category,
        l2.category_name as level_2_category,
        l3.category_name as level_3_category,
        l4.category_name as level_4_category
    from joined j
    left join category_names l1 on j.level_1_id = l1.category_id
    left join category_names l2 on j.level_2_id = l2.category_id
    left join category_names l3 on j.level_3_id = l3.category_id
    left join category_names l4 on j.level_4_id = l4.category_id
)

select
    {{ dbt_utils.generate_surrogate_key(['category_id']) }} as category_sk,
    category_id,
    category_name,
    parent_id,
    path,
    position,
    level,
    children_count,
    url_key,
    url_path,
    meta_title,
    meta_description,

    -- Boolean conversions
    case when is_active = 1 then true else false end as is_active,
    case when include_in_menu = 1 then true else false end as include_in_menu,
    case when is_anchor = 1 then true else false end as is_anchor,

    -- Flattened hierarchy
    level_1_category,
    level_2_category,
    level_3_category,
    level_4_category,

    -- Full breadcrumb path
    coalesce(level_1_category, '') ||
        case when level_2_category is not null then ' > ' || level_2_category else '' end ||
        case when level_3_category is not null then ' > ' || level_3_category else '' end ||
        case when level_4_category is not null then ' > ' || level_4_category else '' end
    as category_breadcrumb,

    -- Flags
    case when level = 1 then true else false end as is_root_category,
    case when children_count = 0 then true else false end as is_leaf_category,

    created_at,
    updated_at

from final
