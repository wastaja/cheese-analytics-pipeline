import duckdb
import pandas as pd

pd.set_option("display.max_columns", None)

con = duckdb.connect("data/cheese_analytics.db")

df = con.execute("""
    select *
    from mart_cheese_features
    limit 10
""").df()

print(df)