
  
    

create or replace transient table CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.dim_person
    
    
    
    as (

/*
    Person/Customer Dimension Table (Klaviyo)
    Contains customer profiles with CLV predictions and churn probability
    Source: KLAVIYO.PERSON
*/

with persons as (
    select
        id as person_id,
        email,
        first_name,
        last_name,
        city,
        region,
        country,

        -- Predictive Analytics (CLV & Churn)
        predictive_analytics_predicted_clv as predicted_clv,
        predictive_analytics_historic_clv as historic_clv,
        predictive_analytics_total_clv as total_clv,
        predictive_analytics_churn_probability as churn_probability,
        predictive_analytics_average_order_value as predicted_aov,
        predictive_analytics_historic_number_of_orders as historic_order_count,
        predictive_analytics_predicted_number_of_orders as predicted_order_count,
        predictive_analytics_average_days_between_orders as avg_days_between_orders,
        predictive_analytics_expected_date_of_next_order as expected_next_order_date,

        -- Custom Order Data
        custom_total_orders as custom_order_count,
        custom_average_order_value as custom_aov,
        custom_first_order_date as first_order_date,
        custom_last_order_date as last_order_date,
        custom_last_order_total as last_order_value,

        created as created_at,
        updated as updated_at,
        _fivetran_deleted as is_deleted,
        _fivetran_synced as last_synced
    from CLIENT_RARE_SEEDS_DB.KLAVIYO.person
    where _fivetran_deleted = false or _fivetran_deleted is null
)

select
    md5(cast(coalesce(cast(person_id as TEXT), '_dbt_utils_surrogate_key_null_') as TEXT)) as person_sk,
    'klaviyo' as platform,
    person_id,
    email,
    first_name,
    last_name,

    -- Location
    city,
    region,
    country,

    -- CLV Metrics
    predicted_clv,
    historic_clv,
    total_clv,
    churn_probability,

    -- Churn Risk Segment
    case
        when churn_probability >= 0.7 then 'High Risk'
        when churn_probability >= 0.4 then 'Medium Risk'
        when churn_probability >= 0.1 then 'Low Risk'
        else 'Healthy'
    end as churn_risk_segment,

    -- CLV Segment
    case
        when total_clv >= 500 then 'High Value'
        when total_clv >= 200 then 'Medium Value'
        when total_clv >= 50 then 'Low Value'
        else 'New/Minimal'
    end as clv_segment,

    -- Order Metrics
    predicted_aov,
    historic_order_count,
    predicted_order_count,
    avg_days_between_orders,
    expected_next_order_date,

    -- Custom Order Data
    custom_order_count,
    custom_aov,
    first_order_date,
    last_order_date,
    last_order_value,

    -- Timestamps
    created_at,
    updated_at,
    last_synced
from persons
    )
;


  