from google import genai
from sql_model import SQLQuery
import os


def generate_sql(client, question):
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

Return the SQL query in the required structured format.
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

    return sql_data.sql


def generate_answer(client, question, sql_query, result):
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

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=answer_prompt
    )

    return response.text