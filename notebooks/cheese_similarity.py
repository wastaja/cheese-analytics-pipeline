import duckdb
import pandas as pd

pd.set_option("display.max_columns", None)

con = duckdb.connect("data/cheese_analytics.db")

selected_cheese = "Aettis"

query = f"""
with similarity as (
    {open('sql/analysis/cheese_similarity.sql').read()}
)

select *
from similarity
where source_cheese = '{selected_cheese}'
order by similarity_score desc
limit 5
"""

df = con.execute(query).df()

print(f"\nTop similar cheeses to: {selected_cheese}\n")
print(df)