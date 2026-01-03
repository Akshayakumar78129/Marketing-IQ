{{
    config(
        materialized='table',
        tags=['dimensions', 'magento']
    )
}}

/*
    Magento Customer Group Dimension
    Customer segmentation/tier reference table
    Source: MAGENTO.CUSTOMER_GROUP
*/

with customer_groups as (
    select
        customer_group_id,
        customer_group_code,
        tax_class_id
    from {{ source('magento', 'customer_group') }}
)

select
    {{ dbt_utils.generate_surrogate_key(['customer_group_id']) }} as customer_group_sk,
    customer_group_id,
    customer_group_code,
    tax_class_id,

    -- Derived flags for common group types
    case
        when lower(customer_group_code) like '%guest%' or customer_group_id = 0 then true
        else false
    end as is_guest_group,
    case
        when lower(customer_group_code) like '%wholesale%' then true
        else false
    end as is_wholesale_group,
    case
        when lower(customer_group_code) like '%retail%' or lower(customer_group_code) like '%general%' then true
        else false
    end as is_retail_group

from customer_groups
