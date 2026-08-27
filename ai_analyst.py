from ollama import chat
from sql_model import SQLQuery
import os
from database import execute_query
from sql_validator import validate_sql
from business_context import BUSINESS_CONTEXT
from schema_validator import validate_schema


def generate_sql(question, schema, previous_error=None):
    error_context = ""

    if previous_error:
        error_context = f"""
The previous SQL query failed with this error:
{previous_error}

Generate a corrected SQL query that fixes this error.
"""

    prompt = f"""
You are a business data analyst.

Convert the user's question into a SQLite SQL query.

Database schema:
{schema}

Business context:
{BUSINESS_CONTEXT}

{error_context}

User question:
{question}

Return ONLY the SQL query.
Do not use markdown.
Do not use ```sql.
Do not explain anything.
"""

    response = chat(
        model="qwen2.5:7b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.message.content.strip()


def generate_answer(question, sql_query, result):

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

    response = chat(
        model="qwen2.5:7b",
        messages=[
            {
                "role": "user",
                "content": answer_prompt
            }
        ]
    )

    return response.message.content.strip()


def run_query_with_retry(
    question,
    schema
):
    sql_query = generate_sql(
        question,
        schema
    )

    print("\nGenerated SQL:")
    print(sql_query)

    validate_sql(sql_query)
    validate_schema(sql_query, schema)

    try:
        result = execute_query(sql_query)

    except Exception as e:
        print("\nSQL Error:")
        print(e)

        sql_query = generate_sql(
            question,
            schema,
            previous_error=str(e)
        )

        print("\nCorrected SQL:")
        print(sql_query)

        validate_sql(sql_query)
        validate_schema(sql_query, schema)

        result = execute_query(sql_query)

    return sql_query, result