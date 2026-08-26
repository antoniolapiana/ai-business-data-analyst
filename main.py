from google import genai
from dotenv import load_dotenv
import os
from sql_model import SQLQuery
from sql_validator import validate_sql
from database import execute_query
from ai_analyst import generate_sql, generate_answer

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

question = "Quanto abbiamo fatturato in Irlanda?"

sql_query = generate_sql(client, question)

print("Generated SQL:")
print(sql_query)

validate_sql(sql_query)

result = execute_query(sql_query)

print("\nDatabase result:")
print(result)

answer = generate_answer(
    client,
    question,
    sql_query,
    result
)

print("\nAnswer:")
print(answer)