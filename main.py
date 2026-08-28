from dotenv import load_dotenv
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

question = input("Ask a question about your sales data: ")

schema = get_schema()

sql_query, result = run_query_with_retry(
    question,
    schema
)

if sql_query is None:
    print("\nI cannot answer this question using the available data.")
    exit()

logger.info("Database result: %s", result)

answer = generate_answer(
    question,
    sql_query,
    result
)

print("\nAnswer:")
print(answer)