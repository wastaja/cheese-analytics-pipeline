import duckdb
from pathlib import Path

Path("data/processed").mkdir(parents=True, exist_ok=True)

con = duckdb.connect("data/cheese_analytics.db")

# RAW - cheese details
con.execute("""
    create or replace view cheese_details_raw as
    select * from read_csv_auto('data/raw/cheese_details.csv')
""")

# STAGING - cheese details
with open('sql/staging/stg_cheese_details.sql', 'r') as f:
    stg_cheese_details_query = f.read()

con.execute(f"""
    create or replace view stg_cheese_details as
    {stg_cheese_details_query}
""")

print("Pipeline executed successfully.")


# MART - cheese features
with open('sql/marts/mart_cheese_features.sql', 'r') as f:
    mart_query = f.read()

con.execute(f"""
    create or replace view mart_cheese_features as
    {mart_query}
""")

df = con.execute("""
    select *
    from mart_cheese_features
""").df()

df.to_csv("data/processed/mart_cheese_features.csv", index=False)