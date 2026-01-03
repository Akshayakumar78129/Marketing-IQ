{{
    config(
        materialized='table',
        tags=['dimensions', 'magento']
    )
}}

/*
    Magento Shipping Method Dimension
    Derived from distinct shipping methods used in orders
    Source: MAGENTO.SALES_ORDER
*/

with shipping_methods as (
    select distinct
        shipping_method,
        shipping_description
    from {{ source('magento', 'sales_order') }}
    where shipping_method is not null
),

shipping_method_parsed as (
    select
        shipping_method,
        shipping_description,

        -- Parse carrier code (part before underscore)
        case
            when shipping_method like '%\\_%' escape '\\'
            then split_part(shipping_method, '_', 1)
            else shipping_method
        end as carrier_code,

        -- Parse method code (part after underscore)
        case
            when shipping_method like '%\\_%' escape '\\'
            then substring(shipping_method, position('_' in shipping_method) + 1)
            else shipping_method
        end as method_code

    from shipping_methods
),

shipping_method_labels as (
    select
        shipping_method,
        shipping_description,
        carrier_code,
        method_code,

        -- Create carrier label
        case
            when carrier_code = 'flatrate' then 'Flat Rate'
            when carrier_code = 'freeshipping' then 'Free Shipping'
            when carrier_code = 'tablerate' then 'Table Rate'
            when carrier_code = 'ups' then 'UPS'
            when carrier_code = 'usps' then 'USPS'
            when carrier_code = 'fedex' then 'FedEx'
            when carrier_code = 'dhl' then 'DHL'
            when carrier_code = 'instore' then 'In-Store Pickup'
            else initcap(replace(carrier_code, '_', ' '))
        end as carrier_name,

        -- Is free shipping
        case
            when carrier_code = 'freeshipping' or shipping_description ilike '%free%'
            then true
            else false
        end as is_free_shipping,

        -- Is store pickup
        case
            when carrier_code = 'instore' or shipping_description ilike '%pickup%'
            then true
            else false
        end as is_store_pickup,

        -- Shipping speed category
        case
            when method_code ilike '%overnight%' or method_code ilike '%express%' or method_code ilike '%priority%'
            then 'Express'
            when method_code ilike '%ground%' or method_code ilike '%standard%'
            then 'Standard'
            when carrier_code = 'freeshipping'
            then 'Economy'
            else 'Standard'
        end as shipping_speed

    from shipping_method_parsed
)

select
    {{ dbt_utils.generate_surrogate_key(['shipping_method']) }} as shipping_method_sk,
    shipping_method,
    coalesce(shipping_description, carrier_name) as shipping_description,
    carrier_code,
    carrier_name,
    method_code,
    is_free_shipping,
    is_store_pickup,
    shipping_speed
from shipping_method_labels
