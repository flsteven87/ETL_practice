from sqlalchemy import create_engine
import pandas as pd
# 建立資料庫連線
engine = create_engine("sqlite:///ecommerce.db")

# SQL查詢語句
query = """
SELECT name FROM sqlite_master WHERE type='table'
"""

df = pd.read_sql_query(query, engine)
print(df)
