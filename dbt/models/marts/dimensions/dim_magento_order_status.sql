{{
    config(
        materialized='table',
        tags=['dimensions', 'magento']
    )
}}

/*
    Magento Order Status Dimension
    Order status reference with state mapping
    Source: MAGENTO.SALES_ORDER_STATUS, MAGENTO.SALES_ORDER_STATUS_STATE, MAGENTO.SALES_ORDER_STATUS_LABEL
*/

with order_statuses as (
    select
        status,
        label as status_label
    from {{ source('magento', 'sales_order_status') }}
),

status_states as (
    select
        status,
        state,
        is_default,
        visible_on_front
    from {{ source('magento', 'sales_order_status_state') }}
),

-- Get primary store labels (store_id = 1) with fallback to any available
status_labels as (
    select
        status,
        store_id,
        label as store_label,
        row_number() over (
            partition by status
            order by case when store_id = 1 then 1 when store_id = 0 then 2 else 3 end
        ) as rn
    from {{ source('magento', 'sales_order_status_label') }}
),

primary_labels as (
    select status, store_label
    from status_labels
    where rn = 1
),

joined as (
    select
        os.status,
        os.status_label,
        ss.state,
        ss.is_default,
        ss.visible_on_front,
        pl.store_label
    from order_statuses os
    left join status_states ss on os.status = ss.status
    left join primary_labels pl on os.status = pl.status
)

select
    {{ dbt_utils.generate_surrogate_key(['status']) }} as order_status_sk,
    status,
    coalesce(store_label, status_label) as status_label,
    state,

    -- Boolean conversions
    case when is_default = 1 then true else false end as is_default,
    case when visible_on_front = 1 then true else false end as is_visible_on_front,

    -- State category flags for easier filtering
    case when state = 'new' then true else false end as is_new,
    case when state = 'pending_payment' then true else false end as is_pending_payment,
    case when state = 'processing' then true else false end as is_processing,
    case when state = 'complete' then true else false end as is_complete,
    case when state = 'closed' then true else false end as is_closed,
    case when state = 'canceled' then true else false end as is_canceled,
    case when state = 'holded' then true else false end as is_on_hold,
    case when state = 'payment_review' then true else false end as is_payment_review,

    -- Status groups
    case
        when state in ('new', 'pending_payment', 'payment_review') then 'Pending'
        when state = 'processing' then 'Active'
        when state = 'complete' then 'Completed'
        when state in ('closed', 'canceled') then 'Closed'
        when state = 'holded' then 'On Hold'
        else 'Other'
    end as status_group

from joined
