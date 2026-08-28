from ollama import chat


def validate_question(question, schema, business_context):
    prompt = f"""
You are a semantic validator for a business data analysis system.

Determine whether the user's question can be answered using the available database schema and business context.

A question is SUPPORTED if the required answer can be obtained directly OR calculated/derived from the available fields using valid SQL operations such as:
- SUM
- AVG
- COUNT
- MIN
- MAX
- arithmetic between columns or aggregates
- GROUP BY
- filtering
- sorting

Do not require the requested business metric to exist as a physical database column.

For example:
If the schema contains revenue and quantity, a question about average revenue per unit is SUPPORTED because it can be calculated from those fields.

Database schema:
{schema}

Business context:
{business_context}

User question:
{question}

If the question can be answered using the available data, return:
SUPPORTED

If the question cannot be answered, return:
UNSUPPORTED: <brief explanation of why the available data is insufficient>

Do not invent missing data.
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

    result = response.message.content.strip()

    if result.upper().startswith("UNSUPPORTED"):
        return False, result

    if result.upper().startswith("SUPPORTED"):
        return True, result

    raise ValueError("Invalid semantic validation result.")