from google import genai
from dotenv import load_dotenv
import os
from sql_validator import validate_sql
from database import execute_query
from ai_analyst import generate_sql, generate_answer,  run_query_with_retry
from database import execute_query, get_schema
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)

logger = logging.getLogger(__name__)

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

question = input("Ask a question about your sales data: ")

schema = get_schema()

sql_query, result = run_query_with_retry(
    client,
    question,
    schema
)

logger.info("Database result: %s", result)

answer = generate_answer(
    client,
    question,
    sql_query,
    result
)

print("\nAnswer:")
print(answer)