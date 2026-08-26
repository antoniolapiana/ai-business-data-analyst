import csv
import sqlite3


connection = sqlite3.connect("sales.db")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS sales (
    date TEXT,
    product TEXT,
    region TEXT,
    quantity INTEGER,
    revenue REAL
)
""")


with open("sales.csv", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        cursor.execute(
            """
            INSERT INTO sales (date, product, region, quantity, revenue)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                row["date"],
                row["product"],
                row["region"],
                int(row["quantity"]),
                float(row["revenue"]),
            ),
        )


connection.commit()
connection.close()

print("Database created successfully.")