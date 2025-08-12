import json
import os
import time

from openai import OpenAI


def analyze_transaction_with_llm(description: str) -> dict:
    """Use OpenAI to detect fraud in transaction description."""

    if not description:
        return {"is_fraud": False, "reason": "No description"}

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    try:
        response = client.responses.create(
            model="gpt-5-nano",
            input=f'Is this transaction description fraudulent? "{description}" Return your answer exclusively in JSON format: {{"is_fraud": true/false, "reason": "brief explanation"}}',
        )
        result = response.output_text
        json_content = json.loads(result)
        return json_content.get("is_fraud", False), json_content.get("reason", "Unknown")

    except Exception as e:
        print("Error calling OpenAI API:", e)
        return False, "API error"
