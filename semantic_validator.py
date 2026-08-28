from ollama import chat


def validate_question(question, schema, business_context):
    prompt = f"""
You are a semantic validator for a business data analysis system.

Determine whether the user's question can be answered using ONLY the available database schema and business context.

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