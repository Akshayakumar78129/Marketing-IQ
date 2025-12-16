{{
    config(
        materialized='table',
        tags=['dimensions']
    )
}}

/*
    Date dimension table
    Generated from a date spine for the relevant date range
*/

with date_spine as (
    {{ dbt_utils.date_spine(
        datepart="day",
        start_date="cast('2023-01-01' as date)",
        end_date="cast(current_date() + 365 as date)"
    ) }}
),

dates as (
    select
        date_day as date_key,
        date_day,
        extract(year from date_day) as year,
        extract(month from date_day) as month,
        extract(day from date_day) as day_of_month,
        extract(dayofweek from date_day) as day_of_week,
        extract(quarter from date_day) as quarter,
        extract(week from date_day) as week_of_year,

        -- Date names
        to_char(date_day, 'YYYY-MM') as year_month,
        to_char(date_day, 'Mon') as month_name_short,
        to_char(date_day, 'Month') as month_name,
        to_char(date_day, 'Dy') as day_name_short,
        to_char(date_day, 'Day') as day_name,

        -- Flags
        case when extract(dayofweek from date_day) in (0, 6) then true else false end as is_weekend,
        case when date_day = current_date() then true else false end as is_today,

        -- Relative periods
        datediff('day', date_day, current_date()) as days_ago

    from date_spine
)

select * from dates
