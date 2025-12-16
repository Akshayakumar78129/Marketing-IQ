@echo off
set SNOWFLAKE_ACCOUNT=zvesymu-vl35446
set SNOWFLAKE_USER=FIVETRAN_USER
set SNOWFLAKE_PASSWORD=MarketingIQ-kaleitics01
set SNOWFLAKE_ROLE=FIVETRAN_ROLE
set SNOWFLAKE_WAREHOUSE=FIVETRAN_WH
cd /d "C:\Users\Akshay kumar\Desktop\Marketing-IQ\dbt"
dbt %*
