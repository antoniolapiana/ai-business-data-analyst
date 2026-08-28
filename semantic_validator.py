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

Return ONLY one of these two values:

SUPPORTED
UNSUPPORTED
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

    result = response.message.content.strip().upper()

    if "UNSUPPORTED" in result:
        return False

    if "SUPPORTED" in result:
        return True

    raise ValueError("Invalid semantic validation result.")