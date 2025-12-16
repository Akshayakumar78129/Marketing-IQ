"""
Snowflake Data Explorer - Marketing IQ
"""
import snowflake.connector
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

# Connection parameters from environment
conn_params = {
    "account": os.getenv("SNOWFLAKE_ACCOUNT"),
    "user": os.getenv("SNOWFLAKE_USER"),
    "password": os.getenv("SNOWFLAKE_PASSWORD"),
    "role": os.getenv("SNOWFLAKE_ROLE"),
    "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE"),
    "database": os.getenv("SNOWFLAKE_DATABASE")
}

def run_query(cursor, query, description=""):
    """Run a query and print results"""
    print(f"\n{'='*60}")
    print(f"Query: {description or query[:50]}")
    print('='*60)
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        columns = [col[0] for col in cursor.description]

        # Print column headers
        print(" | ".join(columns))
        print("-" * 60)

        # Print rows
        for row in results[:50]:  # Limit to 50 rows
            print(" | ".join(str(val)[:30] for val in row))

        if len(results) > 50:
            print(f"... and {len(results) - 50} more rows")

        return results
    except Exception as e:
        print(f"Error: {e}")
        return []

def main():
    # Validate environment variables
    missing = [k for k, v in conn_params.items() if not v]
    if missing:
        print(f"Error: Missing environment variables: {missing}")
        print("Please check your .env file")
        sys.exit(1)

    print("Connecting to Snowflake...")

    try:
        conn = snowflake.connector.connect(**conn_params)
        cursor = conn.cursor()
        print("Connected successfully!")

        # 1. List all schemas
        run_query(cursor, f"SHOW SCHEMAS IN DATABASE {conn_params['database']}", "List all schemas")

        # 2. List tables in each schema
        schemas_to_check = ["GA4", "GOOGLE_ADS", "FACEBOOK_ADS"]

        for schema in schemas_to_check:
            run_query(cursor, f"SHOW TABLES IN SCHEMA {conn_params['database']}.{schema}", f"Tables in {schema}")

        # 3. Sample data from key tables
        print("\n" + "="*60)
        print("SAMPLE DATA FROM KEY TABLES")
        print("="*60)

        # GA4 - Traffic acquisition
        run_query(cursor, f"""
            SELECT * FROM {conn_params['database']}.GA4.TRAFFIC_ACQUISITION_SESSION_SOURCE_MEDIUM_REPORT
            LIMIT 5
        """, "GA4 Traffic Acquisition Sample")

        # Google Ads - Campaign stats
        run_query(cursor, f"""
            SELECT * FROM {conn_params['database']}.GOOGLE_ADS.CAMPAIGN_STATS
            LIMIT 5
        """, "Google Ads Campaign Stats Sample")

        # Facebook Ads - Check what tables exist
        run_query(cursor, f"SHOW TABLES IN SCHEMA {conn_params['database']}.FACEBOOK_ADS", "Tables in FACEBOOK_ADS")

        cursor.close()
        conn.close()
        print("\nConnection closed.")

    except Exception as e:
        print(f"Connection error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
