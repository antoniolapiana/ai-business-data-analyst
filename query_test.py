import sqlite3
from database import get_schema

schema = get_schema()

print(schema)

connection = sqlite3.connect("sales.db")
cursor = connection.cursor()

cursor.execute("""
SELECT region, SUM(revenue)
FROM sales
GROUP BY region
""")

rows = cursor.fetchall()

for row in rows:
    print(row)

connection.close()