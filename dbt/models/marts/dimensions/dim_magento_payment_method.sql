{{
    config(
        materialized='table',
        tags=['dimensions', 'magento']
    )
}}

/*
    Magento Payment Method Dimension
    Derived from distinct payment methods used in orders
    Source: MAGENTO.SALES_ORDER_PAYMENT
*/

with payment_methods as (
    select distinct
        method as payment_method_code,
        cc_type
    from {{ source('magento', 'sales_order_payment') }}
    where method is not null
),

payment_method_labels as (
    select
        payment_method_code,
        cc_type,

        -- Create descriptive label based on method code
        case
            when payment_method_code = 'checkmo' then 'Check / Money Order'
            when payment_method_code = 'free' then 'Free'
            when payment_method_code = 'cashondelivery' then 'Cash on Delivery'
            when payment_method_code = 'banktransfer' then 'Bank Transfer'
            when payment_method_code = 'purchaseorder' then 'Purchase Order'
            when payment_method_code like 'paypal%' then 'PayPal'
            when payment_method_code like 'braintree%' then 'Braintree'
            when payment_method_code like 'stripe%' then 'Stripe'
            when payment_method_code like 'authorizenet%' then 'Authorize.Net'
            when payment_method_code like 'amazon%' then 'Amazon Pay'
            when payment_method_code like 'klarna%' then 'Klarna'
            when payment_method_code like 'affirm%' then 'Affirm'
            when payment_method_code like 'afterpay%' then 'Afterpay'
            when payment_method_code = 'ccsave' then 'Credit Card (Saved)'
            else initcap(replace(payment_method_code, '_', ' '))
        end as payment_method_name,

        -- Payment type categorization
        case
            when payment_method_code in ('checkmo', 'banktransfer', 'purchaseorder', 'cashondelivery') then 'Offline'
            when payment_method_code = 'free' then 'Free'
            when payment_method_code like 'paypal%' or payment_method_code like 'amazon%' then 'Digital Wallet'
            when payment_method_code like 'klarna%' or payment_method_code like 'affirm%' or payment_method_code like 'afterpay%' then 'Buy Now Pay Later'
            else 'Credit Card'
        end as payment_type,

        -- Is credit card based
        case
            when payment_method_code like 'braintree%'
              or payment_method_code like 'stripe%'
              or payment_method_code like 'authorizenet%'
              or payment_method_code = 'ccsave'
              or cc_type is not null
            then true
            else false
        end as is_credit_card,

        -- Is digital wallet
        case
            when payment_method_code like 'paypal%'
              or payment_method_code like 'amazon%'
              or payment_method_code like 'applepay%'
              or payment_method_code like 'googlepay%'
            then true
            else false
        end as is_digital_wallet,

        -- Is buy now pay later
        case
            when payment_method_code like 'klarna%'
              or payment_method_code like 'affirm%'
              or payment_method_code like 'afterpay%'
            then true
            else false
        end as is_bnpl

    from payment_methods
)

select
    {{ dbt_utils.generate_surrogate_key(['payment_method_code']) }} as payment_method_sk,
    payment_method_code,
    payment_method_name,
    payment_type,
    is_credit_card,
    is_digital_wallet,
    is_bnpl,
    cc_type as credit_card_type
from payment_method_labels
