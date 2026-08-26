from google import genai
from dotenv import load_dotenv
import sqlite3
import os
from sql_model import SQLQuery
from sql_validator import validate_sql

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

question = "Quanto abbiamo fatturato in Irlanda?"

prompt = f"""
You are a business data analyst.

Convert the user's question into a SQLite SQL query.

Database table:
sales

Columns:
- date: TEXT
- product: TEXT
- region: TEXT
- quantity: INTEGER
- revenue: REAL

Known region values:
- Ireland
- UK
- Germany

User question:
{question}

Return ONLY the SQL query.
"""

response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=prompt,
    config={
        "response_mime_type": "application/json",
        "response_schema": SQLQuery,
    },
)

sql_data = SQLQuery.model_validate_json(response.text)

sql_query = sql_data.sql

print("Generated SQL:")
print(sql_query)

connection = sqlite3.connect("sales.db")
cursor = connection.cursor()

validate_sql(sql_query)
cursor.execute(sql_query)

result = cursor.fetchall()

print("\nDatabase result:")
print(result)

answer_prompt = f"""
You are a business data analyst.

Answer the user's question using the database result below.

User question:
{question}

SQL query:
{sql_query}

Database result:
{result}

Give a concise answer in natural language.
Do not mention SQL, Python, or the database.
"""

answer_response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=answer_prompt
)

print("\nAnswer:")
print(answer_response.text)

connection.close()