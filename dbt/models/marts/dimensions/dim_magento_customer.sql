{{
    config(
        materialized='table',
        tags=['dimensions', 'magento']
    )
}}

/*
    Magento Customer Dimension
    Flattened customer with EAV attributes and denormalized addresses
    Source: MAGENTO.CUSTOMER_ENTITY, MAGENTO.CUSTOMER_ENTITY_VARCHAR, MAGENTO.CUSTOMER_ADDRESS_ENTITY
*/

with customers as (
    select
        entity_id as customer_id,
        website_id,
        email,
        group_id as customer_group_id,
        store_id,
        is_active,
        prefix,
        firstname as first_name,
        middlename as middle_name,
        lastname as last_name,
        suffix,
        dob as date_of_birth,
        gender,
        taxvat as tax_vat,
        default_billing as default_billing_address_id,
        default_shipping as default_shipping_address_id,
        created_at,
        updated_at,
        created_in
    from {{ source('magento', 'customer_entity') }}
),

-- Get billing address details
billing_addresses as (
    select
        entity_id as address_id,
        parent_id as customer_id,
        city as billing_city,
        region as billing_region,
        region_id as billing_region_id,
        postcode as billing_postcode,
        country_id as billing_country,
        company as billing_company
    from {{ source('magento', 'customer_address_entity') }}
),

-- Get shipping address details
shipping_addresses as (
    select
        entity_id as address_id,
        parent_id as customer_id,
        city as shipping_city,
        region as shipping_region,
        region_id as shipping_region_id,
        postcode as shipping_postcode,
        country_id as shipping_country,
        company as shipping_company
    from {{ source('magento', 'customer_address_entity') }}
),

-- Join customers with their default addresses
joined as (
    select
        c.*,

        -- Billing address
        ba.billing_city,
        ba.billing_region,
        ba.billing_postcode,
        ba.billing_country,
        ba.billing_company,

        -- Shipping address
        sa.shipping_city,
        sa.shipping_region,
        sa.shipping_postcode,
        sa.shipping_country,
        sa.shipping_company

    from customers c
    left join billing_addresses ba
        on c.default_billing_address_id = ba.address_id
        and c.customer_id = ba.customer_id
    left join shipping_addresses sa
        on c.default_shipping_address_id = sa.address_id
        and c.customer_id = sa.customer_id
)

select
    {{ dbt_utils.generate_surrogate_key(['customer_id']) }} as customer_sk,
    customer_id,
    email,
    customer_group_id,
    website_id,
    store_id,

    -- Name fields
    prefix,
    first_name,
    middle_name,
    last_name,
    suffix,
    coalesce(first_name, '') || ' ' || coalesce(last_name, '') as full_name,

    -- Demographics
    date_of_birth,
    case
        when gender = 1 then 'Male'
        when gender = 2 then 'Female'
        else 'Not Specified'
    end as gender,
    datediff('year', date_of_birth, current_date()) as age,
    tax_vat,

    -- Status
    case when is_active = 1 then true else false end as is_active,

    -- Default billing address
    default_billing_address_id,
    billing_city,
    billing_region,
    billing_postcode,
    billing_country,
    billing_company,

    -- Default shipping address
    default_shipping_address_id,
    shipping_city,
    shipping_region,
    shipping_postcode,
    shipping_country,
    shipping_company,

    -- Timestamps
    created_at,
    updated_at,
    created_in,

    -- Derived: Customer tenure segmentation
    datediff('day', created_at, current_timestamp()) as days_since_registration,
    case
        when datediff('day', created_at, current_timestamp()) <= 30 then 'New (0-30 days)'
        when datediff('day', created_at, current_timestamp()) <= 90 then 'Recent (31-90 days)'
        when datediff('day', created_at, current_timestamp()) <= 365 then 'Established (91-365 days)'
        else 'Loyal (365+ days)'
    end as customer_tenure_segment,

    -- Registration cohort
    date_trunc('month', created_at)::date as registration_cohort_month,
    date_trunc('quarter', created_at)::date as registration_cohort_quarter,
    date_trunc('year', created_at)::date as registration_cohort_year

from joined
