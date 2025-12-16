"""
Explore Snowflake schema structure for fact/dimension design
"""
import snowflake.connector
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

conn_params = {
    "account": os.getenv("SNOWFLAKE_ACCOUNT"),
    "user": os.getenv("SNOWFLAKE_USER"),
    "password": os.getenv("SNOWFLAKE_PASSWORD"),
    "role": os.getenv("SNOWFLAKE_ROLE"),
    "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE"),
    "database": os.getenv("SNOWFLAKE_DATABASE")
}

def describe_table(cursor, schema, table):
    """Get column info for a table"""
    print(f"\n{'='*70}")
    print(f"TABLE: {schema}.{table}")
    print('='*70)
    cursor.execute(f"DESCRIBE TABLE {schema}.{table}")
    results = cursor.fetchall()
    for row in results:
        print(f"  {row[0]:40} {row[1]:20} {row[3] if row[3] else ''}")
    return results

def sample_data(cursor, schema, table, limit=3):
    """Get sample data"""
    print(f"\nSample Data ({limit} rows):")
    cursor.execute(f"SELECT * FROM {schema}.{table} LIMIT {limit}")
    results = cursor.fetchall()
    columns = [col[0] for col in cursor.description]
    print("  " + " | ".join(col[:15] for col in columns[:8]))
    print("  " + "-"*100)
    for row in results:
        print("  " + " | ".join(str(val)[:15] if val else "NULL" for val in row[:8]))

def main():
    print("Connecting to Snowflake...")
    conn = snowflake.connector.connect(**conn_params)
    cursor = conn.cursor()
    print("Connected!\n")

    # Key tables to explore for fact/dimension design
    key_tables = [
        # Google Ads - Main stats tables
        ("GOOGLE_ADS", "CAMPAIGN_STATS"),
        ("GOOGLE_ADS", "CAMPAIGN_HISTORY"),
        ("GOOGLE_ADS", "AD_GROUP_STATS"),
        ("GOOGLE_ADS", "AD_STATS"),

        # Facebook Ads - Main tables
        ("FACEBOOK_ADS", "BASIC_AD"),
        ("FACEBOOK_ADS", "AD_HISTORY"),
        ("FACEBOOK_ADS", "AD_SET_HISTORY"),
        ("FACEBOOK_ADS", "CAMPAIGN_HISTORY"),

        # GA4 - Traffic & conversions
        ("GA4", "TRAFFIC_ACQUISITION_SESSION_SOURCE_MEDIUM_REPORT"),
        ("GA4", "CONVERSIONS_REPORT"),
        ("GA4", "EVENTS_REPORT"),
    ]

    for schema, table in key_tables:
        try:
            describe_table(cursor, schema, table)
            sample_data(cursor, schema, table)
        except Exception as e:
            print(f"  Error: {e}")

    cursor.close()
    conn.close()
    print("\n\nDone!")

if __name__ == "__main__":
    main()
