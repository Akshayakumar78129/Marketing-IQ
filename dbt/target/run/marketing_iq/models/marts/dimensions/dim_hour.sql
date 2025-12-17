
  
    

create or replace transient table CLIENT_RARE_SEEDS_DB.PUBLIC_analytics.dim_hour
    
    
    
    as (

/*
    Hour dimension table
    Generated static dimension for hourly analysis (0-23)
*/

with hours as (
    select row_number() over (order by seq4()) - 1 as hour_of_day
    from table(generator(rowcount => 24))
)

select
    hour_of_day as hour_key,
    hour_of_day,
    case
        when hour_of_day between 0 and 5 then 'Night'
        when hour_of_day between 6 and 11 then 'Morning'
        when hour_of_day between 12 and 17 then 'Afternoon'
        else 'Evening'
    end as day_part,
    case
        when hour_of_day between 9 and 17 then true
        else false
    end as is_business_hours,
    lpad(hour_of_day::varchar, 2, '0') || ':00' as hour_label,
    case
        when hour_of_day = 0 then '12 AM'
        when hour_of_day < 12 then hour_of_day::varchar || ' AM'
        when hour_of_day = 12 then '12 PM'
        else (hour_of_day - 12)::varchar || ' PM'
    end as hour_label_12h
from hours
    )
;


  