{{
    config(
        materialized='table',
        tags=['facts', 'magento']
    )
}}

/*
    Magento Product Review Fact Table
    Grain: One row per review
    Source: MAGENTO.REVIEW, MAGENTO.REVIEW_DETAIL
*/

with reviews as (
    select
        review_id,
        entity_id,
        entity_pk_value as product_id,
        status_id,
        created_at as review_date
    from {{ source('magento', 'review') }}
),

review_details as (
    select
        detail_id,
        review_id,
        store_id,
        customer_id,
        title,
        detail as review_text,
        nickname
    from {{ source('magento', 'review_detail') }}
),

joined as (
    select
        r.review_id,
        r.product_id,
        r.status_id,
        r.review_date,
        rd.detail_id,
        rd.store_id,
        rd.customer_id,
        rd.title,
        rd.review_text,
        rd.nickname
    from reviews r
    left join review_details rd on r.review_id = rd.review_id
)

select
    {{ dbt_utils.generate_surrogate_key(['review_id']) }} as review_sk,
    review_id,
    detail_id,
    product_id,
    customer_id,
    store_id,

    -- Review content
    title,
    review_text,
    nickname as reviewer_name,

    -- Status
    status_id,
    case
        when status_id = 1 then 'Approved'
        when status_id = 2 then 'Pending'
        when status_id = 3 then 'Not Approved'
        else 'Unknown'
    end as status_label,
    case when status_id = 1 then true else false end as is_approved,

    -- Dates
    review_date,
    review_date::date as review_date_day,
    date_trunc('month', review_date)::date as review_date_month,

    -- Customer flags
    case when customer_id is not null then true else false end as is_registered_customer,

    -- Review text analysis
    length(coalesce(review_text, '')) as review_length,
    case
        when length(coalesce(review_text, '')) < 50 then 'Short'
        when length(coalesce(review_text, '')) < 200 then 'Medium'
        else 'Long'
    end as review_length_category

from joined
